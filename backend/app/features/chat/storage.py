import re
import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
from starlette.concurrency import run_in_threadpool

from ...shared.crypto import sha256_hex

from ...shared.config import settings
from ...shared.object_storage import MinioObjectStorage
from ...types import FileRef, UploadedFile
from ..files.resolver import build_file_id

ALLOWED_EXTENSIONS = {".pdf"}
ALLOWED_MIME_TYPES = {"application/pdf"}
PDF_MAGIC_HEADER = b"%PDF"


def ensure_storage_dirs() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.system_files_dir).mkdir(parents=True, exist_ok=True)


async def persist_uploaded_pdf(file: UploadFile, object_storage: MinioObjectStorage) -> UploadedFile:
    filename, file_byte_content = await validate_upload(file)

    upload_name = _build_upload_storage_name(filename)
    await run_in_threadpool(object_storage.put_pdf, upload_name, file_byte_content)
    file_id = build_file_id("uploaded", upload_name)
    file_ref = FileRef(filename, "uploaded", file_id)
    file_hash = sha256_hex(file_byte_content)
    extracted_text = _extract_file_text(file_byte_content)
    return UploadedFile(file_ref, file_hash, extracted_text, str(upload_name))


async def validate_upload(file: UploadFile) -> tuple[str, bytes]:
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="File must have a name")
    if not _is_allowed_extension(filename):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    if not _is_allowed_mime(file.content_type):
        raise HTTPException(
            status_code=400,
            detail="Content-Type must be application/pdf",
        )

    content = await _read_with_limit(file, int(settings.max_upload_mb * 1024 * 1024))
    if not content.startswith(PDF_MAGIC_HEADER):
        raise HTTPException(
            status_code=400,
            detail="File content is not a valid PDF file",
        )

    return filename, content


async def _read_with_limit(file: UploadFile, max_bytes: int, chunk_size: int = 1024 * 1024):
    total = 0
    parts: list[bytes] = []

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Limit is {max_bytes / (1024 * 1024):.0f} MB",
            )
        parts.append(chunk)
    return b"".join(parts)


def _is_allowed_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def _is_allowed_mime(content_type) -> bool:
    mime = (content_type or "").split(";")[0].strip().lower()
    return mime in ALLOWED_MIME_TYPES


def _build_upload_storage_name(original_filename: str) -> str:
    safe_name = sanitize_filename(original_filename)
    return f"{uuid.uuid4().hex}_{safe_name}"


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", filename).strip("._")
    fallback_stamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    return cleaned or f"uploaded_file_{fallback_stamp}.pdf"


def _write_file(upload_path: Path, content: bytes) -> None:
    with open(upload_path, "wb") as file:
        file.write(content)


def _extract_file_text(
        file_bytes: bytes, max_pages: int = 5, max_chars: int = 10_000
) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
        final_pages_text: list[str] = []

        for page in reader.pages[:max_pages]:
            current_page_text = page.extract_text() or ""
            if current_page_text:
                final_pages_text.append(current_page_text)

        return "\n".join(final_pages_text).strip()[:max_chars]
    except Exception:
        return ""
