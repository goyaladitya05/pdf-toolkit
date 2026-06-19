"""Framework-agnostic PDF operations. Each takes bytes and returns bytes."""

from __future__ import annotations

import io

import pikepdf

from .errors import AlreadyEncryptedError, InvalidPdfError, WrongPasswordError


def encrypt(data: bytes, password: str) -> bytes:
    """Return an AES-256 encrypted copy of the PDF."""
    if not password:
        raise ValueError("password is required")
    try:
        pdf = pikepdf.open(io.BytesIO(data))
    except pikepdf.PasswordError as exc:
        raise AlreadyEncryptedError from exc
    except pikepdf.PdfError as exc:
        raise InvalidPdfError from exc

    out = io.BytesIO()
    with pdf:
        pdf.save(out, encryption=pikepdf.Encryption(user=password, owner=password, R=6))
    return out.getvalue()


def decrypt(data: bytes, password: str) -> bytes:
    """Return a copy of the PDF with password protection removed."""
    try:
        pdf = pikepdf.open(io.BytesIO(data), password=password or "")
    except pikepdf.PasswordError as exc:
        raise WrongPasswordError from exc
    except pikepdf.PdfError as exc:
        raise InvalidPdfError from exc

    out = io.BytesIO()
    with pdf:
        pdf.save(out)
    return out.getvalue()
