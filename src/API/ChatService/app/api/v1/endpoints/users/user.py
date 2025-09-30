from fastapi import APIRouter
import uuid

from app.dependencies.db_context import DbContext

from app.schemas.queries.query_users import get_users_query_handler_async
from app.schemas.queries.query_user_by_id import get_user_by_id_query_handler_async
from app.schemas.commands.command_create_user import create_user_command, create_user_command_handler_async

router = APIRouter()

@router.get("/")
async def search_user_async(
    dbContext: DbContext
):
    users = await get_users_query_handler_async(dbContext)
    if users is None:
        return {
            "staus": 400
        }
    return {
            "staus": 200,
            "data": users
        }

@router.get("/{user_id}")
async def get_user_by_user_id_async(
    dbContext: DbContext, 
    user_id: str
):
    user = await get_user_by_id_query_handler_async(dbContext, user_id)
    if user is None:
        return {
            "status": 400
        }
    return {
            "status": 200,
            "data": user
        }

@router.post("/register")
async def register_user_async(
    dbContext: DbContext,
    request: create_user_command
):
    user = await create_user_command_handler_async(dbContext, request)
    if user is None:
        return { 
            "status": 400
        }
    else:
        return {
            "status": 200, 
            "data": user
        }