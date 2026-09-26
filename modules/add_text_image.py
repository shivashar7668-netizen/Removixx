"""
Removix Image Engine - Add Text to Image Module
-----------------------------------------------
Draws custom typography, captions, and watermarks onto images.
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps, ImageDraw, ImageFont


def hex_to_rgb(hex_str: str):
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def add_text_to_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    text: str,
    font_size: int = 36,
    color: str = "#ffffff",
    pos_x: int = 50,
    pos_y: int = 50,
    placement: str = "custom",
) -> str:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img).convert("RGBA")
        draw = ImageDraw.Draw(img)
        w, h = img.size

        # Try system fonts, fallback to default
        font = None
        for font_name in ("arial.ttf", "calibri.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except Exception:
                pass
        if font is None:
            font = ImageFont.load_default()

        # Calculate bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if placement == "center":
            draw_x = (w - text_w) // 2
            draw_y = (h - text_h) // 2
        elif placement == "bottom_center":
            draw_x = (w - text_w) // 2
            draw_y = h - text_h - 40
        elif placement == "top_left":
            draw_x = 40
            draw_y = 40
        elif placement == "top_center":
            draw_x = (w - text_w) // 2
            draw_y = 40
        elif placement == "top_right":
            draw_x = w - text_w - 40
            draw_y = 40
        elif placement == "bottom_left":
            draw_x = 40
            draw_y = h - text_h - 40
        elif placement == "bottom_right":
            draw_x = w - text_w - 40
            draw_y = h - text_h - 40
        else:
            draw_x = pos_x
            draw_y = pos_y

        rgb_color = hex_to_rgb(color)
        # Subtle drop shadow for legibility
        draw.text((draw_x + 2, draw_y + 2), text, font=font, fill=(0, 0, 0, 160))
        draw.text((draw_x, draw_y), text, font=font, fill=(*rgb_color, 255))

        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            img.convert("RGB").save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            img.save(str(output_path), optimize=True)

    return str(output_path)
