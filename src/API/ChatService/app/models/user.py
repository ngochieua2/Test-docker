from sqlalchemy import Column, String, DateTime, UUID, PrimaryKeyConstraint, Index

from app.db.base_class import Base


class User(Base):
    __tablename__ = "Users"

    id = Column("Id", UUID)
    first_name = Column("FirstName", String(256), nullable=False)
    last_name = Column("LastName", String(256), nullable=False)
    email = Column("Email", String(256), nullable=False)
    phone_number = Column("PhoneNumber", String(20), nullable=True)
    created_on = Column("CreatedOn", DateTime(timezone=True), nullable=False)
    created_by = Column("CreatedBy", UUID, nullable=False)
    last_modified_on = Column("LastModifiedOn", DateTime(timezone=True), nullable=True)
    last_modified_by = Column("LastModifiedBy", UUID, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('Id', name='pk_users_id'),
        Index('ix_users_id',  'Id'),
        Index('ix_users_email',  'Email'),
        Index('ix_users_phonenumber',  'PhoneNumber'),
    )
