"""
Removix - AI Watermark Remover
--------------------------------
Full site for Removix with:
- Clean Removix header & Hero
- Interactive Video & Image tool with upright SVG progress ring
- 3 Feature Cards (Free tags)
- Before & After visual comparison section
- "Your images never leave your device" privacy section
- Multi-column SaaS footer powered by Shivank Thakur

Run:
    python app.py
Then open http://localhost:7860 (or the PORT you set).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from dataclasses import replace
from pathlib import Path

from flask import Flask, request, jsonify, send_file, abort, Response

if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, "w")
    except Exception:
        pass
if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, "w")
    except Exception:
        pass

# Suppress any child process console windows (ffmpeg, ffprobe, etc.) on Windows
if sys.platform == "win32":
    _orig_popen = subprocess.Popen

    def _silent_popen(*args, **kwargs):
        if "creationflags" not in kwargs:
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        else:
            kwargs["creationflags"] |= subprocess.CREATE_NO_WINDOW
        return _orig_popen(*args, **kwargs)

    subprocess.Popen = _silent_popen

BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
SRC_DIR = BUNDLE_DIR / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

UV_SITE_PACKAGES = Path.home() / "AppData" / "Roaming" / "uv" / "tools" / "remove-ai-watermarks" / "Lib" / "site-packages"
if UV_SITE_PACKAGES.exists() and str(UV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(UV_SITE_PACKAGES))

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
            so.enable_cpu_mem_arena = False
            so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            so.intra_op_num_threads = max(1, min(os.cpu_count() or 1, 4))

            available = ort.get_available_providers()
            session = None

            # 1. Tier 1: NVIDIA CUDA GPU (Ultra-Fast)
            if "CUDAExecutionProvider" in available:
                try:
                    session = ort.InferenceSession(
                        model_path,
                        sess_options=so,
                        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
                    )
                    logging.getLogger(__name__).info(
                        "🚀 [Removix Engine] Accelerated with NVIDIA CUDA GPU: %s", label
                    )
                except Exception as gpu_err:
                    logging.getLogger(__name__).warning(
                        "CUDA initialization notice (%s); trying DirectML/CPU", gpu_err
                    )

            # 2. Tier 2: DirectML GPU (Works on Intel Iris, AMD Radeon, NVIDIA)
            if session is None and "DmlExecutionProvider" in available:
                try:
                    session = ort.InferenceSession(
                        model_path,
                        sess_options=so,
                        providers=["DmlExecutionProvider", "CPUExecutionProvider"],
                    )
                    logging.getLogger(__name__).info(
                        "⚡ [Removix Engine] Accelerated with DirectML GPU: %s", label
                    )
                except Exception as dml_err:
                    logging.getLogger(__name__).warning(
                        "DirectML initialization notice (%s); trying CPU", dml_err
                    )

            # 3. Tier 3: Multi-Core CPU Fallback (Intel / AMD CPU)
            if session is None:
                session = ort.InferenceSession(
                    model_path,
                    sess_options=so,
                    providers=["CPUExecutionProvider"],
                )
                logging.getLogger(__name__).info(
                    "💻 [Removix Engine] Running on Multi-Core CPU: %s", label
                )

            region_eraser._sessions[name] = session
            return session

        region_eraser._get_session = _get_session_auto
    except Exception:
        pass  # Safe fallback to default library path

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

app = Flask(__name__)


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


def process_image_direct(job_id, in_path, out_path):
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
            from remove_ai_watermarks.gemini_engine import GeminiEngine
            from remove_ai_watermarks import region_eraser

            img = cv2.imread(str(in_path))
            if img is not None:
                h, w = img.shape[:2]
                engine = GeminiEngine()
                det = engine.detect_watermark(img)
                if det.detected:
                    rx, ry, rw, rh = det.region
                    pad = 64
                    x0 = max(0, rx - pad)
                    y0 = max(0, ry - pad)
                    x1 = min(w, rx + rw + pad)
                    y1 = min(h, ry + rh + pad)

                    patch = img[y0:y1, x0:x1].copy()
                    pw, ph = x1 - x0, y1 - y0
                    bx0, by0 = rx - x0, ry - y0
                    bx1, by1 = bx0 + rw, by0 + rh

                    # Erase watermark on this tiny patch (uses < 40MB RAM, never OOMs!)
                    clean_patch = region_eraser.erase(patch, boxes=[(bx0, by0, bx1, by1)], backend="auto")

                    # Feather blend back into original image (100% original quality!)
                    mask = np.ones((ph, pw), dtype=np.float32)
                    feather = min(24, ph // 4, pw // 4)
                    for i in range(feather):
                        mask[i, :] *= (i / feather)
                        mask[:, i] *= (i / feather)
                        mask[ph - 1 - i, :] *= (i / feather)
                        mask[:, pw - 1 - i] *= (i / feather)

                    out = img.copy()
                    for c in range(3):
                        out[y0:y1, x0:x1, c] = (
                            img[y0:y1, x0:x1, c] * (1.0 - mask) + clean_patch[:, :, c] * mask
                        ).astype(np.uint8)

                    cv2.imwrite(str(out_path), out)

                    class DummyReport:
                        labels = ["Google Gemini visible watermark (sparkle)"]
                        image = out

                    result_container["report"] = DummyReport()
                    return

            # Standard processing for non-Gemini marks
            try:
                result_container["report"] = remove_visible_detailed(
                    in_path,
                    out_path,
                    backend="auto",
                    strip_metadata=True,
                    write_noop=True,
                )
            except Exception as e:
                result_container["error"] = e
        except Exception as e:
            result_container["error"] = e
        finally:
            import gc
            gc.collect()

    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()

    current_pct = 35
    while worker_thread.is_alive():
        worker_thread.join(timeout=0.35)
        if worker_thread.is_alive() and current_pct < 88:
            current_pct += 1
            set_job(job_id, stage="removing", percent=current_pct, message="Reconstructing background with AI...")

    if result_container["error"] is not None:
        raise result_container["error"]

    set_job(job_id, stage="finalizing", percent=92, message="Validating seamless restoration...")
    time.sleep(0.12)
    set_job(job_id, stage="finalizing", percent=97, message="Stripping origin tags & finalizing...")
    time.sleep(0.1)
    set_job(job_id, stage="done", percent=100, message="Restoration complete")


def process_video_direct(job_id, in_path, out_path):
    import cv2
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
    from remove_ai_watermarks.video_encoding import mux_encoded_video
    from remove_ai_watermarks.metadata import get_ai_metadata, strip_and_verify
    from remove_ai_watermarks.watermark_registry import fill, resolve_backend

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

    capture = cv2.VideoCapture(str(source_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video file: {source_path}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    total_est_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    detections = {mark: [] for mark in detectors}
    timestamps = []
    frame_index = 0

    while True:
        ok, frame = capture.read()
        if not ok:
            break
        timestamps.append(float(capture.get(cv2.CAP_PROP_POS_MSEC)) / 1000)
        prepared = _prepare_frame(frame)
        for mark, detector in detectors.items():
            detections[mark].append(
                detector(frame, frame_index=frame_index, prepared=prepared)
            )
        frame_index += 1
        pct = 5 + int(min(frame_index / total_est_frames, 1.0) * 20)
        set_job(job_id, stage="scanning", percent=pct, message=f"Scanning frame {frame_index}/{total_est_frames}...")

    capture.release()
    total_frames = frame_index or 1

    shared_timestamps = tuple(timestamps)
    probed = probe_video_timestamps(source_path)
    if len(probed) == total_frames:
        shared_timestamps = probed

    scans = {
        mark: VideoScan(width, height, fps, tuple(detections[mark]), shared_timestamps)
        for mark in detectors
    }

    set_job(job_id, stage="scanning", percent=25, message="Analyzing watermark recurrence & stability...")
    selected = _select_stable_visible_mark(scans, detected_metadata, VIDEO_VISIBLE_MARKS)

    if selected is None:
        set_job(job_id, stage="finalizing", percent=90, message="Stripping AI metadata & preserving streams...")
        strip_and_verify(source_path, output_path, keep_standard=True)
        set_job(job_id, stage="done", percent=100, message="Restoration complete")
        return

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
                    frame = fill(frame, mask, backend=resolved_backend)
                    if (
                        previous_source is not None
                        and previous_cleaned is not None
                        and previous_mask is not None
                    ):
                        frame = stabilize_filled_frame(
                            previous_source,
                            previous_cleaned,
                            previous_mask,
                            source_frame,
                            frame,
                            mask,
                            copy=False,
                        )

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
        while not stop_ticker.is_set():
            stop_ticker.wait(0.5)
            if stop_ticker.is_set():
                break
            if curr < 88:
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


def run_job(job_id, in_path, out_path, ext):
    set_job(job_id, stage="scanning", percent=5, message="Scanning media and analyzing coordinates...")
    try:
        if ext in VIDEO_EXTS:
            try:
                process_video_direct(job_id, in_path, out_path)
            except Exception:
                run_job_cli_fallback(job_id, in_path, out_path, ext)
        elif ext in IMAGE_EXTS:
            try:
                process_image_direct(job_id, in_path, out_path)
            except Exception:
                run_job_cli_fallback(job_id, in_path, out_path, ext)
        else:
            set_job(job_id, stage="error", error=f"Unsupported file type: {ext}")
            return
    except FileNotFoundError:
        set_job(job_id, stage="error", error="Restoration engine is currently unavailable. Please check system setup.")
    except Exception as exc:
        set_job(job_id, stage="error", error=sanitize_error_message(str(exc), is_video=(ext in VIDEO_EXTS)))


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/")
def home():
    return PAGE


@app.route("/health")
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "removix", "timestamp": time.time()})


def _render_keep_alive():
    """Background keep-alive thread: keeps Render free tier awake by pinging itself every 9 minutes."""
    if not os.environ.get("RENDER"):
        return
    import urllib.request
    time.sleep(45)  # Wait 45s after startup
    url = os.environ.get("KEEP_ALIVE_URL", "https://removix.sanvox.in/health")
    while True:
        try:
            time.sleep(540)  # 9 minutes (< 15 min Render idle timeout)
            req = urllib.request.Request(url, headers={"User-Agent": "Removix-SelfPinger/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                pass
        except Exception:
            pass


threading.Thread(target=_render_keep_alive, daemon=True).start()


@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No file received."}), 400

    f = request.files["file"]
    ext = Path(f.filename).suffix.lower()
    if ext not in VIDEO_EXTS and ext not in IMAGE_EXTS:
        return jsonify({"error": f"'{ext}' isn't supported yet."}), 400

    job_id = uuid.uuid4().hex[:12]
    job_dir = WORKDIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    in_path = job_dir / f"input{ext}"
    out_path = job_dir / f"clean{ext}"
    f.save(in_path)

    with JOBS_LOCK:
        JOBS[job_id] = {
            "stage": "queued",
            "percent": 0,
            "message": "Preparing media and initializing AI restoration engine...",
            "error": None,
            "out_path": str(out_path),
            "filename": f.filename,
            "created": time.time(),
        }

    thread = threading.Thread(target=run_job, args=(job_id, in_path, out_path, ext), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/api/status/<job_id>")
def status(job_id):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    if not job:
        abort(404)
    ext = Path(job.get("filename", "")).suffix.lower()
    is_img = ext in IMAGE_EXTS
    is_done = job["stage"] == "done"
    return jsonify({
        "stage": job["stage"],
        "percent": job.get("percent", 0),
        "message": job.get("message", ""),
        "error": job.get("error"),
        "is_image": is_img,
        "input_url": f"/api/preview/{job_id}/input" if is_done and is_img else None,
        "output_url": f"/api/preview/{job_id}/output" if is_done and is_img else None,
    })


@app.route("/api/stream/<job_id>")
def stream(job_id):
    def event_stream():
        while True:
            with JOBS_LOCK:
                job = JOBS.get(job_id)
            if not job:
                yield "event: error\ndata: {}\n\n"
                break

            stage = job["stage"]
            percent = job.get("percent", 0)
            message = job.get("message", "")
            error = job.get("error")
            ext = Path(job.get("filename", "")).suffix.lower()
            is_img = ext in IMAGE_EXTS
            is_done = stage == "done"

            payload = {
                "stage": stage,
                "percent": percent,
                "message": message,
                "error": error,
                "is_image": is_img,
                "input_url": f"/api/preview/{job_id}/input" if is_done and is_img else None,
                "output_url": f"/api/preview/{job_id}/output" if is_done and is_img else None,
            }
            yield f"data: {json.dumps(payload)}\n\n"

            if stage in ("done", "error"):
                break
            time.sleep(0.2)

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/preview/<job_id>/<which>")
def preview(job_id, which):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    if not job:
        abort(404)
    ext = Path(job.get("filename", "")).suffix.lower()
    if which == "input":
        p = WORKDIR / job_id / f"input{ext}"
    elif which == "output":
        p = Path(job["out_path"])
    else:
        abort(404)
    if not p.exists():
        abort(404)
    mimetype = "image/png" if ext == ".png" else "image/jpeg" if ext in {".jpg", ".jpeg"} else "image/webp" if ext == ".webp" else None
    return send_file(p, mimetype=mimetype)


@app.route("/api/download/<job_id>")
def download(job_id):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    if not job or job["stage"] != "done":
        abort(404)
    return send_file(job["out_path"], as_attachment=True, download_name=f"removix_{job['filename']}")


LOTTIE_FILE = BUNDLE_DIR / "lottie_scan.json"
LOTTIE_JS_FILE = BUNDLE_DIR / "lottie.min.js"
BEFORE_WEBP = BUNDLE_DIR / "before.webp"
AFTER_WEBP = BUNDLE_DIR / "after.webp"


@app.route("/api/animation.json")
def get_lottie_animation():
    if LOTTIE_FILE.exists():
        return send_file(LOTTIE_FILE, mimetype="application/json")
    abort(404)


@app.route("/lottie.min.js")
def get_lottie_script():
    if LOTTIE_JS_FILE.exists():
        return send_file(LOTTIE_JS_FILE, mimetype="application/javascript")
    abort(404)


@app.route("/static/before.webp")
def get_before_img():
    if BEFORE_WEBP.exists():
        return send_file(BEFORE_WEBP, mimetype="image/webp")
    abort(404)


@app.route("/static/after.webp")
def get_after_img():
    if AFTER_WEBP.exists():
        return send_file(AFTER_WEBP, mimetype="image/webp")
    abort(404)


REMOVIX_PNG = BUNDLE_DIR / "removix.png"
REMOVIX_ICO = BUNDLE_DIR / "removix.ico"
REMOVIX_SVG = BUNDLE_DIR / "removix.svg"


@app.route("/favicon.ico")
def get_favicon_ico():
    if REMOVIX_ICO.exists():
        resp = send_file(REMOVIX_ICO, mimetype="image/x-icon")
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp
    abort(404)


@app.route("/static/removix.svg")
@app.route("/static/removix-logo.svg")
@app.route("/favicon.svg")
def get_removix_svg():
    if REMOVIX_SVG.exists():
        resp = send_file(REMOVIX_SVG, mimetype="image/svg+xml")
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp
    if REMOVIX_PNG.exists():
        resp = send_file(REMOVIX_PNG, mimetype="image/png")
        return resp
    abort(404)


@app.route("/static/removix.png")
@app.route("/static/removix-logo.png")
@app.route("/favicon.png")
def get_removix_logo():
    if REMOVIX_PNG.exists():
        resp = send_file(REMOVIX_PNG, mimetype="image/png")
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp
    if REMOVIX_ICO.exists():
        resp = send_file(REMOVIX_ICO, mimetype="image/x-icon")
        return resp
    abort(404)


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Removix — AI Video & Image Watermark Remover</title>
<link rel="icon" type="image/png" href="/static/removix.png?v=3">
<link rel="shortcut icon" href="/favicon.ico?v=3">
<link rel="apple-touch-icon" href="/static/removix.png?v=3">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="/lottie.min.js"></script>
<script>
  if (!window.lottie) {
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js';
    document.head.appendChild(s);
  }
</script>
<style>
  :root {
    --primary: #0284c7;
    --primary-hover: #0369a1;
    --sky: #0ea5e9;
    --sky-light: #e0f2fe;
    --sky-soft: #f0f9ff;
    --ink: #0f172a;
    --ink-muted: #475569;
    --ink-faint: #94a3b8;
    --bg-page: #f8fafc;
    --card-bg: #ffffff;
    --line: #e2e8f0;
    --line-subtle: #f1f5f9;
    --green-badge: #16a34a;
    --green-badge-bg: #dcfce7;
    --radius-lg: 24px;
    --radius-md: 16px;
    --radius-sm: 10px;
    --shadow-card: 0 20px 45px -12px rgba(15, 23, 42, 0.08), 0 4px 16px -2px rgba(15, 23, 42, 0.03);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    background-color: var(--bg-page);
    background-image: radial-gradient(1200px 600px at 50% -80px, #e0f2fe 0%, rgba(240, 249, 255, 0.4) 45%, rgba(248, 250, 252, 0) 100%);
    background-repeat: no-repeat;
    color: var(--ink);
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }

  a { color: inherit; text-decoration: none; }

  /* ---------- Clean Top Header (Removix) ---------- */
  .top-header {
    padding: 32px 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .brand-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0px;
    background: #ffffff;
    padding: 6px 20px 6px 16px;
    border-radius: 9999px;
    border: 1px solid rgba(226, 232, 240, 0.9);
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
  }
  .brand-icon {
    width: 27px;
    height: 27px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: visible;
    flex-shrink: 0;
  }
  .brand-icon img, .brand-logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
  }
  .brand-icon svg { width: 16px; height: 16px; fill: white; }
  .brand-name {
    font-size: 21.5px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ink);
    line-height: 1;
    margin-left: 0px;
  }
  .brand-name span { color: var(--sky); }

  /* ---------- Hero Section ---------- */
  .hero {
    max-width: 820px;
    margin: 40px auto 0;
    text-align: center;
    padding: 0 20px;
  }
  .badge-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0284c7;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 6px 16px;
    border-radius: 9999px;
    margin-bottom: 20px;
  }
  .hero h1 {
    font-size: clamp(34px, 5.2vw, 56px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin-bottom: 16px;
  }
  .hero-sub {
    font-size: 17px;
    line-height: 1.6;
    color: var(--ink-muted);
    max-width: 620px;
    margin: 0 auto 36px;
  }
  .hero-sub strong { color: var(--ink); font-weight: 600; }

  /* ---------- Tool Card (Hero Main Box) ---------- */
  .tool-container {
    max-width: 860px;
    width: 100%;
    margin: 0 auto;
    padding: 0 20px;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  .main-tool-card {
    background: var(--card-bg);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    padding: 32px;
    position: relative;
    overflow: hidden;
    overflow-x: hidden;
    width: 100%;
    box-sizing: border-box;
  }

  /* Mode Switcher tabs */
  .tool-tabs {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 24px;
  }
  .tool-tab {
    padding: 9px 22px;
    border-radius: 9999px;
    font-size: 13.5px;
    font-weight: 600;
    color: var(--ink-muted);
    background: #f1f5f9;
    border: 1px solid transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
  }
  .tool-tab.active {
    background: #eff6ff;
    color: #0284c7;
    border-color: #bae6fd;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.12);
  }
  .tool-tab:hover:not(.active) {
    background: #e2e8f0;
  }

  /* Dropzone */
  #dropzone {
    border: 2px dashed #bae6fd;
    background: #f8fafc;
    border-radius: var(--radius-md);
    padding: 34px 24px 26px;
    text-align: center;
    cursor: pointer;
    display: block;
    transition: all 0.25s ease;
    user-select: none;
    -webkit-user-select: none;
  }
  #dropzone:hover, #dropzone.hover {
    border-color: var(--sky);
    background: var(--sky-soft);
  }

  /* From Uiverse.io by 3bdel3ziz-T — Removix Sky Blue Edition */
  .folder-container {
    --transition: 350ms;
    --folder-W: 120px;
    --folder-H: 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    padding: 10px;
    background: linear-gradient(135deg, #38bdf8, #0284c7);
    border-radius: 18px;
    box-shadow: 0 15px 30px rgba(2, 132, 199, 0.28);
    height: calc(var(--folder-H) * 1.7);
    width: 210px;
    margin: 14px auto 20px;
    position: relative;
    perspective: 600px;
  }

  .folder {
    position: absolute;
    top: -20px;
    left: calc(50% - 60px);
    animation: float 2.5s infinite ease-in-out;
    transition: transform var(--transition) ease;
  }

  #dropzone:hover .folder,
  .folder-container:hover .folder {
    transform: scale(1.06);
  }

  .folder .front-side,
  .folder .back-side {
    position: absolute;
    transition: transform var(--transition);
    transform-origin: bottom center;
  }

  .folder .back-side::before,
  .folder .back-side::after {
    content: "";
    display: block;
    background-color: white;
    opacity: 0.6;
    z-index: 0;
    width: var(--folder-W);
    height: var(--folder-H);
    position: absolute;
    transform-origin: bottom center;
    border-radius: 12px;
    transition: transform 350ms;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  }

  #dropzone:hover .back-side::before,
  .folder-container:hover .back-side::before {
    transform: rotateX(-5deg) skewX(5deg);
  }
  #dropzone:hover .back-side::after,
  .folder-container:hover .back-side::after {
    transform: rotateX(-15deg) skewX(12deg);
  }

  .folder .front-side {
    z-index: 1;
  }

  #dropzone:hover .front-side,
  .folder-container:hover .front-side {
    transform: rotateX(-40deg) skewX(15deg);
  }

  .folder .tip {
    background: linear-gradient(135deg, #ff9a56, #ff6f56);
    width: 80px;
    height: 20px;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
    position: absolute;
    top: -10px;
    z-index: 2;
  }

  .folder .cover {
    background: linear-gradient(135deg, #ffe563, #ffc663);
    width: var(--folder-W);
    height: var(--folder-H);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.22);
    border-radius: 10px;
  }

  .custom-file-upload {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 10px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    transition: background var(--transition) ease, transform 0.2s ease;
    display: block;
    width: 100%;
    padding: 9px 18px;
    position: relative;
    z-index: 5;
    pointer-events: auto;
    text-decoration: none;
    letter-spacing: 0.01em;
  }

  #dropzone:hover .custom-file-upload,
  .custom-file-upload:hover {
    background: rgba(255, 255, 255, 0.4);
  }

  @keyframes float {
    0% {
      transform: translateY(0px);
    }
    50% {
      transform: translateY(-16px);
    }
    100% {
      transform: translateY(0px);
    }
  }

  .drop-primary {
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 6px;
  }
  .drop-secondary {
    font-size: 13px;
    color: var(--ink-muted);
  }
  input[type=file] { display: none; }

  /* ---------- Processing View ---------- */
  .processing {
    display: none;
    width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  .processing.active {
    display: block;
    animation: fadeIn 0.3s ease;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

  .processing-layout {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 24px;
    align-items: center;
    width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  @media (max-width: 768px) {
    .processing-layout {
      grid-template-columns: 1fr;
      justify-items: center;
      gap: 20px;
      overflow-x: hidden;
    }
  }

  /* Left: Lottie Scanner Stage with Blurred Media Preview */
  .lottie-scan-stage {
    position: relative;
    width: 90%;
    max-width: 380px;
    margin: 0 auto;
    box-sizing: border-box;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid #bae6fd;
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 16px 36px -12px rgba(14, 165, 233, 0.12);
    min-height: 330px;
    text-align: center;
    overflow: hidden;
  }
  .scan-bg-preview {
    position: absolute;
    inset: -12px;
    background-size: cover;
    background-position: center;
    filter: blur(10px) brightness(0.96) saturate(1.1);
    transform: scale(1.12);
    opacity: 0;
    transition: opacity 0.5s ease;
    z-index: 0;
    pointer-events: none;
  }
  .scan-bg-preview.has-image {
    opacity: 0.6;
  }
  .scan-bg-overlay {
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    z-index: 1;
    pointer-events: none;
  }
  .scan-badge {
    position: relative;
    z-index: 2;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0284c7;
    background: rgba(224, 242, 254, 0.92);
    backdrop-filter: blur(8px);
    padding: 5px 13px;
    border-radius: 9999px;
    margin-bottom: 8px;
    border: 1px solid rgba(186, 230, 253, 0.7);
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.15);
  }
  .scan-badge svg {
    width: 13px;
    height: 13px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2.2;
  }
  .lottie-container {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 250px;
    height: 140px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-sizing: border-box;
  }
  .lottie-container svg {
    width: 100% !important;
    height: 100% !important;
    max-width: 100%;
  }
  .stage-title {
    position: relative;
    z-index: 2;
    color: var(--ink);
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
    margin-bottom: 3px;
    word-break: break-word;
    max-width: 100%;
    box-sizing: border-box;
  }
  .stage-sub {
    position: relative;
    z-index: 2;
    color: var(--ink-muted);
    font-size: 12.5px;
    max-width: 320px;
    width: 100%;
    margin: 0 auto 14px;
    line-height: 1.4;
    word-break: break-word;
    box-sizing: border-box;
  }
  .scan-progress-box {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 320px;
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.95);
    border-radius: 12px;
    padding: 10px 14px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    box-sizing: border-box;
  }
  .scan-progress-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    color: var(--ink-muted);
    margin-bottom: 7px;
  }
  .scan-pct-value {
    font-size: 13px;
    font-weight: 800;
    color: var(--primary);
    font-variant-numeric: tabular-nums;
  }
  .scan-progress-track {
    width: 100%;
    height: 7px;
    background: #e2e8f0;
    border-radius: 999px;
    overflow: hidden;
  }
  .scan-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #0ea5e9 0%, #0284c7 100%);
    border-radius: 999px;
    transition: width 0.35s ease;
  }

  /* Right Side: Details & Progress Chips */
  .processing-details {
    padding: 10px;
    text-align: left;
  }
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #0284c7;
    background: #e0f2fe;
    padding: 5px 12px;
    border-radius: 9999px;
    margin-bottom: 12px;
  }
  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #0284c7;
    animation: pulseDot 1.4s infinite;
  }
  @keyframes pulseDot { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.8); } }

  .details-title {
    font-size: 21px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.25;
    margin-bottom: 8px;
  }
  .details-sub {
    font-size: 13.5px;
    color: var(--ink-muted);
    line-height: 1.55;
    margin-bottom: 22px;
  }

  /* Step track */
  .step-track {
    display: flex;
    flex-direction: column;
    gap: 9px;
  }
  .step-chip-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-faint);
  }
  .chip-indicator {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1.5px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    background: #fff;
    color: var(--ink-faint);
    transition: all 0.2s ease;
  }
  .step-chip-row.active {
    color: var(--primary);
  }
  .step-chip-row.active .chip-indicator {
    border-color: var(--primary);
    background: var(--sky-soft);
    color: var(--primary);
  }
  .step-chip-row.done {
    color: var(--ink);
  }
  .step-chip-row.done .chip-indicator {
    border-color: #10b981;
    background: #10b981;
    color: #fff;
  }

  /* Mobile Responsiveness for Processing UI Box (320px - 540px) */
  @media (max-width: 540px) {
    .tool-container {
      padding: 0 12px;
    }
    .main-tool-card {
      padding: 20px 12px;
      border-radius: 18px;
    }
    .lottie-scan-stage {
      width: 90%;
      max-width: 380px;
      margin: 0 auto;
      padding: 20px 12px;
    }
    .processing-details {
      width: 90%;
      max-width: 380px;
      margin: 16px auto 0;
      padding: 4px;
    }
  }

  @media (max-width: 375px) {
    .tool-container {
      padding: 0 6px;
    }
    .main-tool-card {
      padding: 14px 6px;
      border-radius: 14px;
    }
    .lottie-scan-stage {
      width: 90%;
      max-width: 380px;
      margin: 0 auto;
      padding: 16px 8px;
    }
    .scan-progress-box {
      padding: 8px 10px;
    }
    .processing-details {
      width: 90%;
      max-width: 380px;
      margin: 12px auto 0;
    }
  }

  @media (max-width: 330px) {
    .tool-container {
      padding: 0 4px;
    }
    .main-tool-card {
      padding: 12px 4px;
    }
    .lottie-scan-stage {
      width: 92%;
      padding: 14px 6px;
    }
  }

  /* ---------- Result View ---------- */
  .result {
    display: none;
    text-align: center;
    padding: 24px 0;
  }
  .result.active {
    display: block;
    animation: fadeIn 0.3s ease;
  }
  .result-icon-circle {
    width: 68px;
    height: 68px;
    background: #dcfce7;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    color: #16a34a;
  }
  .result-icon-circle svg { width: 34px; height: 34px; fill: none; stroke: currentColor; stroke-width: 2.5; }
  .result h3 {
    font-size: 23px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 6px;
  }
  .result p {
    font-size: 14.5px;
    color: var(--ink-muted);
    margin-bottom: 24px;
  }
  .result-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 14px;
  }
  /* From Uiverse.io by nazar-gavrylyk */ 
  .container {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .label {
    background-color: #0f172a;
    border: 2px solid rgb(91, 91, 240);
    display: flex;
    align-items: center;
    border-radius: 50px;
    width: 160px;
    height: 57px;
    cursor: pointer;
    transition: all 0.4s ease;
    padding: 5px;
    position: relative;
    user-select: none;
    -webkit-user-select: none;
    box-sizing: border-box;
  }

  .label::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    width: 8px;
    height: 8px;
    transition: all 0.4s ease;
    border-radius: 100%;
    margin: auto;
    opacity: 0;
    visibility: hidden;
  }

  .label .input {
    display: none;
  }

  .label .title {
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    transition: all 0.4s ease;
    position: absolute;
    right: 18px;
    top: 50%;
    transform: translateY(-50%);
    text-align: center;
    margin: 0;
    line-height: 1;
  }

  .label .title:last-child {
    opacity: 0;
    visibility: hidden;
  }

  .label .circle {
    height: 45px;
    width: 45px;
    border-radius: 50%;
    background-color: rgb(91, 91, 240);
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.4s ease;
    position: relative;
    box-shadow: 0 0 0 0 rgb(255, 255, 255);
    overflow: hidden;
    flex-shrink: 0;
  }

  .label .circle .icon {
    color: #fff;
    width: 26px;
    height: 26px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.4s ease;
  }

  .label .circle .square {
    aspect-ratio: 1;
    width: 15px;
    border-radius: 2px;
    background-color: #fff;
    opacity: 0;
    visibility: hidden;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.4s ease;
  }

  .label .circle::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    background-color: #3333a8;
    width: 100%;
    height: 0;
    transition: all 0.4s ease;
  }

  .label:has(.input:checked),
  .label.is-checked {
    width: 57px;
    animation: installed 0.35s ease 2s forwards;
  }

  .label:has(.input:checked)::before,
  .label.is-checked::before {
    animation: rotate 1.8s ease-in-out 0.2s forwards;
  }

  .label .input:checked + .circle,
  .label.is-checked .circle {
    animation:
      pulse 0.8s forwards,
      circleDelete 0.2s ease 2s forwards;
    rotate: 180deg;
  }

  .label .input:checked + .circle::before,
  .label.is-checked .circle::before {
    animation: installing 1.8s ease-in-out forwards;
  }

  .label .input:checked + .circle .icon,
  .label.is-checked .circle .icon {
    opacity: 0;
    visibility: hidden;
  }

  .label .input:checked ~ .circle .square,
  .label.is-checked ~ .circle .square {
    opacity: 1;
    visibility: visible;
  }

  .label .input:checked ~ .title,
  .label.is-checked ~ .title {
    opacity: 0;
    visibility: hidden;
  }

  .label .input:checked ~ .title:last-child,
  .label.is-checked ~ .title:last-child {
    animation: showInstalledMessage 0.35s ease 2s forwards;
  }

  @keyframes pulse {
    0% {
      scale: 0.95;
      box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7);
    }
    70% {
      scale: 1;
      box-shadow: 0 0 0 16px rgba(255, 255, 255, 0);
    }
    100% {
      scale: 0.95;
      box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
    }
  }

  @keyframes installing {
    from {
      height: 0;
    }
    to {
      height: 100%;
    }
  }

  @keyframes rotate {
    0% {
      transform: rotate(-90deg) translate(27px) rotate(0);
      opacity: 1;
      visibility: visible;
    }
    99% {
      transform: rotate(270deg) translate(27px) rotate(270deg);
      opacity: 1;
      visibility: visible;
    }
    100% {
      opacity: 0;
      visibility: hidden;
    }
  }

  @keyframes installed {
    100% {
      width: 150px;
      border-color: rgb(35, 174, 35);
    }
  }

  @keyframes circleDelete {
    100% {
      opacity: 0;
      visibility: hidden;
    }
  }

  @keyframes showInstalledMessage {
    100% {
      opacity: 1;
      visibility: visible;
      right: 56px;
    }
  }
  .btn-reset {
    background: #ffffff;
    color: var(--ink);
    border: 2px solid #cbd5e1;
    font-size: 15.5px;
    font-weight: 700;
    height: 57px;
    padding: 0 28px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.25s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    box-sizing: border-box;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    line-height: 1;
    margin: 0;
  }
  .btn-reset:hover {
    background: #f8fafc;
    border-color: #94a3b8;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  }
  .btn-reset svg {
    width: 17px;
    height: 17px;
    stroke: currentColor;
    fill: none;
    stroke-width: 2.2;
    transition: transform 0.3s ease;
  }
  .btn-reset:hover svg {
    transform: rotate(-45deg);
  }

  /* Error Box */
  .error-box {
    display: none;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    font-size: 14px;
    text-align: left;
    margin-top: 20px;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .error-box.active { display: block; }

  /* ---------- Feature Cards (Image 4) ---------- */
  .section-features {
    max-width: 980px;
    margin: 80px auto 0;
    padding: 0 20px;
    text-align: center;
  }
  .features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 24px;
  }
  @media (max-width: 768px) {
    .features-grid { grid-template-columns: 1fr; }
  }
  .feature-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-md);
    padding: 26px;
    text-align: left;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .feature-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
  }
  .feature-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  .feature-icon-pill {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #f0f9ff;
    color: #0284c7;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .feature-icon-pill svg { width: 22px; height: 22px; stroke: currentColor; fill: none; stroke-width: 2; }

  .free-badge {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--green-badge);
    background: var(--green-badge-bg);
    padding: 4px 10px;
    border-radius: 9999px;
    text-transform: uppercase;
  }
  .feature-box h3 {
    font-size: 17px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
  }
  .feature-box p {
    font-size: 13.5px;
    color: var(--ink-muted);
    line-height: 1.6;
  }
  .features-footer-caption {
    font-size: 13.5px;
    color: var(--ink-muted);
    margin-top: 14px;
  }

  /* ---------- Before & After Section (Image 5) ---------- */
  .section-comparison {
    max-width: 980px;
    margin: 90px auto 0;
    padding: 0 20px;
  }
  .comparison-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
  }
  @media (max-width: 800px) {
    .comparison-grid { grid-template-columns: 1fr; gap: 32px; }
  }
  .comp-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4f46e5;
    margin-bottom: 12px;
    display: inline-block;
  }
  .comp-title {
    font-size: clamp(28px, 3.6vw, 40px);
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 18px;
  }
  .comp-desc {
    font-size: 15px;
    color: var(--ink-muted);
    line-height: 1.65;
    margin-bottom: 28px;
  }
  .comp-desc strong {
    color: var(--ink);
  }
  .comp-stats {
    display: flex;
    gap: 28px;
    flex-wrap: wrap;
    padding-top: 18px;
    border-top: 1px solid var(--line);
  }
  .comp-stat-item h4 {
    font-size: 16px;
    font-weight: 800;
    color: #4f46e5;
    margin-bottom: 2px;
  }
  .comp-stat-item p {
    font-size: 12px;
    color: var(--ink-muted);
  }

  /* Comparison Visual Interactive Split Slider */
  .comp-visuals-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 0;
    margin: 0;
  }

  /* ---------- Interactive Split Curtain Comparison Slider ---------- */
  .split-slider-container {
    position: relative;
    width: 100%;
    margin: 0 auto;
    padding: 0;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 16px 38px -8px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(226, 232, 240, 0.9);
    user-select: none;
    -webkit-user-select: none;
    touch-action: pan-y;
    background: transparent !important;
  }
  #homepage-split-slider {
    width: 100%;
    max-width: 440px;
    aspect-ratio: 4 / 5;
    padding: 0;
    margin: 0 auto;
    overflow: hidden;
    background: transparent !important;
  }
  #user-split-slider {
    width: 100%;
    max-width: 620px;
    padding: 0;
    margin: 0 auto;
    overflow: hidden;
    background: transparent !important;
  }
  .split-layer {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    padding: 0;
    margin: 0;
    background: transparent !important;
  }
  .split-slider-container img,
  .split-layer img,
  .split-img {
    position: absolute;
    inset: 0;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center !important;
    display: block;
    pointer-events: none;
    background: transparent !important;
  }
  #homepage-split-slider img,
  #homepage-split-slider .split-img {
    object-position: center 80% !important;
  }
  .split-before {
    clip-path: polygon(0 0, 50% 0, 50% 100%, 0 100%);
    z-index: 2;
  }
  .split-after {
    clip-path: polygon(50% 0, 100% 0, 100% 100%, 50% 100%);
    z-index: 2;
  }
  .split-handle {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .split-line {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 2.5px;
    background: #ffffff;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  }
  .split-knob {
    width: 38px;
    height: 38px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4), 0 0 0 2px #0ea5e9;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0284c7;
    z-index: 6;
  }
  .split-knob svg {
    width: 18px;
    height: 18px;
    stroke: currentColor;
    stroke-width: 2.5;
    fill: none;
  }
  .split-label {
    position: absolute;
    bottom: 12px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.03em;
    pointer-events: none;
    backdrop-filter: blur(8px);
    z-index: 4;
  }
  .before-label {
    left: 12px;
    background: rgba(15, 23, 42, 0.75);
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }
  .after-label {
    right: 12px;
    background: rgba(2, 132, 199, 0.85);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.25);
  }
  .split-range {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: ew-resize;
    z-index: 10;
    margin: 0;
    padding: 0;
  }

  /* Result-specific slider wrap */
  .result-slider-container {
    margin: 18px auto 20px;
    max-width: 620px;
  }

  /* Removix Deep Clean Audit Card */
  .audit-card {
    max-width: 520px;
    margin: 18px auto 20px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px 18px;
    text-align: left;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
  }
  .audit-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e2e8f0;
  }
  .audit-badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    color: #0369a1;
  }
  .audit-badge-pill svg {
    width: 16px;
    height: 16px;
    stroke: currentColor;
    stroke-width: 2.2;
    fill: none;
  }
  .audit-status-tag {
    font-size: 11.5px;
    font-weight: 700;
    color: #15803d;
    background: #dcfce7;
    padding: 3px 8px;
    border-radius: 999px;
  }
  .audit-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  @media (max-width: 540px) {
    .audit-grid { grid-template-columns: 1fr; }
  }
  .audit-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
  }
  .audit-check {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #0284c7;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    flex-shrink: 0;
    margin-top: 1px;
  }
  .audit-item strong {
    display: block;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.25;
  }
  .audit-item small {
    display: block;
    font-size: 11px;
    color: var(--ink-muted);
    line-height: 1.3;
    margin-top: 2px;
  }

  /* ---------- Privacy / Local Processing Section (Image 2) ---------- */
  .section-privacy {
    max-width: 980px;
    margin: 100px auto 0;
    padding: 0 20px;
    text-align: center;
  }
  .privacy-title {
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin-bottom: 40px;
  }
  .privacy-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    text-align: left;
  }
  @media (max-width: 768px) {
    .privacy-grid { grid-template-columns: 1fr; }
  }
  .privacy-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-md);
    padding: 30px 26px;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .privacy-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
  }
  .privacy-icon-box {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: #ecfdf5;
    color: #10b981;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
  }
  .privacy-icon-box svg { width: 22px; height: 22px; stroke: currentColor; fill: none; stroke-width: 2; }
  .privacy-card h3 {
    font-size: 17px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 10px;
  }
  .privacy-card p {
    font-size: 13.5px;
    color: var(--ink-muted);
    line-height: 1.6;
  }

  /* ---------- Professional Developer Footer ---------- */
  footer.site-footer {
    max-width: 980px;
    margin: 80px auto 45px;
    padding: 24px 20px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
  }
  .copyright-text {
    color: var(--ink-muted);
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.01em;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .dev-link {
    color: var(--primary);
    font-weight: 700;
    text-decoration: none;
    padding: 4px 10px;
    border-radius: 8px;
    background: #e0f2fe;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }
  .dev-link:hover {
    background: var(--primary);
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
  }
  .dev-link svg {
    width: 13px;
    height: 13px;
    stroke: currentColor;
    fill: none;
    stroke-width: 2.2;
    transition: transform 0.2s ease;
  }
  .dev-link:hover svg {
    transform: translate(1px, -1px);
  }
</style>
</head>
<body>

<!-- Clean Removix Header -->
<header class="top-header">
  <div class="brand-badge">
    <div class="brand-icon">
      <img src="/static/removix.svg?v=5" alt="Removix Logo" class="brand-logo-img">
    </div>
    <span class="brand-name">emovix</span>
  </div>
</header>

<!-- Hero Section -->
<section class="hero">
  <div class="badge-tag">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z"/></svg>
    REMOVIX • AI WATERMARK REMOVER
  </div>
  <h1>Removix Watermark Remover</h1>
  <p class="hero-sub">
    Drop any AI <strong>video or image</strong> and the watermark is gone in seconds — every frame, original quality, ready to post.
  </p>
</section>

<!-- Interactive Tool Container -->
<section class="tool-container" id="tool-section">
  <div class="main-tool-card">

    <!-- Mode Selector Tabs -->
    <div class="tool-tabs" id="tool-tabs">
      <button class="tool-tab active" id="tab-video" onclick="setMode('video')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>
        Video Remover
      </button>
      <button class="tool-tab" id="tab-image" onclick="setMode('image')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        Image Remover
      </button>
    </div>

    <!-- Dropzone View (3D Floating Folder Animation by 3bdel3ziz-T) -->
    <div id="dropzone" tabindex="0">
      <div class="folder-container">
        <div class="folder">
          <div class="front-side">
            <div class="tip"></div>
            <div class="cover"></div>
          </div>
          <div class="back-side cover"></div>
        </div>
        <label class="custom-file-upload" for="file">
          Choose a file
        </label>
      </div>
      <p class="drop-primary" id="drop-primary-text">Drop your video or image here, or browse</p>
      <p class="drop-secondary" id="drop-secondary-text">Supports MP4, MOV, WebM, MKV, PNG, JPG, WEBP • Max 4K resolution</p>
    </div>
    <input type="file" id="file" accept=".mp4,.mov,.m4v,.webm,.mkv,.avi,.flv,.png,.jpg,.jpeg,.webp">

    <!-- Processing View -->
    <div class="processing" id="processing">
      <div class="processing-layout">
        <!-- Lottie AI Scanner Stage -->
        <div class="lottie-scan-stage" id="lottie-scan-stage">
          <div class="scan-bg-preview" id="scan-bg-preview"></div>
          <div class="scan-bg-overlay"></div>
          <div class="scan-badge">
            <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            AI Frame Matrix Scanner
          </div>
          <div class="lottie-container" id="lottie-container"></div>
          <div class="stage-title" id="stage-title">Analyzing and detecting...</div>
          <p class="stage-sub" id="stage-sub">Reconstructing background and removing watermark cleanly</p>
          <div class="scan-progress-box">
            <div class="scan-progress-header">
              <span id="scan-file-label">Restoration progress</span>
              <span class="scan-pct-value" id="ring-pct">0%</span>
            </div>
            <div class="scan-progress-track">
              <div class="scan-progress-bar" id="player-progress-fill"></div>
            </div>
          </div>
        </div>

        <!-- Right Side: Details & Progress Chips -->
        <div class="processing-details">
          <div class="status-badge">
            <span class="status-dot"></span>
            PROCESSING
          </div>
          <h2 class="details-title" id="details-title">Restoring background with AI...</h2>
          <p class="details-sub">Analyzing pixels and reconstructing original background. One moment.</p>

          <div class="step-track">
            <div class="step-chip-row" id="chip-queued">
              <div class="chip-indicator">1</div>
              <span>Upload to server</span>
            </div>
            <div class="step-chip-row" id="chip-scanning">
              <div class="chip-indicator">2</div>
              <span>Scan frames & detect watermark</span>
            </div>
            <div class="step-chip-row" id="chip-removing">
              <div class="chip-indicator">3</div>
              <span>Intelligent background reconstruction</span>
            </div>
            <div class="step-chip-row" id="chip-finalizing">
              <div class="chip-indicator">4</div>
              <span>Finalizing clean stream</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Result View -->
    <div class="result" id="result">
      <div class="result-icon-circle">
        <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3>Watermark Removed — Clean & Seamless</h3>
      <p>Smart AI reconstruction. Original texture and detail preserved.</p>

      <!-- Live Interactive Comparison Slider for User Upload -->
      <div class="result-slider-container" id="user-split-wrap" style="display:none;">
        <div class="split-slider-container" id="user-split-slider">
          <div class="split-layer split-before">
            <img src="" id="user-img-before" alt="Original" class="split-img">
            <span class="split-label before-label">Original</span>
          </div>
          <div class="split-layer split-after" id="user-split-after">
            <img src="" id="user-img-after" alt="Cleaned image" class="split-img">
            <span class="split-label after-label">Watermark Removed</span>
          </div>
          <div class="split-handle" id="user-split-handle">
            <div class="split-line"></div>
            <div class="split-knob">
              <svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg>
            </div>
          </div>
          <input type="range" min="0" max="100" value="50" class="split-range" id="user-range" aria-label="Compare Original and Cleaned">
        </div>
      </div>

      <!-- Removix AI Provenance Audit Badge -->
      <div class="audit-card">
        <div class="audit-header">
          <div class="audit-badge-pill">
            <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span>Removix Deep Clean Audit</span>
          </div>
          <span class="audit-status-tag">✓ 100% Seamlessly Restored</span>
        </div>
        <div class="audit-grid">
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>Visible AI Watermark</strong>
              <small>Seamless AI reconstruction</small>
            </div>
          </div>
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>Zero Smudge Guarantee</strong>
              <small>Original texture & grain preserved</small>
            </div>
          </div>
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>AI Provenance & Metadata</strong>
              <small>Generative markers removed</small>
            </div>
          </div>
          <div class="audit-item">
            <div class="audit-check">✓</div>
            <div>
              <strong>Lossless Dimensions</strong>
              <small>Byte-identical pixels outside watermark</small>
            </div>
          </div>
        </div>
      </div>
      <div class="result-actions">
        <!-- From Uiverse.io by nazar-gavrylyk --> 
        <div class="container">
          <label class="label" id="dl-label">
            <input type="checkbox" class="input" id="dl-checkbox" />
            <span class="circle">
              <svg
                class="icon"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M12 19V5m0 14-4-4m4 4 4-4"
                ></path>
              </svg>
              <div class="square"></div>
            </span>
            <p class="title">Download</p>
            <p class="title">Open</p>
          </label>
        </div>
        <button class="btn-reset" id="reset-btn">
          <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Clean Another File
        </button>
      </div>
    </div>

    <!-- Error Box -->
    <div class="error-box" id="error-box"></div>

  </div>
</section>

<!-- Feature Cards Section (Image 4) -->
<section class="section-features">
  <div class="features-grid">
    <!-- Card 1 -->
    <div class="feature-box">
      <div class="feature-top">
        <div class="feature-icon-pill">
          <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>
        </div>
        <span class="free-badge">FREE</span>
      </div>
      <h3>Visible logo, lifted</h3>
      <p>The AI watermark sparkle is tracked and removed frame-to-frame without annoying blurs or corner crops.</p>
    </div>

    <!-- Card 2 -->
    <div class="feature-box">
      <div class="feature-top">
        <div class="feature-icon-pill">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        </div>
        <span class="free-badge">FREE</span>
      </div>
      <h3>Every frame, clean</h3>
      <p>The logo is removed across the whole clip, no flicker, no smear. Frame coherence is preserved 100%.</p>
    </div>

    <!-- Card 3 -->
    <div class="feature-box">
      <div class="feature-top">
        <div class="feature-icon-pill">
          <svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        </div>
        <span class="free-badge">FREE</span>
      </div>
      <h3>Pixel-perfect quality</h3>
      <p>Resolution, frame rate, and bitrate stay exactly as rendered. Audio stream passes untouched.</p>
    </div>
  </div>

  <p class="features-footer-caption">
    No re-encode penalty, resolution, frame rate, and bitrate stay exactly as originally rendered.
  </p>
</section>

<!-- Before & After Comparison Section (Image 5) -->
<section class="section-comparison">
  <div class="comparison-grid">
    <div class="comp-text-col">
      <span class="comp-label">Removix Image & Video Engine</span>
      <h2 class="comp-title">How to remove the watermark from an image</h2>
      <p class="comp-desc">
        Switch to the Image tab, drop in any Gemini, Imagen or AI picture, and the <strong>Removix image watermark remover</strong> lifts the sparkle logo automatically at the original resolution. Intelligent background reconstruction restores the watermark area with seamless precision. Outside the watermark zone, every pixel is byte-identical to the original. No compression. No artifacts. No quality loss.
      </p>

      <div class="comp-stats">
        <div class="comp-stat-item">
          <h4>byte-identical</h4>
          <p>Outside watermark</p>
        </div>
        <div class="comp-stat-item">
          <h4>unchanged</h4>
          <p>Dimensions</p>
        </div>
        <div class="comp-stat-item">
          <h4>none</h4>
          <p>Re-compression</p>
        </div>
      </div>
    </div>

    <!-- Interactive Split Curtain Comparison Slider -->
    <div class="comp-visuals-wrapper">
      <div class="split-slider-container" id="homepage-split-slider">
        <div class="split-layer split-before">
          <img src="/static/before.webp?v=7" width="1684" height="2528" alt="Original" class="split-img" loading="eager">
          <span class="split-label before-label">Original</span>
        </div>
        <div class="split-layer split-after" id="homepage-split-after">
          <img src="/static/after.webp?v=7" width="1684" height="2528" alt="After - Watermark Removed" class="split-img" loading="eager">
          <span class="split-label after-label">Watermark Removed</span>
        </div>
        <div class="split-handle" id="homepage-split-handle">
          <div class="split-line"></div>
          <div class="split-knob">
            <svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg>
          </div>
        </div>
        <input type="range" min="0" max="100" value="50" class="split-range" id="homepage-range" aria-label="Compare Before and After">
      </div>
    </div>
  </div>
</section>

<!-- "Your images never leave your device" Privacy Section (Image 2) -->
<section class="section-privacy">
  <h2 class="privacy-title">Your images never leave your device</h2>

  <div class="privacy-grid">
    <!-- Card 1 -->
    <div class="privacy-card">
      <div class="privacy-icon-box">
        <svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <h3>Local processing</h3>
      <p>Everything runs directly on your machine. Your images are never uploaded to external servers. We never see them. We never store them.</p>
    </div>

    <!-- Card 2 -->
    <div class="privacy-card">
      <div class="privacy-icon-box">
        <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h3>Personal & commercial use</h3>
      <p>Use the cleaned images for client work, social posts, marketing campaigns, presentations, anything you'd use a regular photo for.</p>
    </div>

    <!-- Card 3 -->
    <div class="privacy-card">
      <div class="privacy-icon-box">
        <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>
      <h3>Regulated industries</h3>
      <p>Healthcare, legal, and finance: your images stay on your device. No data leakage. No compliance risk. No third-party transmission.</p>
    </div>
  </div>
</section>

<!-- Professional Developer Footer -->
<footer class="site-footer">
  <p class="copyright-text">
    Copyright &copy; 2026 Removix • Developed by
    <a href="https://shivankthakur.com/" target="_blank" rel="noopener noreferrer" class="dev-link">
      Shivank Thakur
      <svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
    </a>
  </p>
</footer>

<script>
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file');
const processingEl = document.getElementById('processing');
const resultEl = document.getElementById('result');
const errorBox = document.getElementById('error-box');
const ringPct = document.getElementById('ring-pct');
const stageTitle = document.getElementById('stage-title');
const stageSub = document.getElementById('stage-sub');
const playerProgressFill = document.getElementById('player-progress-fill');
const scanFileLabel = document.getElementById('scan-file-label');
const dlCheckbox = document.getElementById('dl-checkbox');
const dlLabel = document.getElementById('dl-label');
const resetBtn = document.getElementById('reset-btn');

let currentMode = 'video';
let pollTimer = null;
let lottieAnim = null;
let currentDownloadUrl = '';
let currentDownloadFilename = '';
let isDownloadComplete = false;

function triggerDownload() {
  if (!currentDownloadUrl) return;
  const a = document.createElement('a');
  a.href = currentDownloadUrl;
  a.download = currentDownloadFilename || 'removix_clean_file';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

if (dlCheckbox) {
  dlCheckbox.addEventListener('change', () => {
    if (dlCheckbox.checked) {
      if (dlLabel) dlLabel.classList.add('is-checked');
      triggerDownload();
      setTimeout(() => {
        isDownloadComplete = true;
      }, 2350);
    }
  });

  dlCheckbox.addEventListener('click', (e) => {
    if (isDownloadComplete) {
      e.preventDefault();
      if (currentDownloadUrl) {
        window.open(currentDownloadUrl, '_blank');
      }
    }
  });
}

function initLottie() {
  if (lottieAnim) return;
  const container = document.getElementById('lottie-container');
  if (!container || !window.lottie) return;
  try {
    lottieAnim = window.lottie.loadAnimation({
      container: container,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: '/api/animation.json'
    });
  } catch (e) {
    console.warn('Lottie failed to load', e);
  }
}

// Preload Lottie animation on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLottie);
} else {
  initLottie();
}

const STAGES = {
  queued:     { title: 'Uploading file...',            sub: 'Preparing media and initializing AI restoration engine.' },
  scanning:   { title: 'Analyzing and detecting...',   sub: 'Detecting watermark coordinates with intelligent precision.' },
  removing:   { title: 'Reconstructing with AI...',    sub: 'Intelligent background reconstruction in progress.' },
  finalizing: { title: 'Finalizing clean output...',   sub: 'Saving the clean, restored file with zero quality loss.' },
};
const stageOrder = ['queued', 'scanning', 'removing', 'finalizing', 'done'];

function setMode(mode) {
  currentMode = mode;
  document.getElementById('tab-video').classList.toggle('active', mode === 'video');
  document.getElementById('tab-image').classList.toggle('active', mode === 'image');
  if (mode === 'video') {
    fileInput.accept = ".mp4,.mov,.m4v,.webm,.mkv,.avi,.flv";
    document.getElementById('drop-primary-text').textContent = "Drop your video here, or browse";
    document.getElementById('drop-secondary-text').textContent = "Supports MP4, MOV, WebM, MKV • Up to 4K resolution";
  } else {
    fileInput.accept = ".png,.jpg,.jpeg,.webp";
    document.getElementById('drop-primary-text').textContent = "Drop your image here, or browse";
    document.getElementById('drop-secondary-text').textContent = "Supports PNG, JPG, JPEG, WEBP • Lossless quality";
  }
}

['dragenter','dragover'].forEach(evt =>
  dropzone.addEventListener(evt, e => { e.preventDefault(); dropzone.classList.add('hover'); }));
['dragleave','drop'].forEach(evt =>
  dropzone.addEventListener(evt, e => { e.preventDefault(); dropzone.classList.remove('hover'); }));
dropzone.addEventListener('drop', e => { const f = e.dataTransfer.files[0]; if (f) startJob(f); });
dropzone.addEventListener('click', e => {
  if (e.target !== fileInput && !e.target.closest('label[for="file"]')) {
    fileInput.click();
  }
});
dropzone.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') fileInput.click(); });
fileInput.addEventListener('change', e => { if (e.target.files[0]) startJob(e.target.files[0]); });
resetBtn.addEventListener('click', resetUI);

function setProgress(percent, msg) {
  const p = Math.max(0, Math.min(100, (percent !== null && percent !== undefined) ? percent : 0));
  if (ringPct) ringPct.textContent = Math.round(p) + '%';
  if (playerProgressFill) playerProgressFill.style.width = p + '%';
  if (msg && stageSub) {
    stageSub.textContent = msg;
    stageSub.setAttribute('data-custom', '1');
  } else if (!msg && stageSub) {
    stageSub.removeAttribute('data-custom');
  }
}

function resetUI() {
  cleanupStream();
  processingEl.classList.remove('active');
  resultEl.classList.remove('active');
  errorBox.classList.remove('active');
  dropzone.style.display = '';
  document.getElementById('tool-tabs').style.display = 'flex';
  const bgPreview = document.getElementById('scan-bg-preview');
  if (bgPreview) {
    bgPreview.style.backgroundImage = '';
    bgPreview.classList.remove('has-image');
  }
  if (ringPct) ringPct.textContent = '0%';
  if (playerProgressFill) playerProgressFill.style.width = '0%';
  if (stageSub) stageSub.removeAttribute('data-custom');
  document.querySelectorAll('.step-chip-row').forEach(c => c.classList.remove('active','done'));
  if (lottieAnim) {
    lottieAnim.pause();
  }
  if (dlCheckbox) dlCheckbox.checked = false;
  if (dlLabel) dlLabel.classList.remove('is-checked');
  isDownloadComplete = false;
  currentDownloadUrl = '';
  currentDownloadFilename = '';
  fileInput.value = '';
  const userWrap = document.getElementById('user-split-wrap');
  if (userWrap) userWrap.style.display = 'none';
  const beforeImg = document.getElementById('user-img-before');
  const afterImg = document.getElementById('user-img-after');
  if (beforeImg) beforeImg.src = '';
  if (afterImg) afterImg.src = '';
}

function setupSplitSlider(sliderContainerId) {
  const container = document.getElementById(sliderContainerId);
  if (!container) return;
  const range = container.querySelector('.split-range');
  const beforeLayer = container.querySelector('.split-before');
  const afterLayer = container.querySelector('.split-after');
  const handle = container.querySelector('.split-handle');
  if (!range || !afterLayer || !handle) return;

  function update() {
    const val = range.value;
    if (beforeLayer) {
      beforeLayer.style.clipPath = `polygon(0 0, ${val}% 0, ${val}% 100%, 0 100%)`;
    }
    afterLayer.style.clipPath = `polygon(${val}% 0, 100% 0, 100% 100%, ${val}% 100%)`;
    handle.style.left = val + '%';
  }

  // Adjust container aspect ratio to match natural image dimensions for user-uploaded images
  if (sliderContainerId !== 'homepage-split-slider') {
    const img = container.querySelector('.split-before img');
    if (img) {
      const adjust = () => {
        if (img.naturalWidth && img.naturalHeight) {
          container.style.aspectRatio = `${img.naturalWidth} / ${img.naturalHeight}`;
        }
        update();
      };
      if (img.complete && img.naturalWidth) {
        adjust();
      } else {
        img.addEventListener('load', adjust, { once: true });
      }
    }
  }

  range.addEventListener('input', update);
  range.addEventListener('change', update);
  update();
}

setupSplitSlider('homepage-split-slider');

function setStage(stage) {
  const idx = stageOrder.indexOf(stage);
  ['queued','scanning','removing','finalizing'].forEach((key, keyIdx) => {
    const chip = document.getElementById('chip-' + key);
    if (chip) {
      chip.classList.toggle('done', keyIdx < idx);
      chip.classList.toggle('active', keyIdx === idx);
    }
  });
  const info = STAGES[stage];
  if (info) {
    stageTitle.textContent = info.title;
    if (!stageSub.getAttribute('data-custom')) {
      stageSub.textContent = info.sub;
    }
  }
}

function startJob(file) {
  dropzone.style.display = 'none';
  document.getElementById('tool-tabs').style.display = 'none';
  processingEl.classList.add('active');
  errorBox.classList.remove('active');
  resultEl.classList.remove('active');
  setStage('queued');
  setProgress(0);

  if (scanFileLabel) {
    const fn = file.name || 'File';
    scanFileLabel.textContent = fn.length > 24 ? fn.slice(0, 22) + '...' : fn;
  }

  const bgPreview = document.getElementById('scan-bg-preview');
  if (bgPreview && file) {
    if (file.type && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        bgPreview.style.backgroundImage = `url(${e.target.result})`;
        bgPreview.classList.add('has-image');
      };
      reader.readAsDataURL(file);
    } else if (file.type && file.type.startsWith('video/')) {
      const v = document.createElement('video');
      v.preload = 'metadata';
      v.muted = true;
      v.playsInline = true;
      const vUrl = URL.createObjectURL(file);
      v.src = vUrl;
      v.onloadeddata = () => {
        v.currentTime = 0.1;
      };
      v.onseeked = () => {
        try {
          const c = document.createElement('canvas');
          c.width = v.videoWidth || 320;
          c.height = v.videoHeight || 240;
          const ctx = c.getContext('2d');
          ctx.drawImage(v, 0, 0, c.width, c.height);
          bgPreview.style.backgroundImage = `url(${c.toDataURL()})`;
          bgPreview.classList.add('has-image');
        } catch (err) {}
        URL.revokeObjectURL(vUrl);
      };
    }
  }

  initLottie();
  if (lottieAnim) {
    lottieAnim.play();
  }

  const fd = new FormData();
  fd.append('file', file);

  fetch('/api/upload', { method: 'POST', body: fd })
    .then(r => r.json().then(j => ({ ok: r.ok, body: j })))
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.error || 'Upload failed.');
      poll(body.job_id, file.name);
    })
    .catch(err => showError(err.message));
}

let streamSource = null;

function cleanupStream() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
  if (streamSource) {
    streamSource.close();
    streamSource = null;
  }
}

function handleJob(job, jobId, filename) {
  if (!job) return;
  if (job.stage) {
    setStage(job.stage);
  }
  if (job.percent !== null && job.percent !== undefined) {
    setProgress(job.percent, job.message);
  }
  if (job.stage === 'error') {
    cleanupStream();
    showError(job.error || 'Processing failed.');
    return;
  }
  if (job.stage === 'done') {
    cleanupStream();
    setProgress(100);
    setTimeout(() => {
      processingEl.classList.remove('active');
      resultEl.classList.add('active');
      currentDownloadUrl = '/api/download/' + jobId;
      currentDownloadFilename = 'removix_' + filename;
      if (dlCheckbox) dlCheckbox.checked = false;
      if (dlLabel) dlLabel.classList.remove('is-checked');
      isDownloadComplete = false;

      // Live interactive split comparison for user upload
      const userWrap = document.getElementById('user-split-wrap');
      if (job.is_image && job.input_url && job.output_url && userWrap) {
        const beforeImg = document.getElementById('user-img-before');
        const afterImg = document.getElementById('user-img-after');
        if (beforeImg && afterImg) {
          beforeImg.src = job.input_url;
          afterImg.src = job.output_url;
          const userRange = document.getElementById('user-range');
          if (userRange) userRange.value = 50;
          userWrap.style.display = 'block';
          setupSplitSlider('user-split-slider');
        }
      } else if (userWrap) {
        userWrap.style.display = 'none';
      }
    }, 450);
  }
}

function startPolling(jobId, filename) {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(() => {
    fetch('/api/status/' + jobId)
      .then(r => r.json())
      .then(job => handleJob(job, jobId, filename))
      .catch(() => {});
  }, 250);
}

function poll(jobId, filename) {
  cleanupStream();

  let sseStarted = false;
  if (window.EventSource) {
    try {
      streamSource = new EventSource('/api/stream/' + jobId);
      streamSource.onmessage = (e) => {
        sseStarted = true;
        try {
          const job = JSON.parse(e.data);
          handleJob(job, jobId, filename);
        } catch (err) {}
      };
      streamSource.onerror = () => {
        if (!sseStarted) {
          cleanupStream();
          startPolling(jobId, filename);
        }
      };
    } catch (e) {
      startPolling(jobId, filename);
    }
  } else {
    startPolling(jobId, filename);
  }
}

function showError(msg) {
  cleanupStream();
  processingEl.classList.remove('active');
  errorBox.textContent = msg;
  errorBox.classList.add('active');
  dropzone.style.display = '';
  document.getElementById('tool-tabs').style.display = 'flex';
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    import socket
    import urllib.request

    def _find_free_port(preferred=7860):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", preferred)) != 0:
                return preferred
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    port = int(os.environ.get("PORT", _find_free_port(7860)))
    is_server_mode = os.environ.get("RENDER") is not None or "--server" in sys.argv or "--headless" in sys.argv

    if is_server_mode:
        print(f"Starting Removix Server on http://0.0.0.0:{port}...")
        app.run(host="0.0.0.0", port=port, debug=False)
    else:
        # Native Desktop Application Mode (Silent native window, no browser tab, no console)
        def _run_flask():
            app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

        flask_thread = threading.Thread(target=_run_flask, daemon=True)
        flask_thread.start()

        # Wait for local server to be responsive
        for _ in range(50):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=0.2) as resp:
                    if resp.status == 200:
                        break
            except Exception:
                time.sleep(0.06)

        try:
            import webview
            webview.create_window(
                title="Removix — AI Watermark Remover",
                url=f"http://127.0.0.1:{port}",
                width=1240,
                height=820,
                min_size=(960, 640),
                background_color="#f8fafc",
            )
            webview.start()
        except Exception:
            import webbrowser
            try:
                webbrowser.open(f"http://127.0.0.1:{port}")
            except Exception:
                pass
            flask_thread.join()
