"""
Removix PDF Engine - Delete Pages Module
----------------------------------------
Removes selected pages from a PDF document and exports the cleaned PDF.
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


def delete_pdf_pages(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    pages_to_remove_str: str,
) -> str:
    """
    Removes pages specified in pages_to_remove_str (e.g. '1, 3, 5-8') from the PDF.
    Returns the output PDF file path.
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

    # Parse 1-based page numbers into 0-based set
    remove_indices = set()
    parts = [p.strip() for p in pages_to_remove_str.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) == 2 and bounds[0].strip().isdigit() and bounds[1].strip().isdigit():
                start = max(1, int(bounds[0].strip()))
                end = min(total_pages, int(bounds[1].strip()))
                if start <= end:
                    for p in range(start, end + 1):
                        remove_indices.add(p - 1)
        elif part.isdigit():
            val = int(part)
            if 1 <= val <= total_pages:
                remove_indices.add(val - 1)

    if not remove_indices:
        raise ValueError("No valid pages were specified for deletion.")

    if len(remove_indices) >= total_pages:
        raise ValueError("Cannot delete all pages of the document. At least one page must remain.")

    try:
        out_doc = fitz.open()
        for i in range(total_pages):
            if i not in remove_indices:
                out_doc.insert_pdf(doc, from_page=i, to_page=i)

        out_doc.save(str(output_path), garbage=3, deflate=True)
        out_doc.close()
        return str(output_path)
    finally:
        try:
            doc.close()
        except Exception:
            pass
