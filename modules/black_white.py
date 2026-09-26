"""
Removix Image Engine - Black & White Module
-------------------------------------------
Converts color images to artistic monochrome with enhanced tonal contrast.
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps, ImageEnhance


def convert_black_white(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    contrast_level: float = 1.25,
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img)
        gray = img.convert("L")
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(contrast_level)

        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            enhanced.convert("RGB").save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            enhanced.save(str(output_path), optimize=True)

    return str(output_path)
