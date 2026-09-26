"""
Removix Image Engine - Resize Image Module
------------------------------------------
Resizes images by custom dimensions (width/height) or percentage ratio with aspect ratio lock.
"""

from pathlib import Path
from typing import Optional, Union
from PIL import Image, ImageOps


def resize_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    width: Optional[int] = None,
    height: Optional[int] = None,
    percentage: Optional[int] = None,
    maintain_aspect: bool = True,
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img)
        orig_w, orig_h = img.size

        if percentage and percentage > 0:
            scale = percentage / 100.0
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))
        elif width and height:
            if maintain_aspect:
                img_copy = img.copy()
                img_copy.thumbnail((width, height), Image.Resampling.LANCZOS)
                new_w, new_h = img_copy.size
            else:
                new_w, new_h = max(1, width), max(1, height)
        elif width:
            new_w = max(1, width)
            new_h = max(1, int(orig_h * (new_w / orig_w)))
        elif height:
            new_h = max(1, height)
            new_w = max(1, int(orig_w * (new_h / orig_h)))
        else:
            new_w, new_h = orig_w, orig_h

        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            if resized.mode != "RGB":
                resized = resized.convert("RGB")
            resized.save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            resized.save(str(output_path), optimize=True)

    return str(output_path)
