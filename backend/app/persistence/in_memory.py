from ..features.chat.correlation import FileMemory
from ..types import FileRef, UploadedFile
from .base import FileRepository


class InMemoryFileRepository(FileRepository):
    def __init__(self, file_memory: FileMemory | None = None):
        self._file_memory = file_memory or FileMemory()

    async def persist_uploads(self, uploads: list[UploadedFile]) -> None:
        await self._file_memory.upsert(uploads)

    async def fingerprint(self) -> str:
        return await self._file_memory.fingerprint()

    async def related_files_from_memory(self, question: str) -> list[FileRef]:
        return await self._file_memory.related_files_from_file_memory(question)
