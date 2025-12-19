from pathlib import Path

from fastapi import HTTPException

ALLOWED_SOURCES = {"uploaded", "system"}
FILE_ID_SEPARATOR = "__"


def build_file_id(source: str, filename: str) -> str:
    return f"{source}{FILE_ID_SEPARATOR}{filename}"


def parse_file_id(file_id: str) -> tuple[str, str]:
    if not file_id or FILE_ID_SEPARATOR not in file_id:
        raise HTTPException(status_code=400, detail="Invalid file id")
    source, filename = file_id.split(FILE_ID_SEPARATOR, 1)
    if source not in ALLOWED_SOURCES:
        raise HTTPException(status_code=400, detail="Invalid file id")
    if not _is_safe_filename(filename):
        raise HTTPException(status_code=400, detail="Invalid file id")
    return source, filename


def _is_safe_filename(filename: str) -> bool:
    if not filename:
        return False
    if any(sep in filename for sep in ("/", "\\")):
        return False
    if Path(filename).name != filename:
        return False
    if Path(filename).suffix.lower() != ".pdf":
        return False
    return True


class FileResolver:

    def __init__(self, upload_dir: str, system_files_dir: str):
        self.upload_dir = Path(upload_dir)
        self.system_files_dir = Path(system_files_dir)

    def resolve(self, file_id: str) -> Path:
        source, filename = parse_file_id(file_id)
        base_dir = self.upload_dir if source == "uploaded" else self.system_files_dir
        base_dir = base_dir.resolve()
        candidate = (base_dir / filename).resolve()
        if base_dir not in candidate.parents and candidate != base_dir:
            raise HTTPException(status_code=400, detail="Invalid file id")
        if not candidate.exists() or not candidate.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        return candidate
