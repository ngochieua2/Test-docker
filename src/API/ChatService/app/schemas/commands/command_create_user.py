from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4

from app.core.utils.datetime_utils import now_utc

from app.models.user import User

#------------------Command Class-------------------

class create_user_command(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: EmailStr = Field(alias="email")
    phone_number: str = Field(alias="phoneNumber")
    current_user_id: UUID = Field(alias="currentUserId")

#--------------------------------------------------


#------------------Response Class------------------

class create_user_command_dto(BaseModel):
    id: UUID = Field(alias="id")

class create_user_command_response(BaseModel):
    user: create_user_command_dto

#--------------------------------------------------


#------------------Execute-------------------------

async def create_user_command_handler_async(
    db_session: AsyncSession, 
    model: create_user_command
) -> create_user_command_response:
    stmt = (
        insert(User)
        .values(
            id=uuid4(),
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone_number=model.phone_number,
            created_on=now_utc(),
            created_by=model.current_user_id
        )
        .returning(User)
    )
    result = await db_session.execute(stmt)
    await db_session.commit()
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return create_user_command_response(
        user=create_user_command_dto(id=user.id)
    )

#--------------------------------------------------