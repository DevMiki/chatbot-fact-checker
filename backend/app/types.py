from dataclasses import dataclass
from typing import Literal


@dataclass
class FileRef:
    name: str
    source: Literal["uploaded", "system"]
    file_id: str


@dataclass
class UploadedFile:
    ref: FileRef
    file_hash: str
    file_text: str = ""
    file_path: str = ""
