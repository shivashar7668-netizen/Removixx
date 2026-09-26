"""
Removix Image Engine - Collage Maker Module
-------------------------------------------
Combines multiple photos into balanced grid or strip photo collages.
"""

from pathlib import Path
from typing import List, Union
from PIL import Image, ImageOps


def make_collage(
    image_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    layout: str = "grid",
    spacing: int = 14,
) -> str:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not image_paths or len(image_paths) < 2:
        raise ValueError("At least 2 images are required to make a collage.")

    images = []
    for p in image_paths[:6]:
        with Image.open(p) as img_raw:
            img = ImageOps.exif_transpose(img_raw).convert("RGB")
            images.append(img.copy())

    count = len(images)
    cell_w, cell_h = 600, 600

    # Resize all to cell size
    resized = [ImageOps.fit(im, (cell_w, cell_h), Image.Resampling.LANCZOS) for im in images]

    if layout == "horizontal" or count == 2:
        cols = count
        rows = 1
    elif layout == "vertical":
        cols = 1
        rows = count
    else:
        # Default 2-column grid
        cols = 2
        rows = (count + 1) // 2

    canvas_w = cols * cell_w + (cols + 1) * spacing
    canvas_h = rows * cell_h + (rows + 1) * spacing
    collage = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))

    for idx, im in enumerate(resized):
        r = idx // cols
        c = idx % cols
        x = spacing + c * (cell_w + spacing)
        y = spacing + r * (cell_h + spacing)
        collage.paste(im, (x, y))

    collage.save(str(output_path), "JPEG", quality=95, optimize=True)
    return str(output_path)
