"""
Removix PDF Engine - Rotate PDF Module
--------------------------------------
Rotates all or selected PDF pages by 90, 180, or 270 degrees clockwise or counter-clockwise.
"""

from pathlib import Path
from typing import List, Union

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


def rotate_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    angle: int = 90,
    page_selection: str = "all",
    range_str: str = "",
) -> str:
    """
    Rotates pages of a PDF document by angle (degrees: 90, 180, 270).
    - page_selection: 'all' or 'range'
    - range_str: comma-separated list/ranges if page_selection is 'range'
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    pdf_path = Path(pdf_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        raise ValueError("The provided PDF has 0 pages.")

    try:
        target_pages = set(range(total_pages))
        if page_selection == "range" and range_str.strip():
            target_pages = set()
            for part in range_str.split(","):
                part = part.strip()
                if "-" in part:
                    b = part.split("-")
                    if len(b) == 2 and b[0].isdigit() and b[1].isdigit():
                        s, e = max(1, int(b[0])), min(total_pages, int(b[1]))
                        for p in range(s, e + 1):
                            target_pages.add(p - 1)
                elif part.isdigit():
                    v = int(part)
                    if 1 <= v <= total_pages:
                        target_pages.add(v - 1)

        for i in range(total_pages):
            if i in target_pages:
                current_rot = doc[i].rotation
                new_rot = (current_rot + angle) % 360
                doc[i].set_rotation(new_rot)

        doc.save(str(output_path), garbage=3, deflate=True)
        return str(output_path)
    finally:
        try:
            doc.close()
        except Exception:
            pass
