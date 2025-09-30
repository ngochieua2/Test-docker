from datetime import datetime, timezone

#----Get Utc Time----

def now_utc() -> datetime:
    """Get current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)

#----Convert Between Timezones----

def make_aware(dt: datetime, tz=timezone.utc) -> datetime:
    """Convert naive datetime to aware using given timezone."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt.astimezone(tz)

def make_naive(dt: datetime) -> datetime:
    """Convert aware datetime to naive (drops timezone info)."""
    return dt.replace(tzinfo=None)

#----Formatting and Parsing----

def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """Format datetime to string."""
    return dt.strftime(fmt)

def parse_datetime(s: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse string to naive datetime."""
    return datetime.strptime(s, fmt)