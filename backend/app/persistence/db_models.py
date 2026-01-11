from sqlalchemy import UniqueConstraint, String, Text, DateTime, CheckConstraint
from datetime import datetime
from typing import Literal
import uuid
from sqlalchemy.dialects.postgresql import UUID                                                                                                                    
from sqlalchemy.orm import Mapped, mapped_column  

from .db import Base


class UploadedFileRecord(Base):
    __tablename__ = "uploaded_files"
    __table_args__ = (
        UniqueConstraint("file_hash", name="uq_uploaded_files_file_hash"),
        CheckConstraint("source IN ('uploaded', 'system')", name="ck_uploaded_files_source_allowed")
        )
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[Literal["uploaded", "system"]] = mapped_column(String(16), nullable=False)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)