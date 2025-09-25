from datetime import datetime
from typing import Any, Dict
import json

def format_timestamp(dt: datetime) -> str:
    """
    Format datetime to ISO string
    """
    return dt.isoformat() + "Z"

def sanitize_string(text: str, max_length: int = 100) -> str:
    """
    Sanitize and truncate string input
    """
    if not text:
        return ""
    
    # Remove potentially harmful characters
    sanitized = text.strip()
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length-3] + "..."
    
    return sanitized

def safe_json_loads(text: str, default: Any = None) -> Any:
    """
    Safely parse JSON string
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default

def format_bytes(bytes_count: int) -> str:
    """
    Format bytes to human readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"

def dict_to_query_string(params: Dict[str, Any]) -> str:
    """
    Convert dictionary to query string
    """
    query_parts = []
    for key, value in params.items():
        if value is not None:
            query_parts.append(f"{key}={value}")
    return "&".join(query_parts)