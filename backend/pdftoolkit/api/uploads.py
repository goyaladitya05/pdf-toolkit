"""Upload validation and PDF response helpers."""

from __future__ import annotations

import io
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from ..config import MAX_UPLOAD_BYTES


async def read_pdf_upload(file: UploadFile) -> bytes:
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a .pdf file.")
    data = await file.read()
    if not data:
        raise HTTPException(400, "The uploaded file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, f"File exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit.")
    return data


def pdf_response(data: bytes, original_name: str | None, suffix: str) -> StreamingResponse:
    stem = Path(original_name or "document.pdf").stem
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{stem}-{suffix}.pdf"'},
    )
