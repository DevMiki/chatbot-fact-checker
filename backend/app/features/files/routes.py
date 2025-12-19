from fastapi import APIRouter
from fastapi.responses import FileResponse

from ...shared.config import settings
from .resolver import FileResolver

router = APIRouter()
file_resolver = FileResolver(
    upload_dir=settings.upload_dir,
    system_files_dir=settings.system_files_dir,
)


@router.get("/files/{file_id}")
async def get_file(file_id: str) -> FileResponse:
    path = file_resolver.resolve(file_id)
    # Serve PDFs inline so they open in a new tab instead of downloading
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=path.name,
        content_disposition_type="inline",
    )
