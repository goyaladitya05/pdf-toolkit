import io

import pikepdf
import pytest

from pdftoolkit.core import (
    AlreadyEncryptedError,
    InvalidPdfError,
    WrongPasswordError,
    decrypt,
    encrypt,
)


@pytest.fixture
def plain_pdf() -> bytes:
    pdf = pikepdf.new()
    pdf.add_blank_page(page_size=(200, 200))
    buf = io.BytesIO()
    pdf.save(buf)
    return buf.getvalue()


def test_encrypt_requires_password(plain_pdf):
    encrypted = encrypt(plain_pdf, "secret")
    with pytest.raises(pikepdf.PasswordError):
        pikepdf.open(io.BytesIO(encrypted))


def test_round_trip(plain_pdf):
    encrypted = encrypt(plain_pdf, "secret")
    decrypted = decrypt(encrypted, "secret")
    pikepdf.open(io.BytesIO(decrypted))  # opens without a password


def test_wrong_password(plain_pdf):
    encrypted = encrypt(plain_pdf, "secret")
    with pytest.raises(WrongPasswordError):
        decrypt(encrypted, "nope")


def test_double_encrypt_blocked(plain_pdf):
    encrypted = encrypt(plain_pdf, "secret")
    with pytest.raises(AlreadyEncryptedError):
        encrypt(encrypted, "other")


def test_invalid_pdf():
    with pytest.raises(InvalidPdfError):
        encrypt(b"not a pdf", "secret")


def test_empty_password_rejected(plain_pdf):
    with pytest.raises(ValueError):
        encrypt(plain_pdf, "")
