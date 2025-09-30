from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, Field
from uuid import UUID

from app.models.user import User


#------------------query Class---------------------

#--------------------------------------------------


#------------------response Class------------------

class get_user_query_dto(BaseModel):
    id: UUID = Field(alias="id")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str = Field(alias="email")
    phone_number: str = Field(alias="phoneNumber")

    class Config:
        populate_by_name = True

class get_users_query_response(BaseModel):
    users: list[get_user_query_dto]

#--------------------------------------------------


#------------------Exceute-------------------------

async def get_users_query_handler_async(
    db_session: AsyncSession
) -> get_users_query_response:
    users_query = await db_session.scalars(select(User))
    users = users_query.all()
    if not users:
        return None
    return get_users_query_response(
        users=[
            get_user_query_dto(
                id=p.id,
                first_name=p.first_name,
                last_name=p.last_name,
                email=p.email,
                phone_number=p.phone_number
            )
            for p in users
        ]
    )

#--------------------------------------------------