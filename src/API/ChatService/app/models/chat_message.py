from sqlalchemy import Column, DateTime, UUID, String, PrimaryKeyConstraint, ForeignKeyConstraint, Index
from sqlalchemy import Column, Enum as SQLEnum
from app.enums.chat_role import ChatRole

from app.db.base_class import Base

from app.models.user import User
from app.models.chat_thread import ChatThread


class ChatMessage(Base):
    __tablename__ = "ChatMessages"
    
    id = Column("Id", UUID)
    thread_id = Column("ThreadId", UUID, nullable=False)
    user_id = Column("UserId", UUID, nullable=False)
    chat_role = Column("ChatRole", SQLEnum(ChatRole, name="ChatRoleEnum"), nullable=False)
    chat_message = Column("ChatMessage", String, nullable = False)
    summerize_message = Column("SummerizeMessage", String, nullable = True)
    response_id = Column("ResponseId", String, nullable = True)
    created_by = Column("CreatedBy", UUID, nullable=False)
    created_on = Column("CreatedOn", DateTime(timezone=True), nullable=False)
    last_modified_by = Column("LastModifiedBy", UUID, nullable=True)
    last_modified_on = Column("LastModifiedOn", DateTime(timezone=True), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('Id', 'ThreadId', name='pk_chatmessages_id_threadid'),
        ForeignKeyConstraint(['ThreadId', 'UserId'], ['ChatThreads.Id', 'ChatThreads.UserId'], name='fk_chatmessages_threadchats'),
        Index('ix_chatmessages_id', 'Id'),
        Index('ix_chatmessages_threadid', 'ThreadId'),
        Index('ix_chatmessages_responseid', 'ResponseId')
    )