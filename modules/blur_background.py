"""
Removix Image Engine - Blur Background Module
---------------------------------------------
Isolates the main portrait subject and softly blurs the background.
Uses BiRefNet model when available with smart fallback.
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps, ImageFilter
import cv2
import numpy as np


def blur_background(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    blur_radius: int = 18,
    radius: int = None,
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if radius is not None:
        blur_radius = radius
    blur_radius = max(5, min(40, blur_radius))

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img).convert("RGB")
        w, h = img.size

        # Create background blurred version
        blurred_bg = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # Attempt subject segmentation via bg_remover model
        mask = None
        try:
            from modules.bg_remover import is_model_available, remove_background
            if is_model_available():
                temp_cutout = output_path.parent / f"cutout_{output_path.stem}.png"
                remove_background(input_path, temp_cutout, mode="fast")
                if temp_cutout.exists():
                    with Image.open(temp_cutout) as co:
                        mask = co.split()[-1]
                    temp_cutout.unlink(missing_ok=True)
        except Exception:
            mask = None

        if mask is None:
            # High-performance OpenCV GrabCut center subject fallback
            try:
                cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                mask_cv = np.zeros(cv_img.shape[:2], np.uint8)
                bgd_model = np.zeros((1, 65), np.float64)
                fgd_model = np.zeros((1, 65), np.float64)
                margin_x = int(w * 0.1)
                margin_y = int(h * 0.1)
                rect = (margin_x, margin_y, w - 2 * margin_x, h - 2 * margin_y)
                cv2.grabCut(cv_img, mask_cv, rect, bgd_model, fgd_model, 3, cv2.GC_INIT_WITH_RECT)
                mask_2 = np.where((mask_cv == 2) | (mask_cv == 0), 0, 1).astype('uint8') * 255
                mask = Image.fromarray(mask_2).filter(ImageFilter.GaussianBlur(radius=3))
            except Exception:
                # Radial center focus fallthrough
                mask_raw = Image.new("L", (w, h), 0)
                draw = Image.Draw(mask_raw)
                draw.ellipse((int(w * 0.15), int(h * 0.1), int(w * 0.85), int(h * 0.9)), fill=255)
                mask = mask_raw.filter(ImageFilter.GaussianBlur(radius=30))

        # Composite sharp subject onto blurred background
        blurred_bg.paste(img, (0, 0), mask=mask)

        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            blurred_bg.save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            blurred_bg.save(str(output_path), optimize=True)

    return str(output_path)
