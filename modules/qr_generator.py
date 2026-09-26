"""
Removix QR Code Generator Module
--------------------------------
Generates custom-colored QR codes for URLs, text, contacts, and payments in:
- PNG: Highest master quality (4K-grade resolution, lossless)
- JPG: 100% Maximum quality (4:4:4 chroma subsampling, zero color bleed)
- SVG: True mathematical vector SVG (resolution-independent, infinitely scalable with zero loss)
"""

import io
import base64
from pathlib import Path
from typing import Tuple
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image


def generate_qr_svg_vector(
    qr: qrcode.QRCode,
    fill_color: str = "#0f172a",
    back_color: str = "#ffffff",
) -> Tuple[bytes, str]:
    """
    Generates a true mathematical/vector SVG from the QR module matrix.
    Contiguous horizontal modules in each row are combined into single vector paths
    with shape-rendering="crispEdges" for resolution-independent perfection.
    """
    matrix = qr.modules
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    border = qr.border

    total_w = cols + 2 * border
    total_h = rows + 2 * border

    path_segments = []
    for r_idx in range(rows):
        y = r_idx + border
        c_idx = 0
        while c_idx < cols:
            if matrix[r_idx][c_idx]:
                start_x = c_idx + border
                while c_idx < cols and matrix[r_idx][c_idx]:
                    c_idx += 1
                span = (c_idx + border) - start_x
                path_segments.append(f"M{start_x},{y}h{span}v1h-{span}z")
            else:
                c_idx += 1

    d_str = "".join(path_segments)
    fill = fill_color or "#0f172a"
    back = back_color or "#ffffff"

    svg_content = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" '
        f'shape-rendering="crispEdges" width="100%" height="100%">\n'
        f'  <rect width="{total_w}" height="{total_h}" fill="{back}"/>\n'
        f'  <path d="{d_str}" fill="{fill}"/>\n'
        f'</svg>'
    )

    svg_bytes = svg_content.encode("utf-8")
    b64 = base64.b64encode(svg_bytes).decode("ascii")
    data_url = f"data:image/svg+xml;base64,{b64}"
    return svg_bytes, data_url


def generate_qr(
    text: str,
    fill_color: str = "#0f172a",
    back_color: str = "#ffffff",
    format: str = "PNG",
    border: int = 4,
) -> Tuple[bytes, str, str, str, str]:
    """
    Generates a QR code in PNG, JPG, or true mathematical SVG vector format.
    Returns: (output_bytes, data_url, mime_type, file_ext, dimensions_label)
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Please provide text or a URL to generate a QR code.")

    fill_color = fill_color or "#0f172a"
    back_color = back_color or "#ffffff"
    fmt = (format or "PNG").upper().strip().lstrip(".")
    if fmt == "JPEG":
        fmt = "JPG"

    # Master high-resolution box size for raster formats (PNG & JPG)
    # box_size=25 produces ~1000px to ~1400px ultra-crisp master resolution
    raster_box_size = 25

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=raster_box_size,
        border=max(1, min(20, int(border))),
    )
    qr.add_data(text)
    qr.make(fit=True)

    if fmt == "SVG":
        svg_bytes, data_url = generate_qr_svg_vector(
            qr=qr,
            fill_color=fill_color,
            back_color=back_color,
        )
        return (
            svg_bytes,
            data_url,
            "image/svg+xml",
            "svg",
            "Infinite Vector (Resolution Independent)",
        )

    # Raster rendering (PNG or JPG)
    img = qr.make_image(
        fill_color=fill_color,
        back_color=back_color,
    )
    width, height = img.size

    buf = io.BytesIO()

    if fmt == "JPG":
        # Ensure image is in RGB mode with no transparency
        if img.mode != "RGB":
            rgb_img = Image.new("RGB", img.size, color=back_color)
            if img.mode == "RGBA":
                rgb_img.paste(img, mask=img.split()[3])
            else:
                rgb_img.paste(img)
            img = rgb_img
        # Quality 100 with subsampling=0 (4:4:4 chroma subsampling for absolute razor-sharp edges)
        img.save(buf, format="JPEG", quality=100, subsampling=0, optimize=True)
        img_bytes = buf.getvalue()
        b64 = base64.b64encode(img_bytes).decode("ascii")
        data_url = f"data:image/jpeg;base64,{b64}"
        return (
            img_bytes,
            data_url,
            "image/jpeg",
            "jpg",
            f"{width}x{height}px (Master 100% Quality)",
        )

    # Default: Master Quality PNG
    img.save(buf, format="PNG", compress_level=1, optimize=True)
    img_bytes = buf.getvalue()
    b64 = base64.b64encode(img_bytes).decode("ascii")
    data_url = f"data:image/png;base64,{b64}"
    return (
        img_bytes,
        data_url,
        "image/png",
        "png",
        f"{width}x{height}px (Ultra Clarity Master)",
    )


def save_qr_to_file(
    text: str,
    output_path: str | Path,
    fill_color: str = "#0f172a",
    back_color: str = "#ffffff",
    format: str = "PNG",
    border: int = 4,
) -> str:
    """Generates and writes a QR code image directly to a file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fmt = output_path.suffix.lstrip(".") or format
    out_bytes, _, _, _, _ = generate_qr(
        text=text,
        fill_color=fill_color,
        back_color=back_color,
        format=fmt,
        border=border,
    )
    output_path.write_bytes(out_bytes)
    return str(output_path)
