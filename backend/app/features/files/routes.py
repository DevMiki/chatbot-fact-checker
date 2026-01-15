from fastapi import APIRouter
from starlette.responses import Response
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

from ...shared.config import settings
from .resolver import FileResolver, parse_file_id
from ...shared.object_storage import get_minio_object_storage

router = APIRouter()
file_resolver = FileResolver(
    upload_dir=settings.upload_dir,
    system_files_dir=settings.system_files_dir,
)
minio_object_storage = get_minio_object_storage()


@router.get("/files/{file_id}")
async def get_file(file_id: str) -> Response:
    source, file_name = parse_file_id(file_id)
    # Serve PDFs inline so they open in a new tab instead of downloading
    if source == "system":
        path = file_resolver.resolve(file_id)
        return FileResponse(
            path,
            media_type="application/pdf",
            filename=path.name,
            content_disposition_type="inline",
        )

    file_content = await run_in_threadpool(minio_object_storage.get_pdf_bytes, file_name)
    return Response(
        content=file_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{file_name}"'},
    )
