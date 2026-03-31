from typing import Optional
from urllib.parse import urlparse

def normalize_url(url: str) -> Optional[str]:
    """Normalize and validate a URL."""
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            parsed = parsed._replace(scheme="https")
        if not parsed.netloc:
            return None
        return parsed.geturl()
    except Exception:
        return None
