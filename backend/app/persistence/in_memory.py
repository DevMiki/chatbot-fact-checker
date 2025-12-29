import asyncio
from dataclasses import dataclass
import hashlib
from typing import Tuple
from ..features.chat.correlation import FileMemory
from ..types import FileRef, UploadedFile
from .base import FileRepository


@dataclass
class FileMemoryEntry:
    ref: FileRef
    upload_path: str
    extracted_text: str


class InMemoryFileRepository(FileRepository):
    def __init__(self, file_memory: FileMemory | None = None):
        self.file_memory = FileMemory()
        self._lock = asyncio.Lock()
        self._file_memory_entries: dict[str, FileMemoryEntry] = {}

    async def persist_uploads(self, uploaded_files: list[UploadedFile]) -> None:
        async with self._lock:
            for file in uploaded_files:
                if not file.file_path:
                    continue
                self._file_memory_entries[file.file_hash] = FileMemoryEntry(
                    ref=file.ref,
                    upload_path=file.file_path,
                    extracted_text=file.file_text or "",
                )

    async def get_files_fingerprint(self) -> str:
        async with self._lock:
            combined_memory_entries = "|".join(sorted(self._file_memory_entries.keys()))
        return hashlib.sha256(combined_memory_entries.encode("utf-8")).hexdigest()

    async def related_files_from_memory(self, question: str) -> list[FileRef]:
        MINIMUM_SCORE_TO_RELATE_FILE = 3
        question_keywords = self.file_memory.extract_keywords(question)
        if not question_keywords:
            return []

        async with self._lock:
            hashes_and_memory_entries: list[Tuple[str, FileMemoryEntry]] = list(
                self._file_memory_entries.items()
            )

        scores_and_files: list[Tuple[int, FileRef]] = []
        for _, file_memory in hashes_and_memory_entries:
            question_file_score = self.file_memory._get_question_file_score(
                file_memory.extracted_text, question_keywords
            )
            if question_file_score > MINIMUM_SCORE_TO_RELATE_FILE:
                scores_and_files.append((question_file_score, file_memory.ref))

        scores_and_files.sort(key=lambda pair: pair[0], reverse=True)
        return [file_ref for _, file_ref in scores_and_files]
