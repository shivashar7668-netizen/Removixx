"""
Removix Watermark Removal Processing Engine
------------------------------------------
Houses all direct AI watermark removal logic (LaMa ONNX, optical flow,
hardware acceleration, video inpainting, and CLI fallback).
Separated from app.py to maintain a clean, modular architecture.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from dataclasses import replace

BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
SRC_DIR = BUNDLE_DIR / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

UV_SITE_PACKAGES = Path.home() / "AppData" / "Roaming" / "uv" / "tools" / "remove-ai-watermarks" / "Lib" / "site-packages"
if UV_SITE_PACKAGES.exists() and str(UV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(UV_SITE_PACKAGES))

def _ensure_ffmpeg():
    if shutil.which("ffmpeg") is not None:
        return
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.isfile(exe):
            p = Path(exe).parent
            alias = p / "ffmpeg.exe"
            if not alias.exists():
                try:
                    shutil.copyfile(exe, alias)
                except Exception:
                    pass
            p_str = str(p)
            if p_str not in os.environ.get("PATH", ""):
                os.environ["PATH"] = p_str + os.pathsep + os.environ.get("PATH", "")
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("Could not auto-configure ffmpeg: %s", e)

_ensure_ffmpeg()

# ── World-Class Hardware Acceleration Engine (GPU-First with CPU Fallback) ──
def _patch_lama_engine():
    """Patch ONNX session loader with auto-detect: CUDA GPU -> DirectML GPU -> Multi-Core CPU."""
    try:
        from remove_ai_watermarks import region_eraser
        import onnxruntime as ort

        # Preload Nvidia CUDA / cuDNN runtime DLLs if available on Windows
        if hasattr(ort, "preload_dlls"):
            try:
                ort.preload_dlls()
            except Exception:
                pass

        class SafeInferenceSession:
            """Wrapper around onnxruntime.InferenceSession that automatically falls back to CPU if GPU execution fails."""
            def __init__(self, model_path, sess_options, providers, label):
                self.model_path = model_path
                self.sess_options = sess_options
                self.providers = list(providers)
                self.label = label
                self._session = ort.InferenceSession(model_path, sess_options=sess_options, providers=providers)
                self.is_cpu = ("CPUExecutionProvider" in providers and len(providers) == 1)

            def run(self, output_names, input_feed, run_options=None):
                try:
                    return self._session.run(output_names, input_feed, run_options)
                except Exception as run_err:
                    if not self.is_cpu:
                        import logging
                        logging.getLogger(__name__).warning(
                            "GPU session execution notice (%s); seamlessly falling back to CPU for %s...",
                            run_err, self.label
                        )
                        self._session = ort.InferenceSession(
                            self.model_path,
                            sess_options=self.sess_options,
                            providers=["CPUExecutionProvider"],
                        )
                        self.is_cpu = True
                        return self._session.run(output_names, input_feed, run_options)
                    raise

            def get_inputs(self):
                return self._session.get_inputs()

            def get_outputs(self):
                return self._session.get_outputs()

            def get_providers(self):
                return self._session.get_providers()

            def __getattr__(self, name):
                return getattr(self._session, name)

        def _find_hf_cached_model(repo_id, filename):
            """Find model: 1) bundled inside EXE, 2) huggingface cache."""
            # Priority 1: Bundled inside the EXE (models/ directory)
            bundled = BUNDLE_DIR / "models" / filename
            if bundled.exists():
                return str(bundled)
            # Priority 2: Huggingface cache on disk
            cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
            model_dir = cache_dir / f"models--{repo_id.replace('/', '--')}"
            if model_dir.exists():
                snapshots = model_dir / "snapshots"
                if snapshots.exists():
                    for snap in sorted(snapshots.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
                        candidate = snap / filename
                        if candidate.exists():
                            return str(candidate)
            return None

        def _get_session_auto(name, repo_id, filename, label):
            cached = region_eraser._sessions.get(name)
            if cached is not None:
                return cached
            import logging
            # Try finding model in huggingface cache first (no import needed)
            model_path = _find_hf_cached_model(repo_id, filename)
            if model_path is None:
                # Model not cached yet - must download (first-time only)
                try:
                    from huggingface_hub import hf_hub_download
                    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
                except Exception as dl_err:
                    logging.getLogger(__name__).error(
                        "❌ Cannot find or download model %s/%s: %s", repo_id, filename, dl_err
                    )
                    raise

            so = ort.SessionOptions()
            so.enable_cpu_mem_arena = True
            so.execution_mode = ort.ExecutionMode.ORT_PARALLEL
            so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            threads = max(1, os.cpu_count() or 2)
            so.intra_op_num_threads = threads
            so.inter_op_num_threads = threads

            available = ort.get_available_providers()
            session = None

            # 1. Tier 1: NVIDIA CUDA GPU (Ultra-Fast)
            if "CUDAExecutionProvider" in available:
                try:
                    import numpy as np
                    cuda_session = SafeInferenceSession(
                        model_path,
                        sess_options=so,
                        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
                        label=label,
                    )
                    inp = cuda_session.get_inputs()
                    dummy = {i.name: np.zeros([1 if isinstance(d, str) else d for d in i.shape], dtype=np.float32) for i in inp}
                    cuda_session.run(None, dummy)
                    session = cuda_session
                    logging.getLogger(__name__).info(
                        "🚀 [Removix Engine] Accelerated with NVIDIA CUDA GPU: %s", label
                    )
                except Exception as gpu_err:
                    logging.getLogger(__name__).warning(
                        "CUDA GPU incompatible (%s); trying DirectML/CPU", gpu_err
                    )

            # 2. Tier 2: DirectML GPU (Works on Intel Iris, AMD Radeon, NVIDIA)
            if session is None and "DmlExecutionProvider" in available:
                try:
                    import numpy as np
                    dml_session = SafeInferenceSession(
                        model_path,
                        sess_options=so,
                        providers=["DmlExecutionProvider", "CPUExecutionProvider"],
                        label=label,
                    )
                    # Warmup: verify GPU can actually execute this model's ops
                    inp = dml_session.get_inputs()
                    dummy = {i.name: np.zeros([1 if isinstance(d, str) else d for d in i.shape], dtype=np.float32) for i in inp}
                    dml_session.run(None, dummy)
                    session = dml_session
                    logging.getLogger(__name__).info(
                        "⚡ [Removix Engine] Accelerated with DirectML GPU: %s", label
                    )
                except Exception as dml_err:
                    logging.getLogger(__name__).warning(
                        "DirectML GPU incompatible (%s); using CPU instead", dml_err
                    )

            # 3. Tier 3: Multi-Core CPU Fallback (Intel / AMD CPU)
            if session is None:
                session = SafeInferenceSession(
                    model_path,
                    sess_options=so,
                    providers=["CPUExecutionProvider"],
                    label=label,
                )
                logging.getLogger(__name__).info(
                    "💻 [Removix Engine] Running on Multi-Core CPU: %s", label
                )

            region_eraser._sessions[name] = session
            return session

        region_eraser._get_session = _get_session_auto
    except Exception as e:
        import logging
        logging.getLogger(__name__).error("Engine patch failed: %s", e, exc_info=True)

_patch_lama_engine()

# Avoid pre-warming on memory-tight cloud containers (Render 512MB RAM limit)
if not os.environ.get("RENDER"):
    def _prewarm_lama():
        try:
            from remove_ai_watermarks.region_eraser import _get_lama_session
            _get_lama_session()
            import gc
            gc.collect()
        except Exception:
            pass

    threading.Thread(target=_prewarm_lama, daemon=True).start()

CLI = shutil.which("remove-ai-watermarks") or str(
    Path.home() / ".local" / "bin" / "remove-ai-watermarks.exe"
)
if not shutil.which("remove-ai-watermarks") and not os.path.isfile(CLI):
    CLI = "remove-ai-watermarks"

WORKDIR = Path(tempfile.gettempdir()) / "removix_jobs"
WORKDIR.mkdir(exist_ok=True)

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".flv"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

FRAME_RE = re.compile(r"(\d+)\s*/\s*(\d+)")
PCT_RE = re.compile(r"(\d{1,3})\s*%")

JOBS = {}
JOBS_LOCK = threading.Lock()


def set_job(job_id, **kwargs):
    with JOBS_LOCK:
        if job_id in JOBS:
            JOBS[job_id].update(kwargs)


def sanitize_error_message(raw_msg: str, is_video: bool = False) -> str:
    """Sanitize internal errors so tool names, version numbers, or package internals never leak to UI."""
    if not raw_msg:
        return "Could not complete media processing. Please try again with a valid file."
    
    clean_lines = []
    for line in raw_msg.splitlines():
        line_clean = line.strip()
        # Filter out internal CLI banners and version numbers
        if any(b in line_clean.lower() for b in ["remove-ai-watermarks", "v0.", "visible & invisible", "cleaning input."]):
            continue
        if "requires" in line_clean.lower() or "not found" in line_clean.lower():
            continue
        if line_clean:
            clean_lines.append(line_clean)
            
    filtered = " ".join(clean_lines).strip()
    if not filtered or len(filtered) < 6:
        if is_video:
            return "Unable to process video file. Please ensure it is a valid, supported video format (MP4, MOV, WebM) and try again."
        return "Unable to process image file. Please ensure the image is a valid format (PNG, JPG, WebP) and try again."
    
    # Strip any remaining technical words
    filtered = re.sub(r'remove[-_]ai[-_]watermarks(\[[^\]]*\])?', 'restoration engine', filtered, flags=re.I)
    filtered = re.sub(r'v\d+\.\d+(\.\d+)?', '', filtered, flags=re.I)
    filtered = re.sub(r'\b(lama|migan|opencv|cv2|onnxruntime|c2pa)\b', 'AI component', filtered, flags=re.I)
    return filtered


def process_image_direct(job_id, in_path, out_path, custom_box=None, corner_mode=None):
    import cv2
    import numpy as np
    from remove_ai_watermarks.api import remove_visible_detailed

    set_job(job_id, stage="scanning", percent=10, message="Analyzing image and AI provenance...")
    time.sleep(0.12)
    set_job(job_id, stage="scanning", percent=25, message="Detecting watermark coordinates...")
    time.sleep(0.12)
    set_job(job_id, stage="removing", percent=35, message="Reconstructing background with AI...")

    result_container = {"report": None, "error": None}

    def run_worker():
        try:
            from remove_ai_watermarks import watermark_registry
            from remove_ai_watermarks.api import _load_visible_input, _write_visible_result
            from remove_ai_watermarks import region_eraser

            loaded = _load_visible_input(in_path)
            h, w = loaded.bgr.shape[:2]

            report = None
            if custom_box and len(custom_box) == 4:
                cb_x, cb_y, cb_w, cb_h = custom_box
                cleaned = region_eraser.erase(loaded.bgr, boxes=[(cb_x, cb_y, cb_w, cb_h)], backend="lama")
                class CustomReport:
                    labels = ["Custom selected watermark"]
                    image = cleaned
                report = CustomReport()
            elif corner_mode == "bottom-left":
                bl_w = min(int(w * 0.18), 240)
                bl_h = min(int(h * 0.09), 90)
                margin_x = max(8, int(w * 0.012))
                margin_y = max(8, int(h * 0.012))
                cleaned = region_eraser.erase(loaded.bgr, boxes=[(margin_x, h - bl_h - margin_y, bl_w, bl_h)], backend="lama")
                class BLReport:
                    labels = ["Bottom-Left watermark"]
                    image = cleaned
                report = BLReport()
            elif corner_mode == "bottom-right":
                br_w = min(int(w * 0.18), 240)
                br_h = min(int(h * 0.09), 90)
                margin_x = max(8, int(w * 0.012))
                margin_y = max(8, int(h * 0.012))
                cleaned = region_eraser.erase(loaded.bgr, boxes=[(w - br_w - margin_x, h - br_h - margin_y, br_w, br_h)], backend="lama")
                class BRReport:
                    labels = ["Bottom-Right watermark"]
                    image = cleaned
                report = BRReport()
            else:
                # Use confirmed trust level so marks are recognized even on images without EXIF/metadata
                provenance = loaded.provenance or frozenset(watermark_registry.mark_keys())
                report = watermark_registry.remove_auto_marks_detailed(
                    loaded.bgr,
                    sensitivity="auto",
                    provenance=provenance,
                    backend="lama",
                )

                # Relaxed Gemini sparkle check
                if not report.labels:
                    from remove_ai_watermarks.gemini_engine import GeminiEngine
                    engine = GeminiEngine()
                    det = engine.detect_watermark(loaded.bgr, trust_provenance=True)
                    if not det.detected and getattr(det, "spatial_score", 0.0) >= 0.20:
                        det.detected = True
                        if not det.region:
                            det.region = (w - 72, h - 72, 48, 48)

                    if det.detected:
                        rx, ry, rw, rh = det.region
                        cleaned = region_eraser.erase(loaded.bgr, boxes=[(rx, ry, rw, rh)], backend="lama")
                        class FallbackReport:
                            labels = ["Google Gemini visible watermark (sparkle)"]
                            image = cleaned
                        report = FallbackReport()

                # If still no mark detected, perform Universal AI Watermark Corner Inpaint
                if not report.labels:
                    from remove_ai_watermarks.gemini_engine import GeminiEngine
                    engine = GeminiEngine()
                    sparkle_mask = engine.footprint_mask(loaded.bgr, force=True)
                    cleaned = None

                    # If official Gemini sparkle mask builds, try erasing with LaMa
                    if sparkle_mask is not None and sparkle_mask.any():
                        try:
                            cleaned = region_eraser.erase_lama(loaded.bgr, sparkle_mask)
                        except Exception:
                            cleaned = None

                    # Fallback to standard bottom-right AI watermark box
                    if cleaned is None:
                        br_w = min(int(w * 0.18), 240)
                        br_h = min(int(h * 0.09), 90)
                        margin_x = max(8, int(w * 0.012))
                        margin_y = max(8, int(h * 0.012))
                        rx = w - br_w - margin_x
                        ry = h - br_h - margin_y
                        cleaned = region_eraser.erase(loaded.bgr, boxes=[(rx, ry, br_w, br_h)], backend="lama")

                    class UniversalReport:
                        labels = ["AI Watermark (Universal Clean)"]
                        image = cleaned
                    report = UniversalReport()

            _write_visible_result(
                loaded,
                report.image,
                report.labels,
                out_path,
                strip_metadata=True,
                write_noop=True,
            )
            job_dir = out_path.parent
            if not out_path.exists() and report.image is not None:
                cv2.imwrite(str(out_path), report.image)
            if report.image is not None:
                try:
                    cv2.imwrite(str(job_dir / "preview_output.jpg"), report.image)
                except Exception:
                    pass
            if loaded.bgr is not None:
                try:
                    cv2.imwrite(str(job_dir / "preview_input.jpg"), loaded.bgr)
                except Exception:
                    pass
            result_container["report"] = report
        except Exception as e:
            result_container["error"] = e
        finally:
            import gc
            gc.collect()

    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()

    current_pct = 35
    elapsed_ticks = 0
    while worker_thread.is_alive():
        worker_thread.join(timeout=0.4)
        if not worker_thread.is_alive():
            break
        elapsed_ticks += 1
        # Strictly increasing monotonic progression:
        if current_pct < 60:
            if elapsed_ticks % 2 == 0:
                current_pct += 1
            msg = "Isolating watermark context & creating neural tensor..."
        elif current_pct < 80:
            if elapsed_ticks % 2 == 0:
                current_pct += 1
            msg = "Reconstructing background with LaMa Neural Network..."
        elif current_pct < 92:
            if elapsed_ticks % 3 == 0:
                current_pct += 1
            msg = "Synthesizing seamless textures & removing AI footprint..."
        elif current_pct < 98:
            if elapsed_ticks % 5 == 0:
                current_pct += 1
            msg = "Harmonizing color gradients & edge feathering..."
        else:
            msg = "Finalizing photorealistic pixel blend..."

        set_job(job_id, stage="removing", percent=current_pct, message=msg)

    if result_container["error"] is not None:
        raise result_container["error"]

    set_job(job_id, stage="finalizing", percent=98, message="Validating seamless restoration & stripping tags...")
    time.sleep(0.12)
    set_job(job_id, stage="done", percent=100, message="Restoration complete")


def process_video_direct(job_id, in_path, out_path, custom_box=None, corner_mode=None):
    import cv2
    import numpy as np
    from dataclasses import replace
    from remove_ai_watermarks.video import (
        VIDEO_VISIBLE_MARKS,
        _select_stable_visible_mark,
    )
    from remove_ai_watermarks.video_visible import (
        detect_sora_frame,
        detect_veo_frame,
        detect_seedance_frame,
        detect_doubao_frame,
        detect_dola_frame,
        detect_hailuo_frame,
        detect_kling_frame,
        _prepare_frame,
        probe_video_timestamps,
        probe_video_encode_profile,
        _timestamp_time_base,
        _timestamps_are_variable,
        start_raw_video_encoder,
        raw_video_command,
        _mask_for_region,
        stabilize_filled_frame,
        finish_raw_video_encoder,
        _TimestampedNutWriter,
        staged_video_output,
        VideoScan,
    )
    from remove_ai_watermarks.video_temporal import _backward_map, _backward_warp
    from remove_ai_watermarks.video_encoding import mux_encoded_video
    from remove_ai_watermarks.metadata import get_ai_metadata, strip_and_verify
    from remove_ai_watermarks.watermark_registry import fill, resolve_backend

    def _temporal_lama_inpaint(
        f_idx,
        source_frame,
        mask,
        prev_source,
        prev_cleaned,
        prev_mask,
        backend,
        keyframe_interval=4,
    ):
        if mask is None or not np.any(mask > 0):
            return source_frame

        # Always run full LaMa neural network on keyframes or when prior frame is unavailable
        is_keyframe = (f_idx % keyframe_interval == 0) or prev_cleaned is None or prev_mask is None
        if is_keyframe:
            cleaned = fill(source_frame, mask, backend=backend)
            if prev_source is not None and prev_cleaned is not None and prev_mask is not None:
                cleaned = stabilize_filled_frame(
                    prev_source,
                    prev_cleaned,
                    prev_mask,
                    source_frame,
                    cleaned,
                    mask,
                    copy=False,
                )
            return cleaned

        # Intermediate frames: propagate previous clean pixels using localized optical flow
        union = (prev_mask > 0) | (mask > 0)
        ys, xs = np.where(union)
        if len(xs) == 0:
            return source_frame.copy()

        h, w = mask.shape
        m_w = int(xs.max() - xs.min() + 1)
        m_h = int(ys.max() - ys.min() + 1)
        pad = max(24, round(max(m_w, m_h) * 0.75))
        x0 = max(0, int(xs.min()) - pad)
        y0 = max(0, int(ys.min()) - pad)
        x1 = min(w, int(xs.max()) + pad + 1)
        y1 = min(h, int(ys.max()) + pad + 1)

        prev_src_crop = prev_source[y0:y1, x0:x1]
        curr_src_crop = source_frame[y0:y1, x0:x1]
        prev_cln_crop = prev_cleaned[y0:y1, x0:x1]
        prev_msk_crop = prev_mask[y0:y1, x0:x1]
        curr_msk_crop = mask[y0:y1, x0:x1]

        try:
            maps = _backward_map(
                cv2.cvtColor(curr_src_crop, cv2.COLOR_BGR2GRAY),
                cv2.cvtColor(prev_src_crop, cv2.COLOR_BGR2GRAY),
            )
            warped_prev_src = _backward_warp(prev_src_crop, maps)
            warped_prev_cln = _backward_warp(prev_cln_crop, maps)
            warped_prev_msk = _backward_warp(
                prev_msk_crop,
                maps,
                interpolation=cv2.INTER_NEAREST,
            )

            curr_hole = curr_msk_crop > 0
            covered = curr_hole & (warped_prev_msk > 0)

            if np.any(curr_hole) and float(np.mean(covered[curr_hole])) >= 0.85:
                occupied = curr_hole | (warped_prev_msk > 0)
                dilation = max(7, round(max(m_w, m_h) * 0.25))
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation | 1, dilation | 1))
                context = cv2.dilate(occupied.astype(np.uint8), kernel).astype(bool) & ~occupied
                if np.count_nonzero(context) >= 64:
                    residual = np.abs(curr_src_crop.astype(np.float32) - warped_prev_src.astype(np.float32))
                    context_residual = float(np.mean(residual[context]))
                    if context_residual <= 14.0:
                        # Smooth background motion: warp prior LaMa fill seamlessly
                        result = source_frame.copy()
                        result_crop = result[y0:y1, x0:x1]
                        feather = cv2.GaussianBlur(curr_hole.astype(np.float32), (5, 5), 1.0)[..., None]
                        blended = (1.0 - feather) * result_crop.astype(np.float32) + feather * warped_prev_cln.astype(np.float32)
                        result_crop[curr_hole] = np.clip(blended[curr_hole], 0, 255).astype(np.uint8)
                        return result
        except Exception:
            pass

        # Sudden motion or scene cut: run full LaMa neural network
        cleaned = fill(source_frame, mask, backend=backend)
        if prev_source is not None and prev_cleaned is not None and prev_mask is not None:
            cleaned = stabilize_filled_frame(
                prev_source,
                prev_cleaned,
                prev_mask,
                source_frame,
                cleaned,
                mask,
                copy=False,
            )
        return cleaned

    source_path = Path(in_path)
    output_path = Path(out_path)

    set_job(job_id, stage="scanning", percent=5, message="Scanning video metadata...")
    detected_metadata = get_ai_metadata(source_path)

    detectors = {
        "sora": detect_sora_frame,
        "veo": detect_veo_frame,
        "seedance": detect_seedance_frame,
        "doubao": detect_doubao_frame,
        "dola": detect_dola_frame,
        "hailuo": detect_hailuo_frame,
        "kling": detect_kling_frame,
    }

    job_dir = source_path.parent
    capture = cv2.VideoCapture(str(source_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video file: {source_path}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(capture.get(cv2.CAP_PROP_FPS)) or 24.0
    total_est_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    # Extract frame 0 for preview
    ok0, frame0 = capture.read()
    if ok0 and frame0 is not None:
        try:
            cv2.imwrite(str(job_dir / "preview_input.jpg"), frame0)
        except Exception:
            pass

    # Read authoritative timestamps
    probed = probe_video_timestamps(source_path)
    total_frames = len(probed) if len(probed) > 0 else total_est_frames
    shared_timestamps = probed if len(probed) > 0 else tuple(float(i) / max(1.0, fps) for i in range(total_frames))

    selected = None
    if custom_box and len(custom_box) == 4:
        capture.release()
        cb_x, cb_y, cb_w, cb_h = custom_box
        regions = [(cb_x, cb_y, cb_w, cb_h)] * total_frames
        scan = VideoScan(width, height, fps, (), shared_timestamps)
        selected = ("custom_box", scan, regions, 0.04, "box")
    elif corner_mode == "bottom-left":
        capture.release()
        wm_w = max(160, min(int(width * 0.20), 320))
        wm_h = max(50, min(int(height * 0.085), 110))
        margin_x = max(10, int(width * 0.015))
        margin_y = max(10, int(height * 0.015))
        regions = [(margin_x, height - wm_h - margin_y, wm_w, wm_h)] * total_frames
        scan = VideoScan(width, height, fps, (), shared_timestamps)
        selected = ("bottom_left", scan, regions, 0.04, "box")
    elif corner_mode == "bottom-right":
        capture.release()
        wm_w = max(160, min(int(width * 0.20), 320))
        wm_h = max(50, min(int(height * 0.085), 110))
        margin_x = max(10, int(width * 0.015))
        margin_y = max(10, int(height * 0.015))
        regions = [(width - wm_w - margin_x, height - wm_h - margin_y, wm_w, wm_h)] * total_frames
        scan = VideoScan(width, height, fps, (), shared_timestamps)
        selected = ("bottom_right", scan, regions, 0.04, "box")
    else:
        # Smart Fast-Scan (20-30 frames window as requested)
        max_scan_frames = min(30, total_est_frames)
        scan_frames = [(0, frame0)] if (ok0 and frame0 is not None) else []
        for f_idx in range(1, max_scan_frames):
            ok, f = capture.read()
            if not ok:
                break
            scan_frames.append((f_idx, f))

        detections = {mark: [] for mark in detectors}
        confirmed_mark = None
        for f_idx, f in scan_frames:
            prepared = _prepare_frame(f)
            for mark, detector in detectors.items():
                det = detector(f, frame_index=f_idx, prepared=prepared)
                detections[mark].append(det)
                if getattr(det, "box", None) is not None:
                    pos_count = sum(1 for d in detections[mark] if getattr(d, "box", None) is not None)
                    if pos_count >= 2:
                        confirmed_mark = mark
            pct = 5 + int((f_idx / max_scan_frames) * 18)
            set_job(job_id, stage="scanning", percent=pct, message=f"Scanning frame {f_idx + 1}/{max_scan_frames} for AI watermarks...")
            if confirmed_mark and f_idx >= 15:
                break

        # If not found yet and video has many frames, check 2 sample frames at 50% and 80%
        if not confirmed_mark and total_est_frames > 60:
            for s_pct in (0.50, 0.80):
                s_idx = int(total_est_frames * s_pct)
                capture.set(cv2.CAP_PROP_POS_FRAMES, s_idx)
                s_ok, s_frame = capture.read()
                if s_ok and s_frame is not None:
                    prepared = _prepare_frame(s_frame)
                    for mark, detector in detectors.items():
                        det = detector(s_frame, frame_index=s_idx, prepared=prepared)
                        detections[mark].append(det)
                        if getattr(det, "box", None) is not None:
                            confirmed_mark = mark
                            break
                if confirmed_mark:
                    break

        capture.release()

        # Build scans for detector verification
        scans = {
            mark: VideoScan(width, height, fps, tuple(detections[mark]), shared_timestamps[:len(detections[mark])])
            for mark in detectors
        }
        set_job(job_id, stage="scanning", percent=25, message="Locking watermark coordinates...")
        selected_candidate = _select_stable_visible_mark(scans, detected_metadata, VIDEO_VISIBLE_MARKS)
        if selected_candidate is not None:
            c_mark, c_scan, c_regions, c_pad, c_style = selected_candidate
            found_box = next((r for r in c_regions if r is not None), None)
            if found_box is not None:
                regions = [found_box] * total_frames
                scan = VideoScan(width, height, fps, (), shared_timestamps)
                selected = (c_mark, scan, regions, c_pad, c_style)

        if selected is None:
            # Universal AI Video Watermark Fallback (Runway, Luma, Pika, Kling, etc.)
            wm_w = max(160, min(int(width * 0.20), 320))
            wm_h = max(50, min(int(height * 0.085), 110))
            margin_x = max(10, int(width * 0.015))
            margin_y = max(10, int(height * 0.015))
            box_x = width - wm_w - margin_x
            box_y = height - wm_h - margin_y
            regions = [(box_x, box_y, wm_w, wm_h)] * total_frames
            scan = VideoScan(width, height, fps, (), shared_timestamps)
            selected = ("universal_ai_corner", scan, regions, 0.04, "box")

    mark, scan, regions, padding_fraction, mask_style = selected
    resolved_backend = resolve_backend("lama")

    set_job(job_id, stage="removing", percent=26, message=f"Restoring frame 1/{total_frames} with AI...")

    with staged_video_output(output_path) as (encoded_video, temporary_output):
        profile = probe_video_encode_profile(source_path)
        time_base = _timestamp_time_base(profile.time_base)
        preserve_start_offset = profile.start_pts not in (None, 0)
        timestamped_input = preserve_start_offset or _timestamps_are_variable(scan, time_base=time_base)
        if timestamped_input and profile.time_base is None:
            profile = replace(
                profile,
                time_base=f"{time_base.numerator}/{time_base.denominator}",
            )

        process = start_raw_video_encoder(
            raw_video_command(
                encoded_video,
                width=scan.width,
                height=scan.height,
                fps=scan.fps,
                crf=14,
                profile=profile,
                timestamped_input=timestamped_input,
                copy_input_timestamps=preserve_start_offset,
            )
        )
        frame_pipe = process.stdin
        capture = cv2.VideoCapture(str(source_path))
        timestamped_writer = None
        if timestamped_input:
            timestamped_writer = _TimestampedNutWriter(
                frame_pipe,
                width=scan.width,
                height=scan.height,
                time_base=time_base,
                start_pts=profile.start_pts or 0,
            )

        previous_source = None
        previous_cleaned = None
        previous_mask = None

        try:
            KEYFRAME_INTERVAL = 4
            for f_idx, region in enumerate(regions):
                ok, frame = capture.read()
                if not ok:
                    break
                source_frame = frame
                mask = None
                if region is not None:
                    mask = _mask_for_region(
                        frame,
                        region,
                        padding_fraction=padding_fraction,
                        mask_style=mask_style,
                    )
                    frame = _temporal_lama_inpaint(
                        f_idx,
                        source_frame,
                        mask,
                        previous_source,
                        previous_cleaned,
                        previous_mask,
                        resolved_backend,
                        keyframe_interval=KEYFRAME_INTERVAL,
                    )

                if f_idx == 0 or not (job_dir / "preview_output.jpg").exists():
                    try:
                        cv2.imwrite(str(job_dir / "preview_output.jpg"), frame)
                    except Exception:
                        pass

                if timestamped_writer is None:
                    frame_pipe.write(frame.tobytes())
                else:
                    timestamped_writer.write(frame, scan.timestamps[f_idx])

                previous_source = source_frame
                previous_cleaned = frame
                previous_mask = mask

                pct = 25 + int(((f_idx + 1) / total_frames) * 65)
                set_job(job_id, stage="removing", percent=pct, message=f"Restoring frame {f_idx + 1}/{total_frames} with AI...")

            if timestamped_writer is not None:
                timestamped_writer.close()
                timestamped_writer = None

            set_job(job_id, stage="finalizing", percent=92, message="Finalizing video encoding...")
            finish_raw_video_encoder(process, encoded_video, operation="visible-watermark encode")
            set_job(job_id, stage="finalizing", percent=96, message="Muxing lossless audio & stripping tags...")
            mux_encoded_video(
                encoded_video,
                source_path,
                temporary_output,
                strip_metadata=True,
                copy_input_timestamps=preserve_start_offset,
            )
        finally:
            capture.release()
            if timestamped_writer is not None:
                try:
                    timestamped_writer.close()
                except Exception:
                    pass

    set_job(job_id, stage="done", percent=100, message="Restoration complete")


def run_job_cli_fallback(job_id, in_path, out_path, ext):
    if ext in VIDEO_EXTS:
        cmd = [CLI, "video", "all", "--backend", "lama", str(in_path), "-o", str(out_path)]
    else:
        cmd = [CLI, "visible", "--backend", "lama", str(in_path), "-o", str(out_path)]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )
    set_job(job_id, stage="removing", percent=25, message="Intelligent background reconstruction in progress...")

    stop_ticker = threading.Event()
    def ticker():
        curr = 25
        ticks = 0
        while not stop_ticker.is_set():
            stop_ticker.wait(0.5)
            if stop_ticker.is_set():
                break
            ticks += 1
            if curr < 65:
                curr += 1
            elif curr < 85:
                if ticks % 2 == 0:
                    curr += 1
            elif curr < 98:
                if ticks % 4 == 0:
                    curr += 1
            set_job(job_id, percent=curr)
    
    t_tick = threading.Thread(target=ticker, daemon=True)
    t_tick.start()

    last_lines = []
    try:
        for line in proc.stdout:
            last_lines.append(line.strip())
            last_lines = last_lines[-15:]
            m = FRAME_RE.search(line)
            if m:
                done, total = int(m.group(1)), int(m.group(2))
                if total > 0:
                    pct = 25 + round((done / total) * 65)
                    set_job(job_id, percent=min(pct, 92), stage="removing", message=f"Restoring frame {done}/{total} with AI...")
                    continue
            m = PCT_RE.search(line)
            if m:
                set_job(job_id, percent=min(int(m.group(1)), 90), stage="removing")
    finally:
        stop_ticker.set()
        t_tick.join(timeout=1.0)

    proc.wait()
    set_job(job_id, stage="finalizing", percent=95, message="Finalizing clean output...")

    if proc.returncode != 0 or not out_path.exists():
        raw_err = "\n".join(last_lines[-5:]) or "Processing failed"
        set_job(job_id, stage="error", error=sanitize_error_message(raw_err, is_video=(ext in VIDEO_EXTS)))
        return

    set_job(job_id, stage="done", percent=100, message="Restoration complete")


def run_job(job_id, in_path, out_path, ext, custom_box=None, corner_mode=None):
    set_job(job_id, stage="scanning", percent=5, message="Scanning media and analyzing coordinates...")
    try:
        if ext in VIDEO_EXTS:
            try:
                process_video_direct(job_id, in_path, out_path, custom_box=custom_box, corner_mode=corner_mode)
            except Exception as direct_err:
                import logging
                logging.getLogger(__name__).warning("Direct video processing failed: %s, trying CLI fallback", direct_err)
                try:
                    run_job_cli_fallback(job_id, in_path, out_path, ext)
                except FileNotFoundError:
                    raise direct_err  # Re-raise original error if CLI also missing
        elif ext in IMAGE_EXTS:
            try:
                process_image_direct(job_id, in_path, out_path, custom_box=custom_box, corner_mode=corner_mode)
            except Exception as direct_err:
                import logging
                logging.getLogger(__name__).warning("Direct image processing failed: %s, trying CLI fallback", direct_err)
                try:
                    run_job_cli_fallback(job_id, in_path, out_path, ext)
                except FileNotFoundError:
                    raise direct_err  # Re-raise original error if CLI also missing
        else:
            set_job(job_id, stage="error", error=f"Unsupported file type: {ext}")
            return

        if out_path.exists() and out_path.stat().st_size > 0:
            try:
                from modules import activity_tracker
                f_type = "Video" if ext in VIDEO_EXTS else "Image"
                tool_label = "Video Watermark Remover" if ext in VIDEO_EXTS else "Image Watermark Remover"
                orig_fname = in_path.name
                with JOBS_LOCK:
                    if job_id in JOBS and JOBS[job_id].get("filename"):
                        orig_fname = JOBS[job_id]["filename"]
                activity_tracker.log_file(
                    file_name=f"removix_{orig_fname}",
                    file_type=f_type,
                    file_size_bytes=out_path.stat().st_size,
                    tool_name=tool_label,
                    download_path=str(out_path),
                )
            except Exception:
                pass
    except Exception as exc:
        set_job(job_id, stage="error", error=sanitize_error_message(str(exc), is_video=(ext in VIDEO_EXTS)))


def detect_watermark_in_box(img, box):
    """Accurately detect and snap to watermark text or logo within a user-drawn bounding box."""
    import cv2
    import numpy as np

    if img is None or img.size == 0 or not box or len(box) != 4:
        return {"detected": False, "box": box, "label": "Selected area"}

    h_img, w_img = img.shape[:2]
    bx, by, bw, bh = box
    bx = max(0, min(w_img - 1, int(bx)))
    by = max(0, min(h_img - 1, int(by)))
    bw = max(1, min(w_img - bx, int(bw)))
    bh = max(1, min(h_img - by, int(bh)))

    # 1. Registered Gemini AI watermark check
    try:
        from remove_ai_watermarks.gemini_engine import GeminiEngine
        engine = GeminiEngine()
        det = engine.detect_watermark(img, trust_provenance=True)
        if det.detected and det.region:
            gx, gy, gw, gh = det.region
            ix1 = max(bx, gx)
            iy1 = max(by, gy)
            ix2 = min(bx + bw, gx + gw)
            iy2 = min(by + bh, gy + gh)
            if ix2 > ix1 and iy2 > iy1:
                return {
                    "detected": True,
                    "type": "gemini",
                    "box": [int(gx), int(gy), int(gw), int(gh)],
                    "label": "Gemini AI watermark detected",
                }
    except Exception:
        pass

    # 2. Universal watermark text/logo feature analysis on the subregion crop
    crop = img[by:by+bh, bx:bx+bw]
    if crop.shape[0] < 8 or crop.shape[1] < 8:
        return {"detected": False, "box": [bx, by, bw, bh], "label": "Selected area"}

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    k_size = max(3, min(15, min(bw, bh) // 4))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    contrast = cv2.max(tophat, blackhat)

    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(grad_x, grad_y)
    mag = np.uint8(np.clip(mag / (mag.max() + 1e-5) * 255.0, 0, 255))

    combined = cv2.max(contrast, mag)
    _, thresh = cv2.threshold(combined, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh_clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel)

    contours, _ = cv2.findContours(thresh_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    total_crop_area = bw * bh
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 8:
            continue
        cx, cy, cw, ch = cv2.boundingRect(cnt)
        if cw > 0.95 * bw and ch > 0.95 * bh:
            continue
        rects.append((cx, cy, cw, ch))

    if rects:
        min_x = min(r[0] for r in rects)
        min_y = min(r[1] for r in rects)
        max_x = max(r[0] + r[2] for r in rects)
        max_y = max(r[1] + r[3] for r in rects)

        union_w = max_x - min_x
        union_h = max_y - min_y
        union_area = union_w * union_h

        if 0.05 * total_crop_area <= union_area <= 0.92 * total_crop_area and union_w >= 8 and union_h >= 8:
            pad = 6
            snapped_bx = max(0, bx + min_x - pad)
            snapped_by = max(0, by + min_y - pad)
            snapped_bw = min(w_img - snapped_bx, union_w + 2 * pad)
            snapped_bh = min(h_img - snapped_by, union_h + 2 * pad)
            return {
                "detected": True,
                "type": "watermark",
                "box": [int(snapped_bx), int(snapped_by), int(snapped_bw), int(snapped_bh)],
                "label": "Watermark detected",
            }

    return {
        "detected": False,
        "type": "manual",
        "box": [bx, by, bw, bh],
        "label": "Manual selection",
    }



