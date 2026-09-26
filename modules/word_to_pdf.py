"""
Removix PDF Engine - Word to PDF Module
---------------------------------------
Converts Microsoft Word documents (.docx, .doc) to PDF.
- Uses LibreOffice in headless mode if available.
- Falls back to built-in python-docx + vector typography rendering engine.
"""

import html
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Union

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

try:
    import docx
except ImportError:
    docx = None


def find_libreoffice_binary() -> Union[str, None]:
    """Attempts to locate the LibreOffice binary on the host machine."""
    candidates = ["soffice", "libreoffice"]
    for c in candidates:
        found = shutil.which(c)
        if found:
            return found

    if sys.platform == "win32":
        default_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\LibreOffice\program\soffice.exe"),
        ]
        for p in default_paths:
            if Path(p).is_file():
                return p
    return None


def convert_docx_with_python_engine(docx_path: Path, output_pdf_path: Path) -> str:
    """
    High-fidelity built-in DOCX to PDF converter using python-docx and PyMuPDF Story.
    Handles headings, formatted text runs (bold, italic, underline), lists, and tables.
    """
    if docx is None or fitz is None:
        raise RuntimeError("Document processing dependencies are not available.")

    doc = docx.Document(str(docx_path))

    html_parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>",
        "body { font-family: sans-serif; font-size: 11pt; line-height: 1.5; color: #1e293b; margin: 0; padding: 0; }",
        "h1 { font-size: 20pt; font-weight: 800; color: #0f172a; margin-top: 18pt; margin-bottom: 8pt; }",
        "h2 { font-size: 15pt; font-weight: 700; color: #1e293b; margin-top: 14pt; margin-bottom: 6pt; }",
        "h3 { font-size: 13pt; font-weight: 700; color: #334155; margin-top: 10pt; margin-bottom: 4pt; }",
        "p { margin: 6pt 0; text-align: left; }",
        "table { width: 100%; border-collapse: collapse; margin: 12pt 0; }",
        "th, td { border: 1px solid #cbd5e1; padding: 6pt 10pt; text-align: left; font-size: 10pt; }",
        "th { background-color: #f1f5f9; font-weight: 700; }",
        "</style></head><body>",
    ]

    for p in doc.paragraphs:
        if not p.text.strip():
            html_parts.append("<p>&nbsp;</p>")
            continue

        style_name = (p.style.name or "").lower()
        tag = "p"
        if "heading 1" in style_name or "title" in style_name:
            tag = "h1"
        elif "heading 2" in style_name:
            tag = "h2"
        elif "heading 3" in style_name:
            tag = "h3"

        p_inner = ""
        for r in p.runs:
            run_txt = html.escape(r.text)
            if r.bold and r.italic:
                run_txt = f"<b><i>{run_txt}</i></b>"
            elif r.bold:
                run_txt = f"<b>{run_txt}</b>"
            elif r.italic:
                run_txt = f"<i>{run_txt}</i>"
            if r.underline:
                run_txt = f"<u>{run_txt}</u>"
            p_inner += run_txt

        html_parts.append(f"<{tag}>{p_inner}</{tag}>")

    # Tables support
    for tbl in doc.tables:
        html_parts.append("<table>")
        for row_idx, row in enumerate(tbl.rows):
            html_parts.append("<tr>")
            for cell in row.cells:
                cell_tag = "th" if row_idx == 0 else "td"
                cell_text = html.escape(cell.text.strip())
                html_parts.append(f"<{cell_tag}>{cell_text}</{cell_tag}>")
            html_parts.append("</tr>")
        html_parts.append("</table>")

    html_parts.append("</body></html>")
    full_html = "".join(html_parts)

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    story = fitz.Story(html=full_html)
    writer = fitz.DocumentWriter(str(output_pdf_path))
    rect = fitz.Rect(54, 54, 558, 738)  # Standard Letter/A4 margin area

    more = 1
    while more:
        device = writer.begin_page(rect)
        more, _ = story.place(rect)
        story.draw(device, rect)
        writer.end_page()
    writer.close()

    return str(output_pdf_path)


def word_to_pdf(word_path: Union[str, Path], output_path: Union[str, Path]) -> str:
    """
    Converts a Word document to a PDF file.
    Tries LibreOffice headless mode if present; otherwise uses the native python-docx engine.
    """
    word_path = Path(word_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not word_path.exists():
        raise FileNotFoundError(f"File not found: {word_path}")

    # Check for LibreOffice binary
    soffice_path = find_libreoffice_binary()
    if soffice_path:
        out_dir = output_path.parent
        cmd = [
            soffice_path,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(word_path),
        ]
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW

        res = subprocess.run(cmd, capture_output=True, text=True, creationflags=creationflags)
        expected_pdf = out_dir / f"{word_path.stem}.pdf"
        if expected_pdf.is_file():
            if expected_pdf != output_path:
                shutil.move(str(expected_pdf), str(output_path))
            return str(output_path)

    # Fallback to python native engine for .docx files
    ext = word_path.suffix.lower()
    if ext == ".docx":
        return convert_docx_with_python_engine(word_path, output_path)
    elif ext == ".doc":
        raise ValueError("Legacy .doc format requires DOCX conversion or office environment.")
    else:
        raise ValueError(f"Unsupported document format: {ext}")
