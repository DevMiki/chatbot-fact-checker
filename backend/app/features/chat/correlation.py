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

    async def upsert(self, uploaded_files: Iterable[UploadedFile]) -> None:
        async with self._lock:
            for file in uploaded_files:
                if not file.file_path:
                    continue
                self._file_memory_entries[file.file_hash] = FileMemoryEntry(
                    ref=file.ref,
                    upload_path=file.file_path,
                    extracted_text=file.file_text or "",
                )

    async def fingerprint(self) -> str:
        async with self._lock:
            combined = "|".join(sorted(self._file_memory_entries.keys()))
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    async def related_files_from_file_memory(
        self,
        question: str,
    ) -> List[FileRef]:
        MINIMUM_SCORE_TO_RELATE_FILE = 3
        question_keywords = self._extract_keywords(question)
        if not question_keywords:
            return []

        async with self._lock:
            hashes_and_memory_entries: list[Tuple[str, FileMemoryEntry]] = list(
                self._file_memory_entries.items()
            )

        scores_and_files: list[Tuple[int, FileRef]] = []
        for _, file_memory in hashes_and_memory_entries:
            question_file_score = self._get_question_file_score(
                file_memory.extracted_text, question_keywords
            )
            if question_file_score > MINIMUM_SCORE_TO_RELATE_FILE:
                scores_and_files.append((question_file_score, file_memory.ref))

        scores_and_files.sort(key=lambda pair: pair[0], reverse=True)
        return [file_ref for _, file_ref in scores_and_files]

    def _extract_keywords(self, question: str) -> Set[str]:
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
