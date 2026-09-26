"""
Removix PDF Engine - Unlock PDF Module
-------------------------------------
Removes password protection and restrictions from a secured PDF document.
Allows permanent export of the decrypted, unrestricted PDF.
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


def unlock_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path],
    password: str,
) -> str:
    """
    Decrypts a password-protected PDF document and saves an unencrypted copy.
    Returns the string path of the decrypted PDF.
    """
    if fitz is None:
        raise RuntimeError("PDF processing library is not available.")

    pdf_path = Path(pdf_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))

    if not doc.is_encrypted:
        # Document is not encrypted, save a direct copy
        doc.save(str(output_path), garbage=3, deflate=True)
        doc.close()
        return str(output_path)

    try:
        rc = doc.authenticate(password)
        if rc <= 0:
            raise ValueError("Incorrect password. Please verify and try again.")

        doc.save(
            str(output_path),
            encryption=fitz.PDF_ENCRYPT_NONE,
            garbage=3,
            deflate=True,
        )
        return str(output_path)
    finally:
        try:
            doc.close()
        except Exception:
            pass
