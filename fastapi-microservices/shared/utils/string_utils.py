"""
String utility functions
"""
import re
import string
import secrets
from typing import Optional, List
import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """
    Convert text to URL-friendly slug
    """
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    
    # Remove non-ASCII characters
    text = text.encode("ascii", "ignore").decode("ascii")
    
    # Convert to lowercase and replace spaces/special chars
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", separator, text)
    
    return text.strip(separator)


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix
    """
    if len(text) <= length:
        return text
    
    return text[:length - len(suffix)] + suffix


def camel_to_snake(text: str) -> str:
    """
    Convert camelCase to snake_case
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(text: str) -> str:
    """
    Convert snake_case to camelCase
    """
    components = text.split("_")
    return components[0] + "".join(word.capitalize() for word in components[1:])


def generate_random_string(length: int = 32, include_punctuation: bool = False) -> str:
    """
    Generate cryptographically secure random string
    """
    alphabet = string.ascii_letters + string.digits
    if include_punctuation:
        alphabet += string.punctuation
    
    return "".join(secrets.choice(alphabet) for _ in range(length))


def mask_email(email: str) -> str:
    """
    Mask email address for privacy
    Example: user@example.com -> u***@example.com
    """
    if "@" not in email:
        return email
    
    local, domain = email.split("@", 1)
    if len(local) <= 1:
        return email
    
    masked_local = local[0] + "*" * (len(local) - 1)
    return f"{masked_local}@{domain}"


def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from text
    """
    return re.findall(r"@(\w+)", text)


def extract_hashtags(text: str) -> List[str]:
    """
    Extract #hashtags from text
    """
    return re.findall(r"#(\w+)", text)


def clean_html(text: str) -> str:
    """
    Remove HTML tags from text
    """
    return re.sub(r"<[^>]*>", "", text)


def validate_email(email: str) -> bool:
    """
    Basic email validation
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def pluralize(word: str, count: int) -> str:
    """
    Simple pluralization
    """
    if count == 1:
        return word
    
    # Simple rules - extend as needed
    if word.endswith(("s", "sh", "ch", "x", "z")):
        return word + "es"
    elif word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    else:
        return word + "s"