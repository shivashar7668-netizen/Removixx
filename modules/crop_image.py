"""
Removix Image Engine - Crop Image Module
----------------------------------------
Crops images to popular aspect ratios (1:1, 16:9, 4:3, 9:16) or custom pixel coordinates.
"""

from pathlib import Path
from typing import Optional, Union
from PIL import Image, ImageOps


def crop_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    ratio: Optional[str] = None,
    left: Optional[int] = None,
    top: Optional[int] = None,
    right: Optional[int] = None,
    bottom: Optional[int] = None,
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img)
        w, h = img.size

        if ratio:
            # Aspect ratio center crop
            if ratio == "1:1":
                target_w = target_h = min(w, h)
            elif ratio == "16:9":
                if w / h > 16 / 9:
                    target_h = h
                    target_w = int(h * 16 / 9)
                else:
                    target_w = w
                    target_h = int(w * 9 / 16)
            elif ratio == "4:3":
                if w / h > 4 / 3:
                    target_h = h
                    target_w = int(h * 4 / 3)
                else:
                    target_w = w
                    target_h = int(w * 3 / 4)
            elif ratio == "9:16":
                if w / h > 9 / 16:
                    target_h = h
                    target_w = int(h * 9 / 16)
                else:
                    target_w = w
                    target_h = int(w * 16 / 9)
            else:
                target_w, target_h = w, h

            c_left = (w - target_w) // 2
            c_top = (h - target_h) // 2
            cropped = img.crop((c_left, c_top, c_left + target_w, c_top + target_h))
        elif left is not None and top is not None and right is not None and bottom is not None:
            c_left = max(0, min(w, left))
            c_top = max(0, min(h, top))
            c_right = max(c_left + 1, min(w, right))
            c_bottom = max(c_top + 1, min(h, bottom))
            cropped = img.crop((c_left, c_top, c_right, c_bottom))
        else:
            cropped = img

        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            if cropped.mode != "RGB":
                cropped = cropped.convert("RGB")
            cropped.save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            cropped.save(str(output_path), optimize=True)

    return str(output_path)
