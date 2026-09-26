"""
Removix - AI Media Suite & Watermark Remover
--------------------------------------------
Minimal application entry point and route dispatcher.
All UI layout is organized in the `ui/` package.
All media processing engines reside in the `modules/` package.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

from flask import Flask, request, jsonify, send_file, abort, Response, redirect

# Suppress console windows on Windows subprocesses
if sys.platform == "win32":
    _orig_popen = subprocess.Popen

    def _silent_popen(*args, **kwargs):
        if "creationflags" not in kwargs:
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        else:
            kwargs["creationflags"] |= subprocess.CREATE_NO_WINDOW
        return _orig_popen(*args, **kwargs)

    subprocess.Popen = _silent_popen

# Import Processing Logic from modules/
from modules.watermark_engine import (
    BUNDLE_DIR,
    WORKDIR,
    VIDEO_EXTS,
    IMAGE_EXTS,
    JOBS,
    JOBS_LOCK,
    set_job,
    run_job,
    detect_watermark_in_box,
    sanitize_error_message,
)
from modules.pdf_tools import images_to_pdf, pdf_to_images
from modules.pdf_merge import merge_pdfs
from modules.pdf_split import split_pdf
from modules.pdf_rotate import rotate_pdf
from modules.pdf_delete_pages import delete_pdf_pages
from modules.pdf_protect import protect_pdf
from modules.pdf_unlock import unlock_pdf
from modules.word_to_pdf import word_to_pdf
from modules.pdf_editor import (
    add_text_to_pdf,
    replace_text_in_pdf,
    add_image_to_pdf,
    add_shape_to_pdf,
    annotate_pdf_text,
    redact_pdf_area,
)
from modules.converter import convert_image, convert_media
from modules.qr_generator import generate_qr
from modules.ocr_tool import extract_text_from_file, PdfProcessingError
from modules.bg_remover import (
    is_model_available,
    get_download_status,
    trigger_model_download,
    remove_background,
)

# Import UI Views from ui/
from ui import (
    render_home_page,
    render_video_watermark_page,
    render_image_watermark_page,
    render_image_to_pdf_page,
    render_pdf_to_image_page,
    render_pdf_tools_grid_page,
    render_merge_pdf_page,
    render_split_pdf_page,
    render_rotate_pdf_page,
    render_delete_pages_page,
    render_protect_pdf_page,
    render_unlock_pdf_page,
    render_word_to_pdf_page,
    render_edit_pdf_page,
    render_converter_page,
    render_qr_page,
    render_ocr_page,
    render_bg_remove_page,
    render_more_tools_page,
    # Image Tools Hub & Views
    render_image_tools_grid_page,
    render_png_to_jpg_page,
    render_jpg_to_png_page,
    render_webp_to_jpg_page,
    render_jpg_to_webp_page,
    render_png_to_webp_page,
    render_webp_to_png_page,
    render_png_to_svg_page,
    render_jpg_to_svg_page,
    render_svg_to_png_page,
    render_jpg_to_gif_page,
    render_gif_to_jpg_page,
    render_png_to_gif_page,
    render_gif_to_png_page,
    render_jpg_to_tiff_page,
    render_tiff_to_jpg_page,
    render_png_to_tiff_page,
    render_tiff_to_png_page,
    render_resize_image_page,
    render_crop_image_page,
    render_compress_image_page,
    render_flip_image_page,
    render_black_white_page,
    render_add_text_image_page,
    render_make_round_image_page,
    render_blur_background_page,
    render_collage_maker_page,
    render_upscale_image_page,
    render_privacy_page,
    render_faq_page,
    render_contact_page,
    render_about_page,
)

# Activity Tracker Module
from modules import activity_tracker

# Image Tools Conversion & Utility Modules
from modules.png_to_jpg import convert_png_to_jpg
from modules.jpg_to_png import convert_jpg_to_png
from modules.webp_to_jpg import convert_webp_to_jpg
from modules.jpg_to_webp import convert_jpg_to_webp
from modules.png_to_webp import convert_png_to_webp
from modules.webp_to_png import convert_webp_to_png
from modules.png_to_svg import convert_png_to_svg
from modules.jpg_to_svg import convert_jpg_to_svg
from modules.svg_to_png import convert_svg_to_png
from modules.jpg_to_gif import convert_jpg_to_gif
from modules.gif_to_jpg import convert_gif_to_jpg
from modules.png_to_gif import convert_png_to_gif
from modules.gif_to_png import convert_gif_to_png
from modules.jpg_to_tiff import convert_jpg_to_tiff
from modules.tiff_to_jpg import convert_tiff_to_jpg
from modules.png_to_tiff import convert_png_to_tiff
from modules.tiff_to_png import convert_tiff_to_png
from modules.resize_image import resize_image
from modules.crop_image import crop_image
from modules.compress_image import compress_image
from modules.flip_image import flip_image
from modules.black_white import convert_black_white
from modules.add_text_image import add_text_to_image
from modules.make_round_image import make_round_image
from modules.blur_background import blur_background
from modules.collage_maker import make_collage
from modules.upscale_image import upscale_image


app = Flask(__name__)


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# =====================================================================
# 1. PAGE ROUTING (All views rendered from ui/)
# =====================================================================

@app.route("/")
@app.route("/home")
@app.route("/history")
def page_home():
    """Removix Redesigned Home Page View"""
    return render_home_page()


@app.route("/video-watermark")
@app.route("/video-tools")
def page_video_watermark():
    """Video Watermark Removal View"""
    return render_video_watermark_page()


@app.route("/image-watermark")
def page_image_watermark():
    """Image Watermark Removal View"""
    return render_image_watermark_page()


@app.route("/pdf-tools")
def page_pdf_tools():
    """PDF Tools Hub View"""
    return render_pdf_tools_grid_page()


@app.route("/image-to-pdf")
def page_image_to_pdf():
    """Image to PDF Converter View"""
    return render_image_to_pdf_page()


@app.route("/pdf-to-image")
def page_pdf_to_image():
    """PDF to Image Converter View"""
    return render_pdf_to_image_page()


@app.route("/merge-pdf")
def page_merge_pdf():
    """Merge PDF View"""
    return render_merge_pdf_page()


@app.route("/split-pdf")
def page_split_pdf():
    """Split PDF View"""
    return render_split_pdf_page()


@app.route("/rotate-pdf")
def page_rotate_pdf():
    """Rotate PDF View"""
    return render_rotate_pdf_page()


@app.route("/delete-pages")
def page_delete_pages():
    """Delete PDF Pages View"""
    return render_delete_pages_page()


@app.route("/protect-pdf")
def page_protect_pdf():
    """Protect PDF View"""
    return render_protect_pdf_page()


@app.route("/unlock-pdf")
def page_unlock_pdf():
    """Unlock PDF View"""
    return render_unlock_pdf_page()


@app.route("/word-to-pdf")
def page_word_to_pdf():
    """Word to PDF View"""
    return render_word_to_pdf_page()


@app.route("/edit-pdf")
def page_edit_pdf():
    """Edit PDF View"""
    return render_edit_pdf_page()


@app.route("/format-convert")
def page_format_converter():
    """Universal Format Converter View"""
    return render_converter_page()


@app.route("/qr-code")
@app.route("/qr-generator")
def page_qr():
    """Instant QR Code Generator View"""
    return render_qr_page()


@app.route("/image-to-text")
@app.route("/ocr")
def page_ocr():
    """Image to Text (OCR) View"""
    return render_ocr_page()


@app.route("/bg-remove")
@app.route("/background-remove")
def page_bg_remove():
    """AI Background Remover View"""
    return render_bg_remove_page()


@app.route("/more-tools")
@app.route("/more")
def page_more_tools():
    """More Tools Hub View (OCR & QR Code)"""
    return render_more_tools_page()


# =====================================================================
# Company & Info Pages (Working Footer Links)
# =====================================================================

@app.route("/privacy")
@app.route("/privacy-policy")
def page_privacy():
    """Privacy Policy View"""
    return render_privacy_page()


@app.route("/faq")
def page_faq():
    """Frequently Asked Questions View"""
    return render_faq_page()


@app.route("/contact")
def page_contact():
    """Contact Us View"""
    return render_contact_page()


@app.route("/about")
def page_about():
    """About Removix View"""
    return render_about_page()


# =====================================================================
# Image Tools Hub & Views
# =====================================================================

@app.route("/image-tools")
def page_image_tools():
    """Image Tools Hub Grid View"""
    return render_image_tools_grid_page()


# 17 Format Converter Pages
@app.route("/png-to-jpg")
def page_png_to_jpg():
    return render_png_to_jpg_page()


@app.route("/jpg-to-png")
def page_jpg_to_png():
    return render_jpg_to_png_page()


@app.route("/webp-to-jpg")
def page_webp_to_jpg():
    return render_webp_to_jpg_page()


@app.route("/jpg-to-webp")
def page_jpg_to_webp():
    return render_jpg_to_webp_page()


@app.route("/png-to-webp")
def page_png_to_webp():
    return render_png_to_webp_page()


@app.route("/webp-to-png")
def page_webp_to_png():
    return render_webp_to_png_page()


@app.route("/png-to-svg")
def page_png_to_svg():
    return render_png_to_svg_page()


@app.route("/jpg-to-svg")
def page_jpg_to_svg():
    return render_jpg_to_svg_page()


@app.route("/svg-to-png")
def page_svg_to_png():
    return render_svg_to_png_page()


@app.route("/jpg-to-gif")
def page_jpg_to_gif():
    return render_jpg_to_gif_page()


@app.route("/gif-to-jpg")
def page_gif_to_jpg():
    return render_gif_to_jpg_page()


@app.route("/png-to-gif")
def page_png_to_gif():
    return render_png_to_gif_page()


@app.route("/gif-to-png")
def page_gif_to_png():
    return render_gif_to_png_page()


@app.route("/jpg-to-tiff")
def page_jpg_to_tiff():
    return render_jpg_to_tiff_page()


@app.route("/tiff-to-jpg")
def page_tiff_to_jpg():
    return render_tiff_to_jpg_page()


@app.route("/png-to-tiff")
def page_png_to_tiff():
    return render_png_to_tiff_page()


@app.route("/tiff-to-png")
def page_tiff_to_png():
    return render_tiff_to_png_page()


# 10 Custom Image Tool Pages
@app.route("/resize-image")
def page_resize_image():
    return render_resize_image_page()


@app.route("/crop-image")
def page_crop_image():
    return render_crop_image_page()


@app.route("/compress-image")
def page_compress_image():
    return render_compress_image_page()


@app.route("/flip-image")
def page_flip_image():
    return render_flip_image_page()


@app.route("/black-white")
def page_black_white():
    return render_black_white_page()


@app.route("/add-text-image")
def page_add_text_image():
    return render_add_text_image_page()


@app.route("/make-round-image")
def page_make_round_image():
    return render_make_round_image_page()


@app.route("/blur-background")
def page_blur_background():
    return render_blur_background_page()


@app.route("/collage-maker")
def page_collage_maker():
    return render_collage_maker_page()


@app.route("/upscale-image")
def page_upscale_image():
    return render_upscale_image_page()



@app.route("/health")
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "removix", "timestamp": time.time()})


# =====================================================================
# 2. WATERMARK REMOVAL API ENDPOINTS (modules.watermark_engine)
# =====================================================================

@app.route("/upload", methods=["POST"])
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

    custom_box = None
    box_str = request.form.get("box", "").strip()
    if box_str:
        try:
            parts = [int(float(p.strip())) for p in box_str.split(",")]
            if len(parts) == 4:
                custom_box = parts
        except Exception:
            pass

    corner_mode = request.form.get("corner", "auto").strip().lower()

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

    thread = threading.Thread(
        target=run_job,
        args=(job_id, in_path, out_path, ext, custom_box, corner_mode),
        daemon=True,
    )
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/api/status/<job_id>")
def status(job_id):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    job_dir = WORKDIR / job_id
    if not job:
        if job_dir.exists():
            clean_files = [f for f in job_dir.glob("clean.*") if f.is_file() and f.stat().st_size > 0]
            if clean_files:
                is_img = clean_files[0].suffix.lower() in IMAGE_EXTS
                return jsonify({
                    "stage": "done",
                    "percent": 100,
                    "message": "Restoration complete",
                    "error": None,
                    "is_image": is_img,
                    "input_url": f"/api/preview/{job_id}/input",
                    "output_url": f"/api/preview/{job_id}/output",
                })
        abort(404)

    ext = Path(job.get("filename", "")).suffix.lower()
    is_img = ext in IMAGE_EXTS
    is_done = job["stage"] == "done"
    has_preview = is_img or (job_dir / "preview_output.jpg").exists() or bool(list(job_dir.glob("clean.*")))
    return jsonify({
        "stage": job["stage"],
        "percent": job.get("percent", 0),
        "message": job.get("message", ""),
        "error": job.get("error"),
        "is_image": is_img,
        "input_url": f"/api/preview/{job_id}/input" if is_done and has_preview else None,
        "output_url": f"/api/preview/{job_id}/output" if is_done and has_preview else None,
    })


@app.route("/stream/<job_id>")
@app.route("/api/stream/<job_id>")
def stream(job_id):
    def event_stream():
        while True:
            with JOBS_LOCK:
                job = JOBS.get(job_id)
            job_dir = WORKDIR / job_id
            if not job:
                if job_dir.exists():
                    clean_files = [f for f in job_dir.glob("clean.*") if f.is_file() and f.stat().st_size > 0]
                    if clean_files:
                        is_img = clean_files[0].suffix.lower() in IMAGE_EXTS
                        payload = {
                            "stage": "done",
                            "percent": 100,
                            "message": "Restoration complete",
                            "error": None,
                            "is_image": is_img,
                            "input_url": f"/api/preview/{job_id}/input",
                            "output_url": f"/api/preview/{job_id}/output",
                        }
                        yield f"data: {json.dumps(payload)}\n\n"
                        break
                yield "event: error\ndata: {}\n\n"
                break

            stage = job["stage"]
            percent = job.get("percent", 0)
            message = job.get("message", "")
            error = job.get("error")
            ext = Path(job.get("filename", "")).suffix.lower()
            is_img = ext in IMAGE_EXTS
            is_done = stage == "done"
            has_preview = is_img or (job_dir / "preview_output.jpg").exists() or bool(list(job_dir.glob("clean.*")))

            payload = {
                "stage": stage,
                "percent": percent,
                "message": message,
                "error": error,
                "is_image": is_img,
                "input_url": f"/api/preview/{job_id}/input" if is_done and has_preview else None,
                "output_url": f"/api/preview/{job_id}/output" if is_done and has_preview else None,
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


@app.route("/preview/<job_id>/<which>")
@app.route("/api/preview/<job_id>/<which>")
def preview(job_id, which):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    job_dir = WORKDIR / job_id
    if not job_dir.exists():
        abort(404)

    target_file = None
    if which == "output":
        cand = job_dir / "preview_output.jpg"
        if cand.exists() and cand.stat().st_size > 0:
            target_file = cand
        if target_file is None and job and job.get("out_path"):
            cand = Path(job["out_path"])
            if cand.exists() and cand.stat().st_size > 0 and cand.suffix.lower() not in VIDEO_EXTS:
                target_file = cand
        if target_file is None:
            for ext in [".png", ".webp", ".jpg", ".jpeg"]:
                cand = job_dir / f"clean{ext}"
                if cand.exists() and cand.stat().st_size > 0:
                    target_file = cand
                    break
        if target_file is None:
            cand = job_dir / "preview_input.jpg"
            if cand.exists() and cand.stat().st_size > 0:
                target_file = cand
    elif which == "input":
        cand = job_dir / "preview_input.jpg"
        if cand.exists() and cand.stat().st_size > 0:
            target_file = cand
        if target_file is None:
            for ext in [".png", ".webp", ".jpg", ".jpeg"]:
                cand = job_dir / f"input{ext}"
                if cand.exists() and cand.stat().st_size > 0:
                    target_file = cand
                    break
    else:
        abort(404)

    if not target_file or not target_file.exists():
        abort(404)

    ext = target_file.suffix.lower()
    mimetypes_map = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".gif": "image/gif", ".svg": "image/svg+xml",
        ".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm",
    }
    mimetype = mimetypes_map.get(ext, "image/jpeg")
    resp = send_file(str(target_file), mimetype=mimetype)
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp


@app.route("/erase-box", methods=["POST"])
@app.route("/api/reclean/<job_id>", methods=["POST"])
def reclean(job_id=None):
    if not job_id:
        job_id = request.form.get("job_id") or (request.get_json(silent=True) or {}).get("job_id")
    if not job_id:
        return jsonify({"error": "No job_id provided"}), 400

    with JOBS_LOCK:
        job = JOBS.get(job_id)
    job_dir = WORKDIR / job_id
    if not job:
        if not job_dir.exists():
            abort(404)
        in_files = list(job_dir.glob("input.*"))
        out_files = list(job_dir.glob("clean.*"))
        fname = in_files[0].name if in_files else (out_files[0].name if out_files else "image.jpg")
        out_p = str(out_files[0]) if out_files else str(job_dir / f"clean{Path(fname).suffix}")
        job = {"id": job_id, "filename": fname, "out_path": out_p, "stage": "done", "percent": 100}
        with JOBS_LOCK:
            JOBS[job_id] = job

    data = request.get_json(silent=True) or request.form or {}
    box = data.get("box")
    if isinstance(box, str):
        try:
            box = [int(float(v.strip())) for v in box.split(",") if v.strip()]
        except Exception:
            box = None

    if not box or len(box) != 4:
        return jsonify({"error": "Invalid box coordinates"}), 400

    ext = Path(job.get("filename", "")).suffix.lower()
    out_path = Path(job.get("out_path", job_dir / f"clean{ext}"))

    if ext in IMAGE_EXTS:
        import cv2
        import numpy as np
        from remove_ai_watermarks import region_eraser

        target_img = None
        if out_path.exists() and out_path.stat().st_size > 0:
            target_img = cv2.imread(str(out_path), cv2.IMREAD_UNCHANGED)
        if target_img is None:
            target_img = cv2.imread(str(job_dir / f"input{ext}"), cv2.IMREAD_UNCHANGED)

        if target_img is None:
            return jsonify({"error": "Could not read image file"}), 500

        bx, by, bw, bh = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        if bw < 0: bx += bw; bw = abs(bw)
        if bh < 0: by += bh; bh = abs(bh)

        h, w = target_img.shape[:2]
        bx = max(0, min(w - 1, bx))
        by = max(0, min(h - 1, by))
        bw = max(1, min(w - bx, bw))
        bh = max(1, min(h - by, bh))

        cleaned = region_eraser.erase(target_img, boxes=[(bx, by, bw, bh)], backend="lama", dilate=5)
        cv2.imwrite(str(out_path), cleaned)

        preview_jpg = job_dir / "preview_output.jpg"
        preview_bgr = cleaned[:, :, :3] if cleaned.ndim == 3 and cleaned.shape[2] == 4 else cleaned
        cv2.imwrite(str(preview_jpg), preview_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

        ts = int(time.time() * 1000)
        return jsonify({
            "status": "ok",
            "message": "Selected area erased with LaMa AI",
            "output_url": f"/api/preview/{job_id}/output?t={ts}",
        })
    elif ext in VIDEO_EXTS:
        in_path = job_dir / f"input{ext}"
        with JOBS_LOCK:
            job["stage"] = "queued"
            job["percent"] = 0
            job["message"] = "Re-processing video with selected watermark area..."

        thread = threading.Thread(
            target=run_job,
            args=(job_id, in_path, out_path, ext, box, None),
            daemon=True,
        )
        thread.start()
        return jsonify({"status": "ok", "job_id": job_id})
    else:
        return jsonify({"error": "Unsupported file format"}), 400


@app.route("/api/detect_box/<job_id>", methods=["POST"])
def detect_box_endpoint(job_id):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    job_dir = WORKDIR / job_id
    if not job:
        if not job_dir.exists():
            abort(404)
        job = {"id": job_id, "filename": "image.jpg"}

    data = request.get_json(silent=True) or request.form or {}
    box = data.get("box")
    if isinstance(box, str):
        try:
            box = [int(float(v.strip())) for v in box.split(",") if v.strip()]
        except Exception:
            box = None

    if not box or len(box) != 4:
        return jsonify({"error": "Invalid box coordinates"}), 400

    ext = Path(job.get("filename", "")).suffix.lower()
    import cv2
    img = None
    if ext in VIDEO_EXTS:
        p = job_dir / "preview_input.jpg"
        if not p.exists(): p = job_dir / "preview_output.jpg"
        if p.exists(): img = cv2.imread(str(p))
    else:
        p = job_dir / f"input{ext}"
        if not p.exists(): p = Path(job.get("out_path", ""))
        if p.exists(): img = cv2.imread(str(p))

    if img is None:
        return jsonify({"status": "ok", "detected": False, "box": box, "label": "Manual selection"})

    result = detect_watermark_in_box(img, box)
    return jsonify({"status": "ok", **result})


@app.route("/download/<job_id>")
@app.route("/api/download/<job_id>")
def download(job_id):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    job_dir = WORKDIR / job_id
    if job and job.get("out_path") and Path(job["out_path"]).exists():
        p = Path(job["out_path"])
        dl_name = f"removix_{job['filename']}"
        try:
            ext = p.suffix.lower()
            f_type = "Video" if ext in VIDEO_EXTS else "Image"
            activity_tracker.log_file(
                file_name=dl_name,
                file_type=f_type,
                file_size_bytes=p.stat().st_size,
                tool_name="Watermark Remover",
                download_path=str(p),
            )
        except Exception:
            pass
        return send_file(str(p), as_attachment=True, download_name=dl_name)
    for cand in sorted(list(job_dir.glob("clean.*")) + list(job_dir.glob("output.*"))):
        if cand.is_file() and cand.stat().st_size > 0:
            fn = job.get("filename", cand.name) if job else cand.name
            dl_name = f"removix_{fn}"
            try:
                ext = cand.suffix.lower()
                f_type = "Video" if ext in VIDEO_EXTS else "Image"
                activity_tracker.log_file(
                    file_name=dl_name,
                    file_type=f_type,
                    file_size_bytes=cand.stat().st_size,
                    tool_name="Watermark Remover",
                    download_path=str(cand),
                )
            except Exception:
                pass
            return send_file(str(cand), as_attachment=True, download_name=dl_name)
    abort(404)


# =====================================================================
# 3. NEW FEATURES API ENDPOINTS (modules.pdf_tools & modules.converter)
# =====================================================================

@app.route("/api/image-to-pdf", methods=["POST"])
def api_image_to_pdf():
    files = request.files.getlist("images")
    if not files or len(files) == 0 or not files[0].filename:
        return jsonify({"error": "No images provided for PDF conversion."}), 400

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    saved_images = []
    for idx, f in enumerate(files):
        if f.filename:
            safe_name = Path(f.filename).name
            p = task_dir / f"{idx:03d}_{safe_name}"
            f.save(str(p))
            saved_images.append(p)

    out_pdf = task_dir / "Removix_Document.pdf"
    try:
        images_to_pdf(saved_images, out_pdf)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="Removix_Document.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Image to PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="Removix_Document.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pdf-to-image", methods=["POST"])
def api_pdf_to_image():
    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    fmt = request.form.get("format", "PNG").upper().strip()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_dir = task_dir / "extracted_images"
    try:
        res_path, page_count, is_zip = pdf_to_images(pdf_path, out_dir, dpi=300, fmt=fmt)
        ext = "zip" if is_zip else fmt.lower()
        mimetype = "application/zip" if is_zip else f"image/{ext}"
        base_stem = Path(safe_name).stem
        dl_name = f"{base_stem}_pages.{ext}"
        try:
            sz = Path(res_path).stat().st_size if Path(res_path).exists() else 1024
            activity_tracker.log_file(
                file_name=dl_name,
                file_type="Image",
                file_size_bytes=sz,
                tool_name="PDF to Image",
                download_path=str(res_path),
            )
        except Exception:
            pass
        return send_file(
            res_path,
            as_attachment=True,
            download_name=dl_name,
            mimetype=mimetype,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/merge-pdf", methods=["POST"])
def api_merge_pdf():
    files = request.files.getlist("files")
    if not files or len(files) < 2 or not files[0].filename:
        return jsonify({"error": "At least two PDF files are required for merging."}), 400

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    saved_pdfs = []
    for idx, f in enumerate(files):
        if f.filename:
            safe_name = Path(f.filename).name
            p = task_dir / f"{idx:03d}_{safe_name}"
            f.save(str(p))
            saved_pdfs.append(p)

    out_pdf = task_dir / "removix_merged.pdf"
    try:
        merge_pdfs(saved_pdfs, out_pdf)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_merged.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Merge PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_merged.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/split-pdf", methods=["POST"])
def api_split_pdf():
    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    split_mode = request.form.get("mode", "all").strip().lower()
    range_str = request.form.get("range", "").strip()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_dir = task_dir / "split_output"
    try:
        res_path, is_zip = split_pdf(pdf_path, out_dir, split_mode=split_mode, range_str=range_str)
        mimetype = "application/zip" if is_zip else "application/pdf"
        dl_name = "removix_split_pages.zip" if is_zip else "removix_extracted.pdf"
        try:
            sz = Path(res_path).stat().st_size if Path(res_path).exists() else 1024
            activity_tracker.log_file(
                file_name=dl_name,
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Split PDF",
                download_path=str(res_path),
            )
        except Exception:
            pass
        return send_file(
            res_path,
            as_attachment=True,
            download_name=dl_name,
            mimetype=mimetype,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/rotate-pdf", methods=["POST"])
def api_rotate_pdf():
    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    try:
        angle = int(request.form.get("angle", 90))
    except (ValueError, TypeError):
        angle = 90
    scope = request.form.get("scope", "all").strip().lower()
    range_str = request.form.get("range", "").strip()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_pdf = task_dir / "removix_rotated.pdf"
    try:
        rotate_pdf(pdf_path, out_pdf, angle=angle, page_selection=scope, range_str=range_str)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_rotated.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Rotate PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_rotated.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/delete-pages", methods=["POST"])
def api_delete_pages():
    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    pages_to_remove = request.form.get("pages", "").strip()
    if not pages_to_remove:
        return jsonify({"error": "No pages specified for deletion."}), 400

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_pdf = task_dir / "removix_cleaned.pdf"
    try:
        delete_pdf_pages(pdf_path, out_pdf, pages_to_remove)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_cleaned.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Delete Pages",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_cleaned.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/protect-pdf", methods=["POST"])
def api_protect_pdf():
    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    password = request.form.get("password", "").strip()
    if not password:
        return jsonify({"error": "A password is required to protect the PDF."}), 400

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_pdf = task_dir / "removix_protected.pdf"
    try:
        protect_pdf(pdf_path, out_pdf, password)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_protected.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Protect PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_protected.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/unlock-pdf", methods=["POST"])
def api_unlock_pdf():
    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    password = request.form.get("password", "").strip()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_pdf = task_dir / "removix_unlocked.pdf"
    try:
        unlock_pdf(pdf_path, out_pdf, password)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_unlocked.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Unlock PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_unlocked.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/word-to-pdf", methods=["POST"])
def api_word_to_pdf():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No Word document received."}), 400

    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    word_path = task_dir / safe_name
    f.save(str(word_path))

    out_pdf = task_dir / "removix_converted.pdf"
    try:
        word_to_pdf(word_path, out_pdf)
        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_converted.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Word to PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_converted.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/edit-pdf", methods=["POST"])
def api_edit_pdf():
    import base64

    if "pdf" not in request.files or not request.files["pdf"].filename:
        return jsonify({"error": "No PDF document received."}), 400

    f = request.files["pdf"]
    tool = request.form.get("tool", "text").strip().lower()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    pdf_path = task_dir / safe_name
    f.save(str(pdf_path))

    out_pdf = task_dir / "removix_edited.pdf"
    try:
        if tool == "text":
            text_val = request.form.get("text", "")
            page_num = int(request.form.get("page", 1))
            f_size = float(request.form.get("fontsize", 14))
            pos_x = float(request.form.get("x", 54))
            pos_y = float(request.form.get("y", 100))
            color_val = request.form.get("color", "#0f172a")
            add_text_to_pdf(pdf_path, out_pdf, page_num, text_val, pos_x, pos_y, f_size, color_val)

        elif tool == "replace":
            search_val = request.form.get("search_text", "")
            replace_val = request.form.get("replace_text", "")
            replace_text_in_pdf(pdf_path, out_pdf, search_val, replace_val)

        elif tool == "image":
            if "image" not in request.files or not request.files["image"].filename:
                return jsonify({"error": "No image uploaded."}), 400
            img_file = request.files["image"]
            img_path = task_dir / f"stamp_{Path(img_file.filename).name}"
            img_file.save(str(img_path))
            page_num = int(request.form.get("page", 1))
            pos_x = float(request.form.get("x", 50))
            pos_y = float(request.form.get("y", 100))
            width_val = float(request.form.get("width", 150))
            # Calculate height maintaining reasonable aspect ratio or default
            height_val = width_val * 0.65
            add_image_to_pdf(pdf_path, out_pdf, img_path, page_num, pos_x, pos_y, width_val, height_val)

        elif tool == "shape":
            shape_type = request.form.get("shape", "rect")
            stroke = request.form.get("stroke", "#0284c7")
            page_num = int(request.form.get("page", 1))
            x1 = float(request.form.get("x1", 50))
            y1 = float(request.form.get("y1", 50))
            x2 = float(request.form.get("x2", 200))
            y2 = float(request.form.get("y2", 150))
            add_shape_to_pdf(pdf_path, out_pdf, page_num, shape_type, x1, y1, x2, y2, stroke_color=stroke)

        elif tool == "annotate":
            search_val = request.form.get("search_text", "")
            annot_type = request.form.get("annot_type", "highlight")
            page_num = int(request.form.get("page", 1))
            annotate_pdf_text(pdf_path, out_pdf, page_num, annot_type, search_val)

        elif tool == "signature":
            data_url = request.form.get("signature_data", "")
            if not data_url or "," not in data_url:
                return jsonify({"error": "Invalid signature data."}), 400
            header, encoded = data_url.split(",", 1)
            sig_bytes = base64.b64decode(encoded)
            sig_path = task_dir / "signature.png"
            with open(sig_path, "wb") as sf:
                sf.write(sig_bytes)
            page_num = int(request.form.get("page", 1))
            pos_x = float(request.form.get("x", 350))
            pos_y = float(request.form.get("y", 650))
            add_image_to_pdf(pdf_path, out_pdf, sig_path, page_num, pos_x, pos_y, 160, 60)

        elif tool == "redact":
            page_num = int(request.form.get("page", 1))
            x1 = float(request.form.get("x1", 50))
            y1 = float(request.form.get("y1", 100))
            x2 = float(request.form.get("x2", 300))
            y2 = float(request.form.get("y2", 140))
            redact_pdf_area(pdf_path, out_pdf, page_num, x1, y1, x2, y2)

        try:
            sz = out_pdf.stat().st_size if out_pdf.exists() else 1024
            activity_tracker.log_file(
                file_name="removix_edited.pdf",
                file_type="PDF",
                file_size_bytes=sz,
                tool_name="Edit PDF",
                download_path=str(out_pdf),
            )
        except Exception:
            pass
        return send_file(
            str(out_pdf),
            as_attachment=True,
            download_name="removix_edited.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/format-convert", methods=["POST"])
def api_format_convert():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No file received for conversion."}), 400

    f = request.files["file"]
    target_format = request.form.get("target_format", "PNG").upper().strip().lstrip(".")

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))

    stem = Path(safe_name).stem
    out_ext = target_format.lower()
    if out_ext == "jpeg":
        out_ext = "jpg"
    out_path = task_dir / f"{stem}_converted.{out_ext}"

    src_ext = in_path.suffix.lower()
    is_img = src_ext in (".png", ".jpg", ".jpeg", ".webp", ".svg", ".bmp", ".ico", ".tiff", ".pdf")

    try:
        if is_img and target_format in ("PNG", "JPG", "JPEG", "WEBP", "SVG", "ICO", "PDF", "BMP"):
            convert_image(in_path, out_path, target_format)
        else:
            convert_media(in_path, out_path, target_format)

        mimetypes_map = {
            "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp", "svg": "image/svg+xml", "pdf": "application/pdf",
            "mp4": "video/mp4", "mov": "video/quicktime", "webm": "video/webm",
            "gif": "image/gif", "mp3": "audio/mpeg", "wav": "audio/wav", "mkv": "video/x-matroska",
        }
        mimetype = mimetypes_map.get(out_ext, "application/octet-stream")
        try:
            sz = out_path.stat().st_size if out_path.exists() else 1024
            ext_lower = out_path.suffix.lower()
            f_type = "Video" if ext_lower in VIDEO_EXTS else ("PDF" if ext_lower == ".pdf" else "Image")
            activity_tracker.log_file(
                file_name=out_path.name,
                file_type=f_type,
                file_size_bytes=sz,
                tool_name=f"Convert to {target_format}",
                download_path=str(out_path),
            )
        except Exception:
            pass
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mimetype,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/qr-generate", methods=["POST"])
def api_qr_generate():
    data = request.get_json(silent=True) or request.form or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text or link provided."}), 400

    fill_color = data.get("fill_color", "#0f172a")
    back_color = data.get("back_color", "#ffffff")
    format_opt = data.get("format", "PNG").upper().strip()

    try:
        _, data_url, mime_type, file_ext, dimensions = generate_qr(
            text=text,
            fill_color=fill_color,
            back_color=back_color,
            format=format_opt,
        )
        return jsonify({
            "status": "ok",
            "data_url": data_url,
            "format": file_ext,
            "mime_type": mime_type,
            "dimensions": dimensions,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ocr", methods=["POST"])
def api_ocr():
    f = request.files.get("file") or request.files.get("image")
    if not f or not f.filename:
        return jsonify({"error": "No file received for OCR."}), 400

    lang = request.form.get("lang", "eng+hin").strip()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    file_path = task_dir / safe_name
    f.save(str(file_path))

    try:
        res = extract_text_from_file(file_path, lang=lang)
        text = res.get("text", "").strip()
        is_pdf = res.get("is_pdf", False)
        if not text:
            msg = "No readable text was found in this image."
            return jsonify({
                "status": "empty",
                "text": "",
                "message": msg,
                "is_pdf": is_pdf,
                "truncated": res.get("truncated", False),
                "total_pages": res.get("total_pages", 1),
                "processed_pages": res.get("processed_pages", 1),
            })

        return jsonify({
            "status": "ok",
            "text": text,
            "is_pdf": is_pdf,
            "truncated": res.get("truncated", False),
            "total_pages": res.get("total_pages", 1),
            "processed_pages": res.get("processed_pages", 1),
            "lang": lang,
        })
    except PdfProcessingError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            shutil.rmtree(str(task_dir), ignore_errors=True)
        except Exception:
            pass


@app.route("/api/bg-remove/model-status", methods=["GET"])
def api_bg_model_status():
    return jsonify(get_download_status())


@app.route("/api/bg-remove/download-model", methods=["POST"])
def api_bg_model_download():
    trigger_model_download()
    return jsonify(get_download_status())


@app.route("/api/bg-remove", methods=["POST"])
def api_bg_remove():
    if "image" not in request.files or not request.files["image"].filename:
        return jsonify({"error": "No image received for background removal."}), 400

    f = request.files["image"]
    mode = request.form.get("mode", "fast").strip().lower()

    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))

    stem = Path(safe_name).stem
    out_path = task_dir / f"{stem}_transparent.png"

    # If model is not ready, automatically trigger download and await completion
    if not is_model_available():
        trigger_model_download()
        wait_seconds = 0
        while not is_model_available() and wait_seconds < 120:
            time.sleep(1.0)
            wait_seconds += 1

        if not is_model_available():
            status = get_download_status()
            err = status.get("error") or "Timed out while downloading BiRefNet AI model. Please check network connection."
            return jsonify({"error": err}), 504

    try:
        remove_background(in_path, out_path, mode=mode)
        try:
            sz = out_path.stat().st_size if out_path.exists() else 1024
            activity_tracker.log_file(
                file_name=out_path.name,
                file_type="Image",
                file_size_bytes=sz,
                tool_name="Remove Background",
                download_path=str(out_path),
            )
        except Exception:
            pass
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype="image/png",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================================
# 3. IMAGE TOOLS API ENDPOINTS
# =====================================================================

def _handle_image_tool_file(target_ext, mimetype, process_fn):
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    stem = Path(safe_name).stem
    out_path = task_dir / f"{stem}_processed.{target_ext}"
    try:
        process_fn(in_path, out_path)
        try:
            sz = out_path.stat().st_size if out_path.exists() else in_path.stat().st_size
            tool_name = request.endpoint.replace("api_", "").replace("_", " ").title() if request.endpoint else "Image Tool"
            activity_tracker.log_file(
                file_name=out_path.name,
                file_type="Image",
                file_size_bytes=sz,
                tool_name=tool_name,
                download_path=str(out_path),
            )
        except Exception:
            pass
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mimetype,
        )
    except Exception as e:
        return jsonify({"error": "Could not process this image. Please try again."}), 500


# 17 Format Converter APIs
@app.route("/api/png-to-jpg", methods=["POST"])
def api_png_to_jpg():
    return _handle_image_tool_file("jpg", "image/jpeg", convert_png_to_jpg)


@app.route("/api/jpg-to-png", methods=["POST"])
def api_jpg_to_png():
    return _handle_image_tool_file("png", "image/png", convert_jpg_to_png)


@app.route("/api/webp-to-jpg", methods=["POST"])
def api_webp_to_jpg():
    return _handle_image_tool_file("jpg", "image/jpeg", convert_webp_to_jpg)


@app.route("/api/jpg-to-webp", methods=["POST"])
def api_jpg_to_webp():
    return _handle_image_tool_file("webp", "image/webp", convert_jpg_to_webp)


@app.route("/api/png-to-webp", methods=["POST"])
def api_png_to_webp():
    return _handle_image_tool_file("webp", "image/webp", convert_png_to_webp)


@app.route("/api/webp-to-png", methods=["POST"])
def api_webp_to_png():
    return _handle_image_tool_file("png", "image/png", convert_webp_to_png)


@app.route("/api/png-to-svg", methods=["POST"])
def api_png_to_svg():
    return _handle_image_tool_file("svg", "image/svg+xml", convert_png_to_svg)


@app.route("/api/jpg-to-svg", methods=["POST"])
def api_jpg_to_svg():
    return _handle_image_tool_file("svg", "image/svg+xml", convert_jpg_to_svg)


@app.route("/api/svg-to-png", methods=["POST"])
def api_svg_to_png():
    return _handle_image_tool_file("png", "image/png", convert_svg_to_png)


@app.route("/api/jpg-to-gif", methods=["POST"])
def api_jpg_to_gif():
    return _handle_image_tool_file("gif", "image/gif", convert_jpg_to_gif)


@app.route("/api/gif-to-jpg", methods=["POST"])
def api_gif_to_jpg():
    return _handle_image_tool_file("jpg", "image/jpeg", convert_gif_to_jpg)


@app.route("/api/png-to-gif", methods=["POST"])
def api_png_to_gif():
    return _handle_image_tool_file("gif", "image/gif", convert_png_to_gif)


@app.route("/api/gif-to-png", methods=["POST"])
def api_gif_to_png():
    return _handle_image_tool_file("png", "image/png", convert_gif_to_png)


@app.route("/api/jpg-to-tiff", methods=["POST"])
def api_jpg_to_tiff():
    return _handle_image_tool_file("tiff", "image/tiff", convert_jpg_to_tiff)


@app.route("/api/tiff-to-jpg", methods=["POST"])
def api_tiff_to_jpg():
    return _handle_image_tool_file("jpg", "image/jpeg", convert_tiff_to_jpg)


@app.route("/api/png-to-tiff", methods=["POST"])
def api_png_to_tiff():
    return _handle_image_tool_file("tiff", "image/tiff", convert_png_to_tiff)


@app.route("/api/tiff-to-png", methods=["POST"])
def api_tiff_to_png():
    return _handle_image_tool_file("png", "image/png", convert_tiff_to_png)


# 10 Custom Image Tool APIs
@app.route("/api/resize-image", methods=["POST"])
def api_resize_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))

    w = request.form.get("width")
    h = request.form.get("height")
    pct = request.form.get("percentage")
    maintain = request.form.get("maintain_aspect", "true").lower() == "true"

    width_val = int(w) if w and str(w).isdigit() else None
    height_val = int(h) if h and str(h).isdigit() else None
    pct_val = int(pct) if pct and str(pct).isdigit() else None

    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".png"
    out_path = task_dir / f"resized{ext}"
    try:
        resize_image(in_path, out_path, width=width_val, height=height_val, percentage=pct_val, maintain_aspect=maintain)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not resize image."}), 500


@app.route("/api/crop-image", methods=["POST"])
def api_crop_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    ratio = request.form.get("ratio", "1:1")
    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".png"
    out_path = task_dir / f"cropped{ext}"
    try:
        left = request.form.get("left")
        top = request.form.get("top")
        right = request.form.get("right")
        bottom = request.form.get("bottom")
        if left is not None and top is not None and right is not None and bottom is not None:
            crop_image(
                in_path,
                out_path,
                ratio=None,
                left=int(float(left)),
                top=int(float(top)),
                right=int(float(right)),
                bottom=int(float(bottom)),
            )
        else:
            crop_image(in_path, out_path, ratio=ratio)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not crop image."}), 500


@app.route("/api/compress-image", methods=["POST"])
def api_compress_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    try:
        quality = int(request.form.get("quality", 75))
    except Exception:
        quality = 75
    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"
    out_path = task_dir / f"compressed{ext}"
    try:
        compress_image(in_path, out_path, quality=quality)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not compress image."}), 500


@app.route("/api/flip-image", methods=["POST"])
def api_flip_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    direction = request.form.get("direction", "horizontal")
    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".png"
    out_path = task_dir / f"flipped{ext}"
    try:
        flip_image(in_path, out_path, direction=direction)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not flip image."}), 500


@app.route("/api/black-white", methods=["POST"])
def api_black_white():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"
    out_path = task_dir / f"monochrome{ext}"
    try:
        convert_black_white(in_path, out_path)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not convert image."}), 500


@app.route("/api/add-text-image", methods=["POST"])
def api_add_text_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    text = request.form.get("text", "").strip()
    placement = request.form.get("placement", "bottom_center")
    try:
        font_size = int(request.form.get("font_size", 36))
    except Exception:
        font_size = 36
    color = request.form.get("color", "#ffffff")
    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".png"
    out_path = task_dir / f"captioned{ext}"
    try:
        add_text_to_image(in_path, out_path, text=text, placement=placement, font_size=font_size, color=color)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not add text to image."}), 500


@app.route("/api/make-round-image", methods=["POST"])
def api_make_round_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    out_path = task_dir / "round_avatar.png"
    bg_color = request.form.get("bg_color", "transparent")
    try:
        make_round_image(in_path, out_path, bg_color=bg_color)
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype="image/png",
        )
    except Exception as e:
        return jsonify({"error": "Could not make round image."}), 500


@app.route("/api/blur-background", methods=["POST"])
def api_blur_background():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))
    try:
        radius = int(request.form.get("radius", 18))
    except Exception:
        radius = 18
    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".png"
    out_path = task_dir / f"blurred{ext}"
    try:
        blur_background(in_path, out_path, radius=radius)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not process this image. Please try a different file."}), 500


@app.route("/api/collage-maker", methods=["POST"])
def api_collage_maker():
    files = request.files.getlist("files") or request.files.getlist("images")
    if not files or len(files) < 2:
        return jsonify({"error": "Please provide at least 2 images for the collage."}), 400
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []
    for idx, f in enumerate(files):
        if f and f.filename:
            safe_name = f"img_{idx}_{Path(f.filename).name}"
            p = task_dir / safe_name
            f.save(str(p))
            saved_paths.append(p)
    if len(saved_paths) < 2:
        return jsonify({"error": "Please provide at least 2 images for the collage."}), 400
    layout = request.form.get("layout", "grid")
    out_path = task_dir / "removix_collage.jpg"
    try:
        make_collage(saved_paths, out_path, layout=layout)
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype="image/jpeg",
        )
    except Exception as e:
        return jsonify({"error": "Could not build photo collage."}), 500


@app.route("/api/upscale-image", methods=["POST"])
def api_upscale_image():
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No image file uploaded."}), 400
    f = request.files["file"]
    task_id = uuid.uuid4().hex[:12]
    task_dir = Path(tempfile.gettempdir()) / "removix_tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    in_path = task_dir / safe_name
    f.save(str(in_path))

    # Enforce max 1MB limit as strictly requested in prompt
    file_size = in_path.stat().st_size
    if file_size > 1024 * 1024:
        return jsonify({"error": "Please upload an image smaller than 1MB for best results."}), 400

    ext = Path(safe_name).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".png"
    out_path = task_dir / f"upscaled{ext}"
    try:
        upscale_image(in_path, out_path, scale=2)
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        return send_file(
            str(out_path),
            as_attachment=True,
            download_name=out_path.name,
            mimetype=mime,
        )
    except Exception as e:
        return jsonify({"error": "Could not enhance this image. Please try a different file."}), 500





# =====================================================================
# 4. STATIC ASSETS & FAVICONS
# =====================================================================

LOTTIE_FILE = BUNDLE_DIR / "lottie_scan.json"
LOTTIE_JS_FILE = BUNDLE_DIR / "lottie.min.js"
BEFORE_WEBP = BUNDLE_DIR / "before.webp"
AFTER_WEBP = BUNDLE_DIR / "after.webp"
REMOVIX_PNG = BUNDLE_DIR / "removix.png"
REMOVIX_ICO = BUNDLE_DIR / "removix.ico"
REMOVIX_SVG = BUNDLE_DIR / "removix.svg"


@app.route("/api/animation.json")
def get_lottie_animation():
    if LOTTIE_FILE.exists():
        return send_file(LOTTIE_FILE, mimetype="application/json")
    abort(404)


ROOT_DIR = Path(__file__).resolve().parent
HERO_SVG_FILE = ROOT_DIR / "ui" / "components" / "hero_illustration" / "Young_man_with_red_shirt_at_a_computer.svg"
PREMIUM_LAPTOP_SVG_FILE = ROOT_DIR / "ui" / "components" / "premium_laptop" / "laptop.svg"

@app.route("/static/Young_man_with_red_shirt_at_a_computer.svg")
@app.route("/static/hero-illustration.svg")
def get_hero_svg_illustration():
    for p in [HERO_SVG_FILE, ROOT_DIR / "assets" / "images" / "Young_man_with_red_shirt_at_a_computer.svg", ROOT_DIR / "Young man with red shirt at a computer.svg"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/svg+xml")
    abort(404)


@app.route("/static/laptop.svg")
@app.route("/static/Laptop.svg")
def get_premium_laptop_svg():
    for p in [PREMIUM_LAPTOP_SVG_FILE, ROOT_DIR / "assets" / "images" / "laptop.svg", ROOT_DIR / "Laptop.svg"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/svg+xml")
    abort(404)


@app.route("/lottie.min.js")
def get_lottie_script():
    for p in [LOTTIE_JS_FILE, ROOT_DIR / "lottie.min.js", Path.cwd() / "lottie.min.js"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="application/javascript")
    abort(404)


@app.route("/static/before.webp")
@app.route("/before.webp")
def get_before_img():
    for p in [BEFORE_WEBP, Path.cwd() / "before.webp"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/webp")
    abort(404)


@app.route("/static/after.webp")
@app.route("/after.webp")
def get_after_img():
    for p in [AFTER_WEBP, Path.cwd() / "after.webp"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/webp")
    abort(404)


@app.route("/favicon.ico")
def get_favicon_ico():
    for p in [REMOVIX_ICO, Path.cwd() / "removix.ico"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/x-icon")
    abort(404)


@app.route("/static/removix.svg")
@app.route("/favicon.svg")
def get_removix_svg():
    for p in [REMOVIX_SVG, Path.cwd() / "removix.svg"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/svg+xml")
    if REMOVIX_PNG.exists():
        return send_file(str(REMOVIX_PNG), mimetype="image/png")
    abort(404)


@app.route("/static/removix.png")
@app.route("/favicon.png")
def get_removix_logo():
    for p in [REMOVIX_PNG, Path.cwd() / "removix.png"]:
        if p.exists() and p.is_file():
            return send_file(str(p), mimetype="image/png")
    abort(404)


# =====================================================================
# 5. ACTIVITY TRACKER & SETTINGS API ENDPOINTS
# =====================================================================

SETTINGS_FILE = Path(__file__).resolve().parent / "data" / "settings.json"


@app.route("/api/activity/recent", methods=["GET"])
def api_activity_recent():
    """Returns the most recent processed file records."""
    limit = request.args.get("limit", 10, type=int)
    files = activity_tracker.get_recent_files(limit=limit)
    return jsonify(files)


@app.route("/api/activity/stats", methods=["GET"])
def api_activity_stats():
    """Returns activity statistics for the requested period (week, month, all)."""
    period = request.args.get("period", "month").strip().lower()
    if period not in ("week", "month", "all"):
        period = "month"
    stats = activity_tracker.get_stats(period=period)
    return jsonify(stats)


@app.route("/api/activity/delete/<int:file_id>", methods=["DELETE", "POST"])
def api_activity_delete(file_id: int):
    """Removes a file record from the activity history."""
    success = activity_tracker.delete_file_record(file_id)
    return jsonify({"success": success})


@app.route("/api/activity/download/<int:file_id>", methods=["GET"])
def api_activity_download(file_id: int):
    """Downloads a file by its activity log ID if it exists on disk."""
    record = activity_tracker.get_file_record(file_id)
    if record and record.get("download_path"):
        p = Path(record["download_path"])
        if p.exists() and p.is_file():
            return send_file(
                str(p),
                as_attachment=True,
                download_name=record.get("name", p.name),
            )
    return redirect("/#recent-files")


@app.route("/api/settings", methods=["GET", "POST"])
def api_settings():
    """Reads or updates application preferences (e.g. theme)."""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    current_settings = {"theme": "light", "auto_refresh_seconds": 30}
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                current_settings = json.load(f)
        except Exception:
            pass

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        if "theme" in data:
            current_settings["theme"] = "dark" if data["theme"] == "dark" else "light"
        if "auto_refresh_seconds" in data:
            try:
                current_settings["auto_refresh_seconds"] = int(data["auto_refresh_seconds"])
            except Exception:
                pass
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(current_settings, f, indent=2)
        except Exception:
            pass
        return jsonify(current_settings)

    return jsonify(current_settings)


@app.route("/profile")
def profile_route():
    """Renders the Removix user profile page."""
    from ui.profile_ui import render_profile_view
    return render_profile_view()


@app.route("/api/auth/config", methods=["GET"])
def api_auth_config():
    """Returns public Supabase configuration from .env."""
    from modules.auth_config import get_supabase_config
    return jsonify(get_supabase_config())


# =====================================================================
# 6. ENTRY POINT (Desktop Window or Localhost Web Server)
# =====================================================================

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
        def _run_flask():
            app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

        flask_thread = threading.Thread(target=_run_flask, daemon=True)
        flask_thread.start()

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
