import uuid
from sqlalchemy import Column, String, DateTime, UUID, PrimaryKeyConstraint, ForeignKeyConstraint, Index
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.chat_thread import ChatThread
from enum import Enum

class ImportStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ImportData(Base):
    __tablename__ = "ImportData"

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FileName = Column(String(256), nullable=True)
    FileUrl = Column(String, nullable=True)
    Status = Column(String(50), nullable=False, default=ImportStatus.PENDING.value)
    UserId = Column(UUID(as_uuid=True), index=True, nullable=False)
    Response = Column(String, nullable=True)
    DataSummary = Column(String, nullable=True)
    CreatedBy = Column(UUID(as_uuid=True), nullable=False)
    CreatedOn = Column(DateTime(timezone=True), nullable=False)
    LastModifiedBy = Column(UUID(as_uuid=True), nullable=True)
    LastModifiedOn = Column(DateTime(timezone=True), nullable=True)
    ThreadId = Column(UUID(as_uuid=True), nullable=False)
    chat_thread = relationship("ChatThread", back_populates="import_data")

    __table_args__ = (
        PrimaryKeyConstraint("Id", name="pk_importdata_id"),
        ForeignKeyConstraint(
            ["ThreadId", "UserId"], ["ChatThreads.Id", "ChatThreads.UserId"],
            name="fk_importdata_threadchats"
        ),
        Index("ix_importdata_id", "Id"),
        Index("ix_importdata_status_createdon", "Status", "CreatedOn"),
    )