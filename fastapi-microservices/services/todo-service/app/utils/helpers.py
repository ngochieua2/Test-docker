from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import json
import re

def format_timestamp(dt: datetime) -> str:
    """
    Format datetime to ISO string
    """
    return dt.isoformat() + "Z"

def sanitize_string(text: str, max_length: int = 200) -> str:
    """
    Sanitize and truncate string input
    """
    if not text:
        return ""
    
    # Remove potentially harmful characters and normalize whitespace
    sanitized = re.sub(r'\s+', ' ', text.strip())
    
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

def calculate_completion_rate(completed: int, total: int) -> float:
    """
    Calculate completion rate as percentage
    """
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)

def get_date_range(days: int = 7) -> tuple[datetime, datetime]:
    """
    Get date range for the last N days
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def paginate_query_params(skip: int, limit: int, max_limit: int = 1000) -> tuple[int, int]:
    """
    Validate and normalize pagination parameters
    """
    skip = max(0, skip)
    limit = min(max(1, limit), max_limit)
    return skip, limit

def build_search_filters(search: Optional[str]) -> List[str]:
    """
    Build search filter keywords from search string
    """
    if not search:
        return []
    
    # Split search string into words and clean them
    words = [word.strip().lower() for word in search.split() if word.strip()]
    return words

def format_file_size(bytes_count: int) -> str:
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
            if isinstance(value, bool):
                value = str(value).lower()
            query_parts.append(f"{key}={value}")
    return "&".join(query_parts)

def validate_todo_priority(priority: Optional[str]) -> str:
    """
    Validate and normalize todo priority
    """
    valid_priorities = ['low', 'medium', 'high', 'urgent']
    if priority is None:
        return 'medium'
    
    priority_lower = priority.lower().strip()
    return priority_lower if priority_lower in valid_priorities else 'medium'