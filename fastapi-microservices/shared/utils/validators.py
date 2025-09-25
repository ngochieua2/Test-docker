"""
Validation utility functions
"""
from typing import Any, Dict, List, Optional, Union
import re
from datetime import datetime


class ValidationResult:
    """
    Result of a validation operation
    """
    def __init__(self, is_valid: bool = True, errors: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []
    
    def add_error(self, error: str):
        """Add an error to the result"""
        self.is_valid = False
        self.errors.append(error)
    
    def __bool__(self):
        return self.is_valid


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """
    Validate that all required fields are present and not empty
    """
    result = ValidationResult()
    
    for field in required_fields:
        if field not in data:
            result.add_error(f"Field '{field}' is required")
        elif data[field] is None or (isinstance(data[field], (str, list, dict)) and len(data[field]) == 0):
            result.add_error(f"Field '{field}' cannot be empty")
    
    return result


def validate_string_length(value: str, min_length: int = 0, max_length: Optional[int] = None) -> ValidationResult:
    """
    Validate string length constraints
    """
    result = ValidationResult()
    
    if len(value) < min_length:
        result.add_error(f"String must be at least {min_length} characters long")
    
    if max_length and len(value) > max_length:
        result.add_error(f"String must be no more than {max_length} characters long")
    
    return result


def validate_email_format(email: str) -> ValidationResult:
    """
    Validate email format
    """
    result = ValidationResult()
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        result.add_error("Invalid email format")
    
    return result


def validate_url_format(url: str) -> ValidationResult:
    """
    Validate URL format
    """
    result = ValidationResult()
    
    pattern = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
    if not re.match(pattern, url):
        result.add_error("Invalid URL format")
    
    return result


def validate_phone_number(phone: str) -> ValidationResult:
    """
    Validate phone number format (basic validation)
    """
    result = ValidationResult()
    
    # Remove common separators
    clean_phone = re.sub(r"[\s\-\(\)\+]", "", phone)
    
    # Check if it's all digits and reasonable length
    if not clean_phone.isdigit() or len(clean_phone) < 7 or len(clean_phone) > 15:
        result.add_error("Invalid phone number format")
    
    return result


def validate_numeric_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None, max_value: Optional[Union[int, float]] = None) -> ValidationResult:
    """
    Validate numeric value is within specified range
    """
    result = ValidationResult()
    
    if min_value is not None and value < min_value:
        result.add_error(f"Value must be at least {min_value}")
    
    if max_value is not None and value > max_value:
        result.add_error(f"Value must be no more than {max_value}")
    
    return result


def validate_date_range(date: datetime, min_date: Optional[datetime] = None, max_date: Optional[datetime] = None) -> ValidationResult:
    """
    Validate date is within specified range
    """
    result = ValidationResult()
    
    if min_date and date < min_date:
        result.add_error(f"Date must be on or after {min_date.strftime('%Y-%m-%d')}")
    
    if max_date and date > max_date:
        result.add_error(f"Date must be on or before {max_date.strftime('%Y-%m-%d')}")
    
    return result


def validate_password_strength(password: str) -> ValidationResult:
    """
    Validate password strength
    """
    result = ValidationResult()
    
    if len(password) < 8:
        result.add_error("Password must be at least 8 characters long")
    
    if not re.search(r"[A-Z]", password):
        result.add_error("Password must contain at least one uppercase letter")
    
    if not re.search(r"[a-z]", password):
        result.add_error("Password must contain at least one lowercase letter")
    
    if not re.search(r"\d", password):
        result.add_error("Password must contain at least one digit")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        result.add_error("Password must contain at least one special character")
    
    return result


def combine_validation_results(*results: ValidationResult) -> ValidationResult:
    """
    Combine multiple validation results into one
    """
    combined = ValidationResult()
    
    for result in results:
        if not result.is_valid:
            combined.is_valid = False
            combined.errors.extend(result.errors)
    
    return combined