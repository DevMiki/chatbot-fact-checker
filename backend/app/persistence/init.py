from .base import FileRepository
from .in_memory import InMemoryFileRepository

__all__ = ["FileRepository", "InMemoryFileRepository", "get_file_repository"]


def get_file_repository() -> FileRepository:
    return InMemoryFileRepository()
