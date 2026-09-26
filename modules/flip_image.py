"""
Removix Image Engine - Flip Image Module
----------------------------------------
Flips images horizontally (mirror reflection) or vertically (inverted).
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps


def flip_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    direction: str = "horizontal",
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img)
        if direction.lower() == "vertical":
            flipped = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        else:
            flipped = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            if flipped.mode != "RGB":
                flipped = flipped.convert("RGB")
            flipped.save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            flipped.save(str(output_path), optimize=True)

    return str(output_path)
