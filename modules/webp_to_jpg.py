"""
Removix Image Engine - WEBP to JPG Module
-------------------------------------
Converts WEBP format directly to JPG with optimal quality and compression.
"""

from pathlib import Path
from typing import Union
from PIL import Image, ImageOps

try:
    import resvg_py
except ImportError:
    resvg_py = None


def convert_webp_to_jpg(input_path: Union[str, Path], output_path: Union[str, Path]) -> str:
    """
    Converts a WEBP file at input_path into a JPG file at output_path.
    Returns the string path of the generated output file.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # SVG to Raster Rendering
    if "WEBP" == "SVG":
        try:
            import pymupdf as fitz
            doc = fitz.open(str(input_path))
            page = doc[0]
            pix = page.get_pixmap(dpi=300)
            pix.save(str(output_path))
            doc.close()
            return str(output_path)
        except Exception:
            if resvg_py:
                with open(input_path, "rb") as sf:
                    svg_bytes = sf.read()
                png_bytes = resvg_py.svg_to_bytes(svg_bytes, dpi=300)
                with open(output_path, "wb") as of:
                    of.write(png_bytes)
                return str(output_path)
            raise RuntimeError("Could not render SVG document.")

    # Raster to SVG Vector Wrapper
    if "JPG" == "SVG":
        import base64
        with Image.open(input_path) as raw_img:
            img = ImageOps.exif_transpose(raw_img)
            w, h = img.size
        with open(input_path, "rb") as rf:
            b64_data = base64.b64encode(rf.read()).decode("ascii")
        mime = "image/png" if "WEBP" == "PNG" else "image/jpeg"
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <image width="{w}" height="{h}" href="data:{mime};base64,{b64_data}"/>
</svg>'''
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(svg_content)
        return str(output_path)

    # Standard Raster Image Processing
    with Image.open(input_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img)

        # Handling Target Format: JPG
        if "JPG" == "JPG":
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
                white_bg = Image.new("RGB", img.size, (255, 255, 255))
                white_bg.paste(img, mask=img.split()[-1])
                img = white_bg
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img.save(str(output_path), "JPEG", quality=95, optimize=True)

        # Handling Target Format: PNG
        elif "JPG" == "PNG":
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
            img.save(str(output_path), "PNG", compress_level=6, optimize=True)

        # Handling Target Format: WEBP
        elif "JPG" == "WEBP":
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
            img.save(str(output_path), "WEBP", quality=90, method=6)

        # Handling Target Format: GIF
        elif "JPG" == "GIF":
            if img.mode != "P":
                img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
            img.save(str(output_path), "GIF", optimize=True)

        # Handling Target Format: TIFF
        elif "JPG" == "TIFF":
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            img.save(str(output_path), "TIFF", compression="tiff_deflate")

        else:
            img.save(str(output_path))

    return str(output_path)
