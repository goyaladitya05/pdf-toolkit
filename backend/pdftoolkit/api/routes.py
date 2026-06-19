from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from ..core import (
    AlreadyEncryptedError,
    InvalidPdfError,
    WrongPasswordError,
    decrypt,
    encrypt,
)
from .uploads import pdf_response, read_pdf_upload

router = APIRouter(prefix="/api")


@router.post("/encrypt")
async def encrypt_route(
    file: UploadFile = File(...),
    password: str = Form(...),
) -> StreamingResponse:
    if not password:
        raise HTTPException(400, "A password is required to encrypt.")
    data = await read_pdf_upload(file)
    try:
        result = encrypt(data, password)
    except AlreadyEncryptedError:
        raise HTTPException(400, "This PDF is already password-protected. Decrypt it first.")
    except InvalidPdfError:
        raise HTTPException(400, "Could not read this file as a PDF.")
    return pdf_response(result, file.filename, "encrypted")


@router.post("/decrypt")
async def decrypt_route(
    file: UploadFile = File(...),
    password: str = Form(...),
) -> StreamingResponse:
    data = await read_pdf_upload(file)
    try:
        result = decrypt(data, password)
    except WrongPasswordError:
        raise HTTPException(400, "Wrong or missing password for this PDF.")
    except InvalidPdfError:
        raise HTTPException(400, "Could not read this file as a PDF.")
    return pdf_response(result, file.filename, "decrypted")
