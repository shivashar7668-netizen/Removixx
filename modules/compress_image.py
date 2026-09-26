"""
Removix Image Engine - Compress Image Module
--------------------------------------------
Reduces image file size significantly with quality retention options (60%, 75%, 85%).
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps


def compress_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    quality: int = 75,
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    quality = max(20, min(95, quality))

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img)
        ext = output_path.suffix.lower()

        if ext in (".jpg", ".jpeg"):
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(str(output_path), "JPEG", quality=quality, optimize=True)
        elif ext == ".webp":
            img.save(str(output_path), "WEBP", quality=quality, method=6)
        elif ext == ".png":
            if quality <= 70:
                # Palettize for high compression
                pal_img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
                pal_img.save(str(output_path), "PNG", optimize=True)
            else:
                img.save(str(output_path), "PNG", compress_level=9, optimize=True)
        else:
            img.save(str(output_path), optimize=True)

    return str(output_path)
