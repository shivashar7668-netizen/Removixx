"""
Removix OCR Tool Module (Image & PDF to Text)
---------------------------------------------
Extracts text from screenshots, photos, documents, and PDFs using Tesseract OCR and pytesseract.
Supports bilingual extraction with English and Hindi language packs (hin + eng).

Advanced preprocessing pipeline:
1. Low-resolution upscale (2x interpolation for images with width/height < 500px)
2. Grayscale conversion
3. Skew detection and automated deskewing / straightening
4. Adaptive contrast & unsharp edge sharpening (blurry edge restoration)
5. Edge-preserving noise removal & denoising
6. High-resolution PDF rendering (300 DPI) with multi-page handling (up to 20 pages)
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict, Any, Union
import numpy as np
import cv2
from PIL import Image, ImageOps
import pytesseract

try:
    import pymupdf as fitz
except ImportError:
    import fitz


class PdfProcessingError(Exception):
    """Raised when a PDF file is corrupted or cannot be processed."""
    pass


# Auto-detect Tesseract executable path
CANDIDATE_PATHS = [
    Path(r"C:\Users\Production\tesseract-ocr\tesseract.exe"),
    Path.home() / "tesseract-ocr" / "tesseract.exe",
    Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
    Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    Path(__file__).parent.parent / "bin" / "tesseract-ocr" / "tesseract.exe",
]

TESSERACT_EXE = None
for cand in CANDIDATE_PATHS:
    if cand.exists():
        TESSERACT_EXE = str(cand)
        break

if not TESSERACT_EXE:
    which = shutil.which("tesseract")
    if which:
        TESSERACT_EXE = which

if TESSERACT_EXE:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE
    # Set TESSDATA_PREFIX if tessdata directory exists alongside executable
    tessdata_cand = Path(TESSERACT_EXE).parent / "tessdata"
    if tessdata_cand.exists():
        os.environ["TESSDATA_PREFIX"] = str(tessdata_cand)


def get_available_languages() -> List[str]:
    """Returns the list of installed OCR languages."""
    if not TESSERACT_EXE:
        return []
    try:
        return pytesseract.get_languages()
    except Exception:
        return ["eng"]


def deskew_image(gray: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Detects skew angle in a grayscale text image and deskews it.
    Uses Otsu thresholding + morphological dilation + minAreaRect.
    """
    try:
        # Invert Otsu threshold: text is white, background is black
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morphological dilation to connect characters horizontally into text line blobs
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        pts = cv2.findNonZero(dilated)
        if pts is None or len(pts) < 50:
            return gray, 0.0

        rect = cv2.minAreaRect(pts)
        (cx, cy), (w, h), angle = rect

        # Handle OpenCV minAreaRect angle representation
        if w < h:
            angle += 90.0

        while angle <= -45.0:
            angle += 90.0
        while angle > 45.0:
            angle -= 90.0

        # Only deskew if meaningful tilt (> 0.5 deg and < 45 deg)
        if abs(angle) > 0.5 and abs(angle) < 45.0:
            h_img, w_img = gray.shape[:2]
            center = (w_img // 2, h_img // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            deskewed = cv2.warpAffine(
                gray,
                M,
                (w_img, h_img),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )
            return deskewed, angle

        return gray, 0.0
    except Exception:
        return gray, 0.0


