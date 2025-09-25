import pytest
from unittest.mock import AsyncMock
from app.services.hello_service import HelloService

@pytest.mark.asyncio
async def test_hello_service_get_hello_message():
    """
    Test HelloService get_hello_message method
    """
    service = HelloService()
    result = await service.get_hello_message()
    
    assert result.message == "Hello World!"
    assert result.service == "hello-service"

@pytest.mark.asyncio
async def test_hello_service_get_personalized_hello():
    """
    Test HelloService get_personalized_hello method
    """
    service = HelloService()
    result = await service.get_personalized_hello("John")
    
    assert result.message == "Hello, John!"
    assert result.service == "hello-service"

@pytest.mark.asyncio
async def test_hello_service_get_hello_in_language():
    """
    Test HelloService get_hello_in_language method
    """
    service = HelloService()
    
    # Test known language
    result = await service.get_hello_in_language("spanish")
    assert "Hola" in result.message
    assert result.language == "spanish"
    
    # Test unknown language
    result = await service.get_hello_in_language("unknown")
    assert "Hello" in result.message
    assert result.language == "unknown"
    
    # Test case insensitive
    result = await service.get_hello_in_language("FRENCH")
    assert "Bonjour" in result.message
    assert result.language == "french"