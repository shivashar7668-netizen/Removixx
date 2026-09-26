"""
Removix PDF Engine - Edit PDF Module
------------------------------------
Provides Stirling-PDF-level comprehensive PDF editing capabilities:
1. Add Text & Watermarks
2. Edit / Replace Existing Text
3. Add Images & Logos
4. Add Shapes & Freehand Drawing
5. Annotations (Highlight, Underline, Strikeout)
6. Add Digital Signature
7. Redact Content & Sensitive Info Permanently
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


def hex_to_rgb_tuple(hex_str: str) -> Tuple[float, float, float]:
    """Converts '#RRGGBB' to normalized (r, g, b) float tuple (0.0 to 1.0)."""
    hex_clean = hex_str.lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    if len(hex_clean) != 6:
        return (0.0, 0.0, 0.0)
    r = int(hex_clean[0:2], 16) / 255.0
    g = int(hex_clean[2:4], 16) / 255.0
    b = int(hex_clean[4:6], 16) / 255.0
    return (r, g, b)


def add_text_to_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    page_num: int,
    text: str,
    x: float,
    y: float,
    fontsize: float = 14.0,
    color: str = "#0f172a",
) -> str:
    """Inserts text onto the specified page (1-based index) at coordinates (x, y)."""
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    if page_num < 1 or page_num > len(doc):
        doc.close()
        raise ValueError(f"Page number {page_num} out of bounds (1-{len(doc)}).")

    page = doc[page_num - 1]
    rgb = hex_to_rgb_tuple(color)
    point = fitz.Point(x, y)
    page.insert_text(point, text, fontsize=fontsize, color=rgb)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)


def replace_text_in_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    search_text: str,
    replace_text: str,
    page_num: Optional[int] = None,
) -> str:
    """
    Finds occurrences of search_text and replaces them with replace_text.
    If page_num is None, searches all pages.
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    target_pages = [page_num - 1] if page_num is not None else list(range(len(doc)))

    for p_idx in target_pages:
        if 0 <= p_idx < len(doc):
            page = doc[p_idx]
            rects = page.search_for(search_text)
            for r in rects:
                # Add redaction to erase original text
                page.add_redact_annot(r, fill=(1, 1, 1))
            page.apply_redactions()

            for r in rects:
                # Estimate font size from rect height
                f_size = max(8.0, r.height * 0.75)
                page.insert_text(fitz.Point(r.x0, r.y1 - 2), replace_text, fontsize=f_size)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)


def add_image_to_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    image_path: Union[str, Path],
    page_num: int,
    x: float,
    y: float,
    width: float,
    height: float,
) -> str:
    """Inserts an image or digital signature onto the specified page."""
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    if page_num < 1 or page_num > len(doc):
        doc.close()
        raise ValueError(f"Page number {page_num} out of bounds.")

    page = doc[page_num - 1]
    rect = fitz.Rect(x, y, x + width, y + height)
    page.insert_image(rect, filename=str(image_path))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)


def add_shape_to_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    page_num: int,
    shape_type: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke_color: str = "#0284c7",
    fill_color: Optional[str] = None,
    width: float = 2.0,
) -> str:
    """Draws a shape (rect, line, circle) onto the specified page."""
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    if page_num < 1 or page_num > len(doc):
        doc.close()
        raise ValueError("Page out of range.")

    page = doc[page_num - 1]
    s_rgb = hex_to_rgb_tuple(stroke_color)
    f_rgb = hex_to_rgb_tuple(fill_color) if fill_color else None

    if shape_type == "rect":
        rect = fitz.Rect(x1, y1, x2, y2)
        page.draw_rect(rect, color=s_rgb, fill=f_rgb, width=width)
    elif shape_type == "line":
        p1 = fitz.Point(x1, y1)
        p2 = fitz.Point(x2, y2)
        page.draw_line(p1, p2, color=s_rgb, width=width)
    elif shape_type == "circle":
        rect = fitz.Rect(x1, y1, x2, y2)
        page.draw_oval(rect, color=s_rgb, fill=f_rgb, width=width)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)


