from typing import Dict
from app.schemas.hello import HelloResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

class HelloService:
    """
    Business logic for hello operations
    """
    
    # Dictionary for different language greetings
    GREETINGS: Dict[str, str] = {
        "english": "Hello",
        "spanish": "Hola",
        "french": "Bonjour", 
        "german": "Hallo",
        "italian": "Ciao",
        "portuguese": "Olá",
        "russian": "Привет",
        "japanese": "こんにちは",
        "chinese": "你好",
        "korean": "안녕하세요"
    }
    
    async def get_hello_message(self) -> HelloResponse:
        """
        Get simple hello message
        """
        logger.info("Generating simple hello message")
        return HelloResponse(
            message="Hello World!",
            timestamp=None,
            service="hello-service"
        )
    
    async def get_personalized_hello(self, name: str) -> HelloResponse:
        """
        Get personalized hello message
        """
        logger.info(f"Generating personalized hello for: {name}")
        return HelloResponse(
            message=f"Hello, {name}!",
            timestamp=None,
            service="hello-service"
        )
    
    async def get_hello_in_language(self, language: str) -> HelloResponse:
        """
        Get hello message in specified language
        """
        language_lower = language.lower()
        logger.info(f"Generating hello message in language: {language}")
        
        greeting = self.GREETINGS.get(language_lower, "Hello")
        
        return HelloResponse(
            message=f"{greeting}, World!",
            timestamp=None,
            service="hello-service",
            language=language_lower
        )