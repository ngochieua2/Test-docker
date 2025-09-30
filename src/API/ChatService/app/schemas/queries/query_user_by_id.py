from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, Field
import uuid

from app.models.user import User


#------------------query Class---------------------

class get_user_by_id_query(BaseModel):
    user_id: uuid.UUID

#--------------------------------------------------


#------------------response Class------------------

class get_user_by_id_query_response(BaseModel):
    id: uuid.UUID = Field(alias="id")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str = Field(alias="email")
    phone_number: str = Field(alias="phoneNumber")

    class Config:
        populate_by_name = True

#--------------------------------------------------


#------------------Exceute-------------------------

async def get_user_by_id_query_handler_async(
        db_session: AsyncSession, 
        user_id: uuid.UUID
) -> get_user_by_id_query_response:
    user_query = await db_session.scalars(select(User).where(User.id==user_id).limit(1))
    user = user_query.first()
    if user is None:
        return None
    return get_user_by_id_query_response(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number
    )

#--------------------------------------------------