"""
Removix Image Engine - Make Round Image Module
----------------------------------------------
Crops photos into circular avatars with transparent outer backgrounds.
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps, ImageDraw


def make_round_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    bg_color: str = "transparent",
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img).convert("RGBA")
        w, h = img.size
        size = min(w, h)

        # Center crop to square
        left = (w - size) // 2
        top = (h - size) // 2
        square_img = img.crop((left, top, left + size, top + size))

        # Antialiased circle mask (2x supersampling)
        mask_size = (size * 2, size * 2)
        mask = Image.new("L", mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)
        mask = mask.resize((size, size), Image.Resampling.LANCZOS)

        fill_bg = (0, 0, 0, 0)
        if bg_color == "white":
            fill_bg = (255, 255, 255, 255)
        elif bg_color and bg_color.startswith("#"):
            h_str = bg_color.lstrip("#")
            if len(h_str) == 3:
                h_str = "".join([c * 2 for c in h_str])
            if len(h_str) == 6:
                fill_bg = tuple(int(h_str[i:i+2], 16) for i in (0, 2, 4)) + (255,)

        round_img = Image.new("RGBA", (size, size), fill_bg)
        round_img.paste(square_img, (0, 0), mask=mask)
        round_img.save(str(output_path), "PNG", optimize=True)

    return str(output_path)
