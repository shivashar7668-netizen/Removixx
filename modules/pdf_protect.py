"""
Removix PDF Engine - Protect PDF Module
---------------------------------------
Adds military-grade AES-256 password encryption to any PDF document.
Secures document contents from unauthorized viewing and modification.
"""

from pathlib import Path
from typing import Union

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


def protect_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    password: str,
) -> str:
    """
    Encrypts a PDF document with the specified user/owner password using AES-256.
    Returns the string path of the encrypted PDF.
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    if not password:
        raise ValueError("A password must be provided to protect the PDF.")

    pdf_path = Path(pdf_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    if doc.is_encrypted:
        doc.close()
        raise ValueError("This PDF is already password-protected. Please unlock it first.")

    try:
        doc.save(
            str(output_path),
            encryption=fitz.PDF_ENCRYPT_AES_256,
            user_pw=password,
            owner_pw=password,
            garbage=3,
            deflate=True,
        )
        return str(output_path)
    finally:
        try:
            doc.close()
        except Exception:
            pass
