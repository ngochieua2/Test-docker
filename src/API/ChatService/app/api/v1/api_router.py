from fastapi import APIRouter
from .endpoints.analyze_data.analyze_data import router as analyze_data_router
from .endpoints.chats.chat import router as chat
from .endpoints.users.user import router as user
from .endpoints.process_data.input_data import router as process_data_router


router = APIRouter()

# Register APIs router
router.include_router(analyze_data_router, prefix="/analyze-data", tags=["Data Analysis"])
router.include_router(chat, prefix="/chats", tags=["Chats"])
router.include_router(user, prefix="/users", tags=["Users"])
router.include_router(process_data_router, prefix="/process-data", tags=["Data Processing"])
