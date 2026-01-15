import random
from typing import List, Optional
from urllib.parse import quote

from fastapi import HTTPException

from ...shared.crypto import sha256_hex

from ..llm.service import LlmUnavailableError, ask_llm
from ...shared.config import settings

from ...cache import Cache
from ...types import FileRef as DomainFileRef, UploadedFile
from .correlation import SystemFileManager
from ...persistence.base import FileRepository
from .schemas import ChatResponse, FileRef as ResponseFileRef


MOCK_ANSWERS = [
    "My model is on a coffee break—try again in a moment while I reconnect.",
    "LLM signal is weak right now. Give it another go shortly.",
    "Temporary outage in brainpower. Retrying usually helps.",
    "Still waiting for the facts to load. Ping me again and I will fetch them.",
    "Oops, the model blinked. A quick retry should bring the real answer.",
    "Running on sarcasm instead of data; try again and I will behave.",
    "Currently experiencing a wisdom brownout. Please ask again in a beat.",
    "Debugging my thoughts—resend and I will give you a proper answer.",
]


class ChatService:

    def __init__(
        self,
        cache: Cache,
        system_files: SystemFileManager,
        document_repo: FileRepository,
    ):
        self.cache = cache
        self.system_files = system_files
        self.document_repo = document_repo

    async def send_message(
        self, question: str, uploaded_files: List[UploadedFile], use_llm: bool = True
    ) -> ChatResponse:

        stripped_question_text = self._validate_question(question)
        await self.document_repo.persist_uploads(uploaded_files)
        files_memory_fingerprint = await self.document_repo.get_files_fingerprint()
        cache_key = self._build_cache_key(stripped_question_text, uploaded_files, files_memory_fingerprint, use_llm)

        cached_response = await self._get_cached_response(cache_key)
        if cached_response:
            return cached_response

        answer = (
            await self._ask_llm_model(stripped_question_text)
            if use_llm
            else self._pick_mock_answer()
        )
        file_refs = await self._collect_file_references(stripped_question_text)

        response = self._build_response(answer, file_refs, cache_hit=False)
        await self.cache.set(cache_key, response.model_dump(mode="json"))
        return response

    def _validate_question(self, question: str) -> str:
        if not question or not question.strip():
            raise HTTPException(status_code=400, detail="Question is required")
        return question.strip()

    def _build_cache_key(
        self,
        question: str,
        uploaded_files: List[UploadedFile],
        files_memory_fingerprint: str,
        use_llm: bool,
    ) -> str:
        mode = "llm" if use_llm else "mock"
        file_hashes = sorted(file.file_hash for file in uploaded_files)
        joined_hashes = "|".join(file_hashes)
        return sha256_hex(f"mode:{mode}|q:{question.lower()}|files:{joined_hashes}|mem:{files_memory_fingerprint}")

    async def _get_cached_response(self, cache_key: str) -> Optional[ChatResponse]:
        cached_chat_response = await self.cache.get(cache_key)
        if not cached_chat_response:
            return None
        cached_file_refs = cached_chat_response.get("referenced_files") or []
        validated_file_refs = [
            ResponseFileRef.model_validate(file_ref) for file_ref in cached_file_refs
        ]
        return ChatResponse(
            answer=cached_chat_response.get("answer", ""),
            referenced_files=validated_file_refs,
            cache_hit=True,
        )

    def _build_response(
        self,
        answer: str,
        referenced_files: List[DomainFileRef],
        cache_hit: bool,
    ) -> ChatResponse:
        file_refs = [
            ResponseFileRef(
                name=file.name,
                source=file.source,
                url=self._build_file_url(file),
            )
            for file in referenced_files
        ]
        return ChatResponse(
            answer=answer,
            referenced_files=file_refs,
            cache_hit=cache_hit,
        )

    async def _ask_llm_model(self, question: str) -> str:
        try:
            answer = await ask_llm(
                question, settings.ollama_base_url, settings.ollama_model
            )
        except LlmUnavailableError as exc:
            raise HTTPException(
                status_code=503,
                detail="LLM unavailable. Please try again later or switch to mock answers.",
            ) from exc

        stripped_answer = answer.strip()
        if stripped_answer:
            return stripped_answer
        return self._pick_mock_answer()

    def _pick_mock_answer(self) -> str:
        return random.choice(MOCK_ANSWERS)

    async def _collect_file_references(self, question: str) -> list[DomainFileRef]:
        file_refs = []
        file_refs += await self.document_repo.related_files_from_memory(question)
        file_refs += self.system_files.list_files()
        return file_refs

    def _build_file_url(self, file_ref: DomainFileRef) -> str:
        if not file_ref.file_id:
            raise HTTPException(status_code=500, detail="Missing file id")
        return f"/api/files/{quote(file_ref.file_id, safe='')}"
