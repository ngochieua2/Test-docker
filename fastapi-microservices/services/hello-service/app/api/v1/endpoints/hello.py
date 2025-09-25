from fastapi import APIRouter, Depends
from app.services.hello_service import HelloService
from app.schemas.hello import HelloResponse, HelloRequest

router = APIRouter()

@router.get("/", response_model=HelloResponse)
async def get_hello(hello_service: HelloService = Depends(HelloService)):
    """
    Simple hello endpoint
    """
    return await hello_service.get_hello_message()

@router.post("/", response_model=HelloResponse)
async def post_hello(
    request: HelloRequest,
    hello_service: HelloService = Depends(HelloService)
):
    """
    Personalized hello endpoint
    """
    return await hello_service.get_personalized_hello(request.name)

@router.get("/greetings/{language}", response_model=HelloResponse)
async def get_hello_in_language(
    language: str,
    hello_service: HelloService = Depends(HelloService)
):
    """
    Hello in different languages
    """
    return await hello_service.get_hello_in_language(language)