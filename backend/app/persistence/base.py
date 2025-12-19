from abc import ABC, abstractmethod

from ..types import FileRef, UploadedFile


class FileRepository(ABC):
    @abstractmethod
    async def persist_uploads(self, uploads: list[UploadedFile]) -> None: ...

    @abstractmethod
    async def fingerprint(self) -> str: ...

    @abstractmethod
    async def related_files_from_memory(
        self, question: str,
    ) -> list[FileRef]: ...
