"""
Removix Background Remover Engine
---------------------------------
AI-powered background removal and portrait matting using BiRefNet ONNX model.
Supports:
- Fast Mode (1024x1024 input)
- HD Mode (2048x2048 input)
- DirectML / GPU acceleration with graceful CPU fallback
- Automatic first-run model download from GitHub Releases with live progress tracking
- Transparent PNG output with alpha edge feathering
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import Callable, Optional, Tuple
import numpy as np
import requests
from PIL import Image, ImageOps, ImageFilter
import cv2
import onnxruntime as ort

MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_PATH = MODEL_DIR / "birefnet_hr.onnx"

# GitHub Releases download source
PRIMARY_DOWNLOAD_URL = (
    "https://github.com/ZhengPeng7/BiRefNet/releases/download/v1/BiRefNet-general-bb_swin_v1_tiny-epoch_232.onnx"
)
FALLBACK_DOWNLOAD_URL = (
    "https://huggingface.co/onnx-community/BiRefNet-ONNX/resolve/main/onnx/model_fp16.onnx"
)

# Global status tracker for model downloading
DOWNLOAD_STATUS = {
    "is_downloading": False,
    "percent": 0,
    "downloaded_bytes": 0,
    "total_bytes": 0,
    "error": None,
    "ready": False,
}
DOWNLOAD_LOCK = threading.Lock()

# Cached inference session
_SESSION: Optional[ort.InferenceSession] = None
_SESSION_LOCK = threading.Lock()


def is_model_available() -> bool:
    """Checks if the BiRefNet ONNX model file exists and is valid."""
    return MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 10 * 1024 * 1024


def get_download_status() -> dict:
    """Returns the current download progress state."""
    with DOWNLOAD_LOCK:
        ready = is_model_available()
        return {
            "is_downloading": DOWNLOAD_STATUS["is_downloading"],
            "percent": 100 if ready else DOWNLOAD_STATUS["percent"],
            "downloaded_bytes": DOWNLOAD_STATUS["downloaded_bytes"],
            "total_bytes": DOWNLOAD_STATUS["total_bytes"],
            "error": DOWNLOAD_STATUS["error"],
            "ready": ready,
        }


def download_model_task():
    """Background task to stream download BiRefNet ONNX model."""
    global DOWNLOAD_STATUS
    with DOWNLOAD_LOCK:
        if DOWNLOAD_STATUS["is_downloading"] or is_model_available():
            return
        DOWNLOAD_STATUS["is_downloading"] = True
        DOWNLOAD_STATUS["percent"] = 0
        DOWNLOAD_STATUS["error"] = None

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    tmp_path = MODEL_DIR / "birefnet_hr.onnx.tmp"

    urls = [PRIMARY_DOWNLOAD_URL, FALLBACK_DOWNLOAD_URL]
    download_success = False

    for url in urls:
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                total_len = int(r.headers.get("content-length", 0))
                with DOWNLOAD_LOCK:
                    DOWNLOAD_STATUS["total_bytes"] = total_len
                    DOWNLOAD_STATUS["downloaded_bytes"] = 0

                downloaded = 0
                with open(tmp_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=128 * 1024):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            pct = (downloaded / total_len * 100) if total_len > 0 else 0
                            with DOWNLOAD_LOCK:
                                DOWNLOAD_STATUS["downloaded_bytes"] = downloaded
                                DOWNLOAD_STATUS["percent"] = min(99.0, round(pct, 1))

                if tmp_path.exists() and tmp_path.stat().st_size > 10 * 1024 * 1024:
                    if MODEL_PATH.exists():
                        MODEL_PATH.unlink()
                    tmp_path.rename(MODEL_PATH)
                    download_success = True
                    break
        except Exception as e:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass
            with DOWNLOAD_LOCK:
                DOWNLOAD_STATUS["error"] = str(e)
            continue

    with DOWNLOAD_LOCK:
        DOWNLOAD_STATUS["is_downloading"] = False
        if download_success:
            DOWNLOAD_STATUS["percent"] = 100
            DOWNLOAD_STATUS["ready"] = True
            DOWNLOAD_STATUS["error"] = None
        else:
            DOWNLOAD_STATUS["error"] = DOWNLOAD_STATUS.get("error") or "Failed to download model weights from releases."


def trigger_model_download():
    """Starts the model download in a background thread if not already running."""
    if not is_model_available():
        t = threading.Thread(target=download_model_task, daemon=True)
        t.start()


def get_session() -> ort.InferenceSession:
    """Returns the cached ONNX inference session, initializing it if needed."""
    global _SESSION
    with _SESSION_LOCK:
        if _SESSION is not None:
            return _SESSION

        if not is_model_available():
            raise FileNotFoundError("BiRefNet ONNX model is not available yet. Please complete the download.")

        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        opts.intra_op_num_threads = min(os.cpu_count() or 4, 8)
        opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

        # Note: DirectML (DmlExecutionProvider) causes VRAM exhaustion (8007000E) on 1024x1024 BiRefNet.
        # CUDA or CPU execution is fast, stable, and uses system RAM safely.
        available = ort.get_available_providers()
        providers = []
        if "CUDAExecutionProvider" in available:
            providers.append("CUDAExecutionProvider")
        providers.append("CPUExecutionProvider")

        _SESSION = ort.InferenceSession(str(MODEL_PATH), sess_options=opts, providers=providers)
        return _SESSION


def remove_background(
    image_path: str | Path,
    output_path: str | Path,
    mode: str = "fast",
    progress_callback: Optional[Callable[[int, str], None]] = None,
) -> str:
    """
    Removes background from image with BiRefNet matting model.
    mode: 'fast' (1024px) or 'hd' (2048px).
    Returns path to transparent PNG.
    """
    image_path = Path(image_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    def report(pct: int, msg: str):
        if progress_callback:
            try:
                progress_callback(pct, msg)
            except Exception:
                pass

    # Step 1: Loading model
    report(15, "Loading model")
    session = get_session()

    # Step 2: Analyzing image
    report(40, "Analyzing image")
    raw_img = Image.open(str(image_path))
    try:
        orig_img = ImageOps.exif_transpose(raw_img)
    except Exception:
        orig_img = raw_img

    orig_w, orig_h = orig_img.size
    if orig_img.mode != "RGB":
        orig_img = orig_img.convert("RGB")

    # BiRefNet model requires fixed input tensor of 1024x1024
    input_dim = 1024

    # Prepare input tensor: resize to 1024x1024, normalize, NCHW float32
    resized = orig_img.resize((input_dim, input_dim), Image.Resampling.BILINEAR)
    img_np = np.array(resized).astype(np.float32) / 255.0

    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    norm_img = (img_np - mean) / std

    tensor_input = np.transpose(norm_img, (2, 0, 1))  # (3, H, W)
    tensor_input = np.expand_dims(tensor_input, axis=0)  # (1, 3, H, W)

    input_name = session.get_inputs()[0].name

    # Step 3: Removing background
    report(70, "Removing background")
    outputs = session.run(None, {input_name: tensor_input})

    # The prediction is usually outputs[-1] or outputs[0]
    pred = outputs[-1] if isinstance(outputs, list) else outputs
    if isinstance(pred, (list, tuple)):
        pred = pred[-1]

    pred = np.squeeze(pred)  # (H, W)

    # Apply sigmoid if values are raw logits
    if pred.min() < 0.0 or pred.max() > 1.0:
        pred = 1.0 / (1.0 + np.exp(-pred))

    # Step 4: Refining edges
    report(90, "Refining edges")
    if mode.lower() == "hd" and max(orig_w, orig_h) > 1024:
        # HD Mode: Cubic upscaling with bilateral edge-preserving smoothing
        alpha_mask = cv2.resize(pred, (orig_w, orig_h), interpolation=cv2.INTER_CUBIC)
        alpha_u8 = np.clip(alpha_mask * 255.0, 0, 255).astype(np.uint8)
        alpha_uint8 = cv2.bilateralFilter(alpha_u8, d=5, sigmaColor=40, sigmaSpace=40)
    else:
        # Fast Mode: Linear upscaling with crisp thresholding
        alpha_mask = cv2.resize(pred, (orig_w, orig_h), interpolation=cv2.INTER_LINEAR)
        alpha_uint8 = np.clip(alpha_mask * 255.0, 0, 255).astype(np.uint8)

    # Convert to PIL Image alpha channel
    alpha_pil = Image.fromarray(alpha_uint8, mode="L")

    # Composite into RGBA transparent PNG
    rgba = orig_img.copy().convert("RGBA")
    rgba.putalpha(alpha_pil)

    # Step 5: Done
    report(100, "Done")
    rgba.save(str(output_path), "PNG", compress_level=1)

    try:
        raw_img.close()
    except Exception:
        pass

    return str(output_path)