def annotate_pdf_text(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    page_num: int,
    annot_type: str,  # "highlight", "underline", "strikeout"
    search_text: str,
) -> str:
    """Adds highlighting, underline, or strikeout to text matches on a page."""
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    if page_num < 1 or page_num > len(doc):
        doc.close()
        raise ValueError("Page out of range.")

    page = doc[page_num - 1]
    rects = page.search_for(search_text)
    for r in rects:
        if annot_type == "highlight":
            page.add_highlight_annot(r)
        elif annot_type == "underline":
            page.add_underline_annot(r)
        elif annot_type == "strikeout":
            page.add_strikeout_annot(r)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)


def redact_pdf_area(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    page_num: int,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    fill_color: str = "#000000",
) -> str:
    """Permanently blacks out and removes underlying text/vectors in specified bounding box."""
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    if page_num < 1 or page_num > len(doc):
        doc.close()
        raise ValueError("Page out of range.")

    page = doc[page_num - 1]
    rect = fitz.Rect(x1, y1, x2, y2)
    rgb = hex_to_rgb_tuple(fill_color)
    page.add_redact_annot(rect, fill=rgb)
    page.apply_redactions()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)


def apply_edit_batch(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    operations: List[Dict[str, Any]],
) -> str:
    """
    Applies a batch of editing actions (text additions, redactions, signatures, shapes)
    in a single atomic write.
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)

    for op in operations:
        op_type = op.get("type")
        p_num = int(op.get("page", 1))
        if p_num < 1 or p_num > total_pages:
            continue
        page = doc[p_num - 1]

        if op_type == "text":
            text = op.get("text", "")
            x = float(op.get("x", 50))
            y = float(op.get("y", 50))
            fontsize = float(op.get("fontsize", 14))
            color = op.get("color", "#0f172a")
            page.insert_text(fitz.Point(x, y), text, fontsize=fontsize, color=hex_to_rgb_tuple(color))

        elif op_type == "redact":
            x1 = float(op.get("x1", 50))
            y1 = float(op.get("y1", 50))
            x2 = float(op.get("x2", 200))
            y2 = float(op.get("y2", 100))
            color = op.get("color", "#000000")
            page.add_redact_annot(fitz.Rect(x1, y1, x2, y2), fill=hex_to_rgb_tuple(color))

        elif op_type == "image":
            img_path = op.get("image_path")
            if img_path and Path(img_path).exists():
                x = float(op.get("x", 50))
                y = float(op.get("y", 50))
                w = float(op.get("width", 150))
                h = float(op.get("height", 80))
                page.insert_image(fitz.Rect(x, y, x + w, y + h), filename=str(img_path))

        elif op_type == "shape":
            s_type = op.get("shape", "rect")
            x1 = float(op.get("x1", 50))
            y1 = float(op.get("y1", 50))
            x2 = float(op.get("x2", 200))
            y2 = float(op.get("y2", 100))
            stroke = op.get("stroke", "#0284c7")
            fill = op.get("fill")
            width = float(op.get("width", 2.0))
            s_rgb = hex_to_rgb_tuple(stroke)
            f_rgb = hex_to_rgb_tuple(fill) if fill else None
            if s_type == "rect":
                page.draw_rect(fitz.Rect(x1, y1, x2, y2), color=s_rgb, fill=f_rgb, width=width)
            elif s_type == "line":
                page.draw_line(fitz.Point(x1, y1), fitz.Point(x2, y2), color=s_rgb, width=width)
            elif s_type == "circle":
                page.draw_oval(fitz.Rect(x1, y1, x2, y2), color=s_rgb, fill=f_rgb, width=width)

        elif op_type == "highlight":
            stext = op.get("search_text", "")
            if stext:
                for r in page.search_for(stext):
                    page.add_highlight_annot(r)

    # Apply all pending redactions across all pages
    for p in doc:
        p.apply_redactions()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=3, deflate=True)
    doc.close()
    return str(output_path)
