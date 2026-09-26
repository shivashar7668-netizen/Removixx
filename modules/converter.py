"""
Removix Universal Format Converter Module
----------------------------------------
Supports:
1. Image Conversions:
   - JPG ↔ PNG ↔ WEBP ↔ SVG ↔ ICO ↔ PDF
   - Uses Pillow with balanced high fidelity & file size (JPG quality=95, PNG compress_level=6 optimize=True, WEBP lossless=True).
   - High-definition SVG rendering via resvg-py (Rust engine).
2. Video & Audio Conversions:
   - MP4 ↔ MOV ↔ WebM ↔ MKV
   - Video ➔ Animated GIF (2-pass lanczos palette filter)
   - Video ➔ MP3 (320kbps) / WAV (lossless PCM)
   - Uses FFmpeg with subprocess.
"""

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

try:
    import resvg_py
except ImportError:
    resvg_py = None


def get_ffmpeg_cmd() -> str:
    """Finds ffmpeg executable from PATH or bundled imageio-ffmpeg."""
    which = shutil.which("ffmpeg")
    if which:
        return which
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.isfile(exe):
            return exe
    except Exception:
        pass
    return "ffmpeg"


def convert_image(
    input_path: str | Path,
    output_path: str | Path,
    target_format: str,
    scale: float = 2.0,
) -> str:
    """
    Converts image files between formats:
    Supports PNG, JPG, JPEG, WEBP, SVG, ICO, BMP, TIFF, PDF.
    Ensures reasonable output file sizes matching the input:
    - JPG saved with quality=95 and optimize=True (no 100% bloat)
    - PNG saved with compress_level=6 and optimize=True (lossless standard compression)
    - WEBP saved with lossless=True (compressed lossless format)
    - SVG rendered at high-resolution or embedded with clean compressed data
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    target_fmt = target_format.upper().strip().lstrip(".")
    if target_fmt == "JPEG":
        target_fmt = "JPG"

    # 1. Load Source Image
    pil_img: Image.Image
    if input_path.suffix.lower() == ".svg":
        if resvg_py is None:
            raise RuntimeError("resvg-py is not installed for SVG rendering.")
        png_bytes = resvg_py.svg_to_bytes(svg_path=str(input_path), zoom=float(scale))
        pil_img = Image.open(io.BytesIO(png_bytes))
    elif input_path.suffix.lower() == ".pdf":
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz

        doc = fitz.open(str(input_path))
        if len(doc) == 0:
            raise ValueError("The provided PDF file has no pages.")

        if target_fmt == "PDF":
            shutil.copyfile(str(input_path), str(output_path))
            doc.close()
            return str(output_path)

        if target_fmt == "SVG":
            page = doc[0]
            svg_content = page.get_svg_image()
            output_path.write_text(svg_content, encoding="utf-8")
            doc.close()
            return str(output_path)

        # For raster formats (JPG, PNG, WEBP, ICO, BMP, TIFF)
        zoom = 2.0  # High clarity ~144-150 DPI
        mat = fitz.Matrix(zoom, zoom)
        if len(doc) == 1:
            pix = doc[0].get_pixmap(matrix=mat, alpha=False)
            pil_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            doc.close()
        else:
            page_images = []
            max_w = 0
            total_h = 0
            pages_to_render = min(len(doc), 20)
            for p_idx in range(pages_to_render):
                pix = doc[p_idx].get_pixmap(matrix=mat, alpha=False)
                p_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_images.append(p_img)
                max_w = max(max_w, p_img.width)
                total_h += p_img.height + (16 if p_idx > 0 else 0)
            doc.close()

            stitched = Image.new("RGB", (max_w, total_h), (255, 255, 255))
            curr_y = 0
            for p_img in page_images:
                offset_x = (max_w - p_img.width) // 2
                stitched.paste(p_img, (offset_x, curr_y))
                curr_y += p_img.height + 16
                p_img.close()
            pil_img = stitched
    else:
        pil_img = Image.open(str(input_path))

    try:
        # 2. Convert to Target Format
        if target_fmt == "SVG":
            # Embed raster into an SVG vector container
            w, h = pil_img.size
            buf = io.BytesIO()
            import base64
            # If image has alpha or transparency, use optimized PNG; otherwise use clean JPG 95
            if pil_img.mode in ("RGBA", "LA", "P"):
                pil_img.save(buf, format="PNG", optimize=True, compress_level=6)
                mime = "image/png"
            else:
                if pil_img.mode != "RGB":
                    pil_img = pil_img.convert("RGB")
                pil_img.save(buf, format="JPEG", quality=95, optimize=True)
                mime = "image/jpeg"
            b64_data = base64.b64encode(buf.getvalue()).decode("ascii")
            svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <image width="{w}" height="{h}" href="data:{mime};base64,{b64_data}"/>
</svg>'''
            output_path.write_text(svg_content, encoding="utf-8")
            return str(output_path)

        elif target_fmt in ("JPG", "JPEG"):
            # Solid white background for transparency
            if pil_img.mode in ("RGBA", "LA", "P"):
                rgb_img = Image.new("RGB", pil_img.size, (255, 255, 255))
                if pil_img.mode == "P":
                    pil_img = pil_img.convert("RGBA")
                mask = pil_img.split()[-1] if pil_img.mode == "RGBA" else None
                rgb_img.paste(pil_img, mask=mask)
                rgb_img.save(str(output_path), "JPEG", quality=95, optimize=True)
            else:
                if pil_img.mode != "RGB":
                    pil_img = pil_img.convert("RGB")
                pil_img.save(str(output_path), "JPEG", quality=95, optimize=True)

        elif target_fmt == "PNG":
            pil_img.save(str(output_path), "PNG", optimize=True, compress_level=6)

        elif target_fmt == "WEBP":
            pil_img.save(str(output_path), "WEBP", lossless=True, quality=100, method=6)

        elif target_fmt == "ICO":
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            pil_img.save(str(output_path), format="ICO", sizes=icon_sizes)

        elif target_fmt == "PDF":
            if pil_img.mode != "RGB":
                pil_img = pil_img.convert("RGB")
            pil_img.save(str(output_path), "PDF", resolution=100.0)

        else:
            pil_img.save(str(output_path), format=target_fmt)

        return str(output_path)
    finally:
        try:
            pil_img.close()
        except Exception:
            pass


def convert_media(
    input_path: str | Path,
    output_path: str | Path,
    target_format: str,
) -> str:
    """
    Converts Video & Audio files using FFmpeg:
    Supports MP4, MOV, WEBM, MKV, GIF, MP3, WAV.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = get_ffmpeg_cmd()
    fmt = target_format.upper().strip().lstrip(".")

    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NO_WINDOW

    if fmt == "GIF":
        # Professional 2-pass palette generation for ultra-smooth GIF colors
        vf_filter = "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            "-vf", vf_filter,
            str(output_path),
        ]
    elif fmt == "MP3":
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            "-vn",
            "-c:a", "libmp3lame",
            "-b:a", "320k",
            str(output_path),
        ]
    elif fmt == "WAV":
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            "-vn",
            "-c:a", "pcm_s16le",
            str(output_path),
        ]
    elif fmt == "WEBM":
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            "-c:v", "libvpx-vp9",
            "-crf", "28",
            "-b:v", "0",
            "-c:a", "libopus",
            str(output_path),
        ]
    elif fmt in ("MP4", "MOV"):
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_path),
        ]
    elif fmt == "MKV":
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            "-c", "copy",
            str(output_path),
        ]
    else:
        cmd = [
            ffmpeg, "-y",
            "-i", str(input_path),
            str(output_path),
        ]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creationflags)
    if proc.returncode != 0:
        err_msg = proc.stderr.decode("utf-8", errors="ignore")
        raise RuntimeError(f"FFmpeg conversion failed: {err_msg[-400:] if err_msg else 'Unknown error'}")

    return str(output_path)
