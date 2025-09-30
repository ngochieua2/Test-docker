from sqlalchemy import Column, String, DateTime, UUID, PrimaryKeyConstraint, ForeignKeyConstraint, Index
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from app.models.user import User

class ChatThread(Base):
    __tablename__ = "ChatThreads"
    
    id = Column("Id", UUID)
    user_id = Column("UserId", UUID, nullable=False)
    thread_name = Column("ThreadName", String(256), nullable=True)
    created_by = Column("CreatedBy", UUID, nullable=False)
    created_on = Column("CreatedOn", DateTime(timezone=True), nullable=False)
    last_modified_by = Column("LastModifiedBy", UUID, nullable=True)
    last_modified_on = Column("LastModifiedOn", DateTime(timezone=True), nullable=True)
    import_data = relationship("ImportData", back_populates="chat_thread", cascade="all, delete-orphan")

    __table_args__ = (
        PrimaryKeyConstraint('Id', 'UserId', name='pk_chatthreads_id_userid'),
        ForeignKeyConstraint(['UserId'], ['Users.Id'], name='fk_chatthreads_users'),
        Index('ix_chatthreads_id', 'Id'),
        Index('ix_chatthreads_userid', 'UserId')
    )