def preprocess_image_for_ocr(img_cv: np.ndarray) -> np.ndarray:
    """
    Comprehensive image preprocessing pipeline for high OCR accuracy:
    1. Upscale if small (width < 500px or height < 500px)
    2. Convert to Grayscale
    3. Deskew / straighten tilted text
    4. Contrast enhancement (CLAHE) & edge sharpening (Unsharp mask)
    5. Edge-preserving Denoising (Bilateral filtering)
    """
    # 1. Resize / Upscale if resolution is low (e.g., width < 500 or height < 500)
    h, w = img_cv.shape[:2]
    if w < 500 or h < 500:
        scale = max(2.0, min(3.0, 1000.0 / max(w, h, 1)))
        new_w = int(w * scale)
        new_h = int(h * scale)
        img_cv = cv2.resize(img_cv, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # 2. Grayscale conversion
    if len(img_cv.shape) == 3:
        if img_cv.shape[2] == 4:
            # BGRA -> BGR -> Gray with white background
            alpha = img_cv[:, :, 3] / 255.0
            bgr = img_cv[:, :, :3]
            white_bg = np.ones_like(bgr, dtype=np.uint8) * 255
            blended = (bgr * alpha[:, :, None] + white_bg * (1.0 - alpha[:, :, None])).astype(np.uint8)
            gray = cv2.cvtColor(blended, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_cv.copy()

    # 3. Deskew (Straighten tilted text)
    gray, _ = deskew_image(gray)

    # 4. Contrast enhancement (CLAHE) & Sharpness enhancement (Unsharp mask)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_img = clahe.apply(gray)

    # Sharpness enhancement: unsharp masking to sharpen blurry letter edges
    gaussian = cv2.GaussianBlur(contrast_img, (0, 0), 2.0)
    sharpened = cv2.addWeighted(contrast_img, 1.5, gaussian, -0.5, 0)

    # 5. Denoise: Edge-preserving bilateral filter to eliminate background grain/noise
    denoised = cv2.bilateralFilter(sharpened, d=7, sigmaColor=50, sigmaSpace=50)

    return denoised


def run_tesseract_ocr(img_gray: np.ndarray, lang: str = "eng+hin") -> str:
    """Runs Tesseract OCR on a preprocessed grayscale image."""
    if not TESSERACT_EXE:
        raise RuntimeError(
            "Tesseract OCR engine is not installed or not found. Please install Tesseract."
        )

    avail = get_available_languages()
    req_langs = [l.strip() for l in lang.split("+") if l.strip()]
    usable_langs = [l for l in req_langs if l in avail]
    if not usable_langs:
        usable_langs = ["eng"] if "eng" in avail else avail

    active_lang = "+".join(usable_langs) if usable_langs else "eng"

    # Primary OCR pass: PSM 3 (Fully automatic page segmentation)
    custom_config = r"--oem 3 --psm 3"
    text = pytesseract.image_to_string(img_gray, lang=active_lang, config=custom_config).strip()

    # Fallback if no text found: try Otsu thresholding with PSM 6 (single uniform block)
    if not text:
        otsu = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(otsu, lang=active_lang, config=r"--oem 3 --psm 6").strip()

    return text


def extract_text_from_image(
    image_input: Union[str, Path, Image.Image, np.ndarray],
    lang: str = "eng+hin",
    preprocess: bool = True,
) -> str:
    """
    Extracts text from an image (PNG, JPG, WEBP, BMP, etc.).
    Supports English, Hindi, and Bilingual recognition.
    """
    if isinstance(image_input, (str, Path)):
        img_path = Path(image_input)
        if not img_path.exists():
            raise FileNotFoundError(f"Image file not found: {img_path}")
        # Open with PIL to safely handle EXIF rotation & format support
        with Image.open(str(img_path)) as pil_img:
            try:
                pil_img = ImageOps.exif_transpose(pil_img)
            except Exception:
                pass
            pil_rgb = pil_img.convert("RGB")
            img_np = np.array(pil_rgb)
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    elif isinstance(image_input, Image.Image):
        try:
            image_input = ImageOps.exif_transpose(image_input)
        except Exception:
            pass
        pil_rgb = image_input.convert("RGB")
        img_np = np.array(pil_rgb)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    elif isinstance(image_input, np.ndarray):
        img_cv = image_input.copy()
    else:
        raise ValueError("Unsupported image input type.")

    if preprocess:
        processed_gray = preprocess_image_for_ocr(img_cv)
    else:
        if len(img_cv.shape) == 3:
            processed_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            processed_gray = img_cv

    return run_tesseract_ocr(processed_gray, lang=lang)


def extract_text_from_pdf(
    pdf_path: Union[str, Path],
    lang: str = "eng+hin",
    max_pages: int = 20,
) -> Dict[str, Any]:
    """
    Extracts text from a PDF document using PyMuPDF and Tesseract OCR:
    1. Validates and opens PDF (handles corrupted files safely)
    2. Enforces maximum 20-page processing limit
    3. Renders each page at high DPI (300 DPI)
    4. Applies preprocessing pipeline (grayscale, sharpen, denoise, deskew)
    5. Extracts text with page separators ('--- Page X ---')
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        raise PdfProcessingError("This PDF file could not be processed. Please try a different file.")

    try:
        if doc.is_encrypted and not doc.authenticate(""):
            raise PdfProcessingError("This PDF file could not be processed. Please try a different file.")

        total_pages = len(doc)
        if total_pages == 0:
            raise PdfProcessingError("This PDF file could not be processed. Please try a different file.")

        pages_to_process = min(total_pages, max_pages)
        truncated = total_pages > max_pages

        # Render at 300 DPI (72 base pt -> 300 DPI matrix)
        zoom = 300.0 / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        page_texts = []
        for page_idx in range(pages_to_process):
            page = doc[page_idx]
            pix = page.get_pixmap(matrix=matrix, alpha=False)

            # Convert pixmap samples to numpy BGR array
            img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            if pix.n == 3:
                img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            elif pix.n == 1:
                img_cv = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)
            else:
                img_cv = img_np[:, :, :3]

            # Apply same preprocessing pipeline
            processed_gray = preprocess_image_for_ocr(img_cv)

            # Extract text
            page_text = run_tesseract_ocr(processed_gray, lang=lang)

            if total_pages > 1:
                page_header = f"--- Page {page_idx + 1} ---"
                page_texts.append(f"{page_header}\n{page_text}" if page_text else f"{page_header}\n(No readable text on this page)")
            else:
                page_texts.append(page_text)

        combined_text = "\n\n".join(page_texts).strip()

        return {
            "text": combined_text,
            "total_pages": total_pages,
            "processed_pages": pages_to_process,
            "truncated": truncated,
            "is_pdf": True,
        }
    except PdfProcessingError:
        raise
    except Exception as e:
        raise PdfProcessingError("This PDF file could not be processed. Please try a different file.")
    finally:
        try:
            doc.close()
        except Exception:
            pass


def extract_text_from_file(
    file_path: Union[str, Path],
    lang: str = "eng+hin",
) -> Dict[str, Any]:
    """
    Unified entry point for both Images and PDFs.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    # Check for PDF
    is_pdf = False
    if suffix == ".pdf":
        is_pdf = True
    else:
        # Check magic bytes for PDF
        try:
            with open(path, "rb") as f:
                header = f.read(5)
                if header.startswith(b"%PDF-"):
                    is_pdf = True
        except Exception:
            pass

    if is_pdf:
        return extract_text_from_pdf(path, lang=lang, max_pages=20)
    else:
        # Image file
        try:
            text = extract_text_from_image(path, lang=lang, preprocess=True)
            return {
                "text": text,
                "total_pages": 1,
                "processed_pages": 1,
                "truncated": False,
                "is_pdf": False,
            }
        except Exception as e:
            if "Tesseract" in str(e):
                raise
            raise RuntimeError(f"Failed to process image: {str(e)}")
