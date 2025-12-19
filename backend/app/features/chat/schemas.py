from typing import List

from pydantic import BaseModel


class FileRef(BaseModel):
    name: str | None
    source: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    referenced_files: List[FileRef]
    cache_hit: bool = False
