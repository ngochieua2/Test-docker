from fastapi import APIRouter, HTTPException, Depends
from dotenv import load_dotenv

from app.services.redis_cache import RedisCacheService
from app.config import settings

from app.services.openai_service import ask_openai
from app.dependencies.redis_session import get_redis_cache_session
from app.services.redis_cache import RedisCacheService

from ...endpoints.analyze_data.requests.chat_request import ChatRequest

load_dotenv()

router = APIRouter()

# @router.post("/")
# async def analy_data(request: ChatRequest):
#     try:
#         openai_model = settings.CHAT_GPTs_MODEL
#         content_list = [msg.content for msg in request.messages]
#         response = ask_openai(content_list, openai_model)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("add-contents")
# async def add_content_async(
#     key: str, 
#     value: str, 
#     redis: RedisCacheService = Depends(get_redis_cache_session)
# ):
#     key = redis.make_key("user", key)

#     # Simulate DB lookup or business logic
#     user_data = {"user_id": key, "name": value}

#     # Save to Redis
#     await redis.set(key, user_data)

#     return {"from_cache": False, "data": user_data}

# @router.get("get-contents")
# async def get_content_async(
#     key: str,
#     redis: RedisCacheService = Depends(get_redis_cache_session)
# ):
#     return await redis.get(key)
