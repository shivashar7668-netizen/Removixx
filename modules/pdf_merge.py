"""
Removix PDF Engine - Merge PDF Module
-------------------------------------
Merges multiple PDF documents into a single unified PDF.
Preserves bookmarks, vector graphics, fonts, and annotations.
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


def merge_pdfs(pdf_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> str:
    """
    Merges multiple PDF files into one output PDF in the order provided.
    Returns the string path of the generated PDF.
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    if not pdf_paths or len(pdf_paths) < 2:
        raise ValueError("At least two PDF files are required for merging.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    merged_doc = fitz.open()
    open_docs = []

    try:
        for p in pdf_paths:
            path_obj = Path(p)
            if not path_obj.exists():
                continue
            src_doc = fitz.open(str(path_obj))
            open_docs.append(src_doc)
            merged_doc.insert_pdf(src_doc)

        if len(merged_doc) == 0:
            raise ValueError("No valid PDF pages were found to merge.")

        merged_doc.save(str(output_path), garbage=3, deflate=True)
        return str(output_path)
    finally:
        for d in open_docs:
            try:
                d.close()
            except Exception:
                pass
        try:
            merged_doc.close()
        except Exception:
            pass
