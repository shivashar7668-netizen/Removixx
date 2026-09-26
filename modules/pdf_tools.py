"""
Removix PDF Tools Module
------------------------
1. Image to PDF:
   - Combines multiple images (PNG, JPG, JPEG, WEBP) into a single multi-page PDF.
   - Preserves original resolutions with Pillow.
   - Handles alpha channels smoothly with pure white canvas fill.
2. PDF to Image:
   - Extracts all pages of a PDF document at Ultra HD 300 DPI.
   - Uses PyMuPDF (fitz) for fast vector rasterization.
   - Returns a single image if 1 page, or a neatly packed ZIP file for multi-page documents.
"""

import os
import zipfile
from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageOps

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


def images_to_pdf(image_paths: List[str | Path], output_pdf_path: str | Path) -> str:
    """Combines a list of image file paths into a single high-quality PDF document."""
    if not image_paths:
        raise ValueError("No images provided for PDF conversion.")

    output_pdf_path = Path(output_pdf_path)
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    pil_images: List[Image.Image] = []
    try:
        for p in image_paths:
            raw_img = Image.open(str(p))
            # Automatically orient image according to EXIF metadata
            try:
                img = ImageOps.exif_transpose(raw_img)
            except Exception:
                img = raw_img

            # Convert RGBA/P/LA images to RGB on a crisp white canvas for standard PDF compatibility
            if img.mode == "P":
                img = img.convert("RGBA")

            if img.mode in ("RGBA", "LA"):
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                mask = img.split()[-1]
                rgb_img.paste(img, mask=mask)
                pil_images.append(rgb_img)
            elif img.mode != "RGB":
                pil_images.append(img.convert("RGB"))
            else:
                pil_images.append(img.copy())
            try:
                raw_img.close()
            except Exception:
                pass

        first_img = pil_images[0]
        remaining = pil_images[1:] if len(pil_images) > 1 else []

        first_img.save(
            str(output_pdf_path),
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=remaining,
        )
        return str(output_pdf_path)
    finally:
        for img in pil_images:
            try:
                img.close()
            except Exception:
                pass


def pdf_to_images(
    pdf_path: str | Path,
    output_dir: str | Path,
    dpi: int = 300,
    fmt: str = "PNG",
) -> Tuple[str, int, bool]:
    """
    Extracts all pages from a PDF file at crisp DPI (default 300 DPI).
    Returns (result_path, page_count, is_zip).
    If 1 page: returns path to the single image file.
    If multiple pages: returns path to a ZIP file containing all pages.
    """
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed. Please run: pip install pymupdf")

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    page_count = len(doc)
    if page_count == 0:
        doc.close()
        raise ValueError("The provided PDF file has 0 pages.")

    fmt_clean = fmt.upper().strip()
    ext = "jpg" if fmt_clean in ("JPG", "JPEG") else "png"

    extracted_files: List[Path] = []
    base_stem = pdf_path.stem

    for page_idx in range(page_count):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        out_filename = f"{base_stem}_page_{page_idx + 1:03d}.{ext}"
        out_filepath = output_dir / out_filename
        pix.save(str(out_filepath))
        extracted_files.append(out_filepath)

    doc.close()

    if page_count == 1:
        return str(extracted_files[0]), 1, False

    # Package multiple pages into a clean ZIP archive
    zip_path = output_dir / f"{base_stem}_pages_{page_count}x.zip"
    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in extracted_files:
            zipf.write(str(f), arcname=f.name)

    return str(zip_path), page_count, True
