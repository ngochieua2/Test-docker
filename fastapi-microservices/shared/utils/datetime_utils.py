"""
Date and time utility functions
"""
from datetime import datetime, timezone, timedelta
from typing import Optional
import pytz


def utc_now() -> datetime:
    """
    Get current UTC datetime
    """
    return datetime.now(timezone.utc)


def local_now(tz: str = "UTC") -> datetime:
    """
    Get current datetime in specified timezone
    """
    timezone_obj = pytz.timezone(tz)
    return datetime.now(timezone_obj)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string
    """
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse datetime string
    """
    return datetime.strptime(dt_str, format_str)


def add_timezone(dt: datetime, tz: str = "UTC") -> datetime:
    """
    Add timezone info to naive datetime
    """
    if dt.tzinfo is None:
        timezone_obj = pytz.timezone(tz)
        return timezone_obj.localize(dt)
    return dt


def convert_timezone(dt: datetime, target_tz: str) -> datetime:
    """
    Convert datetime to different timezone
    """
    target_timezone = pytz.timezone(target_tz)
    return dt.astimezone(target_timezone)


def time_ago(dt: datetime, reference: Optional[datetime] = None) -> str:
    """
    Get human-readable time difference
    """
    if reference is None:
        reference = utc_now()
    
    # Ensure both datetimes have timezone info
    if dt.tzinfo is None:
        dt = add_timezone(dt)
    if reference.tzinfo is None:
        reference = add_timezone(reference)
    
    diff = reference - dt
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"


def is_business_day(dt: datetime) -> bool:
    """
    Check if datetime falls on a business day (Monday-Friday)
    """
    return dt.weekday() < 5  # 0-4 = Monday-Friday


def next_business_day(dt: datetime) -> datetime:
    """
    Get next business day
    """
    next_day = dt + timedelta(days=1)
    while not is_business_day(next_day):
        next_day += timedelta(days=1)
    return next_day