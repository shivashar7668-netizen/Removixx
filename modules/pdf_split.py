"""
Removix PDF Engine - Split PDF Module
-------------------------------------
Splits a PDF into individual pages (ZIP) or extracts specified page ranges into a new PDF.
"""

import zipfile
from pathlib import Path
from typing import List, Tuple, Union

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


def parse_page_ranges(range_str: str, max_pages: int) -> List[int]:
    """
    Parses a page range string (e.g. '1-3, 5, 8-10') into 0-indexed page numbers.
    """
    pages = set()
    parts = [p.strip() for p in range_str.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) == 2 and bounds[0].strip().isdigit() and bounds[1].strip().isdigit():
                start = max(1, int(bounds[0].strip()))
                end = min(max_pages, int(bounds[1].strip()))
                if start <= end:
                    for p in range(start, end + 1):
                        pages.add(p - 1)
        elif part.isdigit():
            val = int(part)
            if 1 <= val <= max_pages:
                pages.add(val - 1)
    return sorted(list(pages))


def split_pdf(
    pdf_path: Union[str, Path],
    output_dir: Union[str, Path],
    split_mode: str = "all",
    range_str: str = "",
) -> Tuple[str, bool]:
    """
    Splits a PDF file:
    - 'all': Extracts every page as an individual PDF and packages them into a ZIP archive.
    - 'range': Extracts specified page range(s) into a single new PDF document.
    Returns (result_filepath, is_zip).
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        raise ValueError("The provided PDF has 0 pages.")

    base_stem = pdf_path.stem

    try:
        if split_mode == "range" and range_str.strip():
            page_indices = parse_page_ranges(range_str, total_pages)
            if not page_indices:
                raise ValueError("No valid pages found in the specified range.")

            out_doc = fitz.open()
            for p_idx in page_indices:
                out_doc.insert_pdf(doc, from_page=p_idx, to_page=p_idx)

            out_pdf_path = output_dir / f"{base_stem}_extracted.pdf"
            out_doc.save(str(out_pdf_path), garbage=3, deflate=True)
            out_doc.close()
            return str(out_pdf_path), False
        else:
            # Split all pages into individual files & package into ZIP
            extracted_files = []
            for i in range(total_pages):
                single_doc = fitz.open()
                single_doc.insert_pdf(doc, from_page=i, to_page=i)
                page_file = output_dir / f"{base_stem}_page_{i + 1:03d}.pdf"
                single_doc.save(str(page_file), garbage=3, deflate=True)
                single_doc.close()
                extracted_files.append(page_file)

            zip_path = output_dir / f"{base_stem}_split_pages.zip"
            with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
                for f in extracted_files:
                    zf.write(str(f), arcname=f.name)
            return str(zip_path), True
    finally:
        try:
            doc.close()
        except Exception:
            pass
