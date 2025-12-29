import asyncio
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set, Tuple

from reportlab.pdfgen import canvas

from ...types import FileRef, UploadedFile
from ..files.resolver import build_file_id

SampleFile = tuple[str, str, str]


@dataclass
class FileMemoryEntry:
    ref: FileRef
    upload_path: str
    extracted_text: str


class FileMemory:

    def __init__(self):
        self._file_memory_entries: dict[str, FileMemoryEntry] = {}
        self._lock = asyncio.Lock()

    def extract_keywords(self, question: str) -> Set[str]:
        words = re.findall(r"[a-zA-Z0-9]+", question.lower())
        return {word for word in words if len(word) >= 3}

    def _get_question_file_score(
        self, file_memory_extracted_text: str, question_keywords: Set[str]
    ) -> int:
        if not file_memory_extracted_text:
            return 0
        lowered_extracted_text = file_memory_extracted_text.lower()
        return sum(
            1 for keyword in question_keywords if keyword in lowered_extracted_text
        )


class SystemFileManager:

    _SAMPLE_FILES: list[SampleFile] = [
        ("product_faq.pdf", "Product FAQ", "Common questions and answers."),
        ("security_notes.pdf", "Security Notes", "Security best practices."),
    ]

    def __init__(self, base_dir: str):
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._ensure_sample_files_exist()

    def _has_any_pdf(self) -> bool:
        return any(self.base_path.glob("*.pdf"))

    def _ensure_sample_files_exist(self) -> None:
        if self._has_any_pdf():
            return

        for filename, title, body in self._SAMPLE_FILES:
            self._create_pdf(self.base_path / filename, title, body)

    def _create_pdf(self, path: Path, title: str, body: str) -> None:
        pdf = canvas.Canvas(str(path))

        pdf.setFont("Helvetica", 14)
        pdf.drawString(72, 780, title)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(72, 760, body)

        pdf.save()

    def list_files(self) -> List[FileRef]:
        sorted_pdfs = sorted(self.base_path.glob("*.pdf"))
        return [
            FileRef(
                name=p.name,
                source="system",
                file_id=build_file_id("system", p.name),
            )
            for p in sorted_pdfs
        ]
