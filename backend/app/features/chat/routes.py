from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from ...cache import get_cache
from ...shared.config import settings
from .correlation import SystemFileManager
from ...persistence.init import get_file_repository
from .storage import persist_uploaded_pdf
from .schemas import ChatResponse
from .service import ChatService

router = APIRouter()

cache = get_cache()
system_files_manager = SystemFileManager(base_dir=settings.system_files_dir)
file_repository = get_file_repository()
chat_service = ChatService(cache, system_files_manager, file_repository)


def parse_form_bool(value: Optional[str], default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", ""}:
        return False
    return default


@router.post("/chat", response_model=ChatResponse)
async def chat(
    question: str = Form(...),
    use_llm: Optional[str] = Form(None),
    files: list[UploadFile] = File([]),
) -> ChatResponse:
    uploaded_files = [await persist_uploaded_pdf(file) for file in files]
    use_llm_flag = parse_form_bool(use_llm, default=True)
    return await chat_service.send_message(
        question, uploaded_files, use_llm=use_llm_flag
    )
