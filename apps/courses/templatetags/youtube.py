import re
from urllib.parse import parse_qs, urlparse

from django import template

register = template.Library()

_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


@register.filter
def youtube_id(value):
    """Extract a valid YouTube video ID from a URL or return empty string."""
    if not value:
        return ""

    raw = str(value).strip()
    if _ID_PATTERN.fullmatch(raw):
        return raw

    try:
        parsed = urlparse(raw)
    except ValueError:
        parsed = None

    if parsed and parsed.scheme and parsed.netloc:
        query = parse_qs(parsed.query)
        if "v" in query and query["v"]:
            candidate = query["v"][0]
            if _ID_PATTERN.fullmatch(candidate):
                return candidate

        path_parts = [part for part in parsed.path.split("/") if part]
        if path_parts:
            if path_parts[0] in {"embed", "v", "shorts", "live"} and len(path_parts) > 1:
                candidate = path_parts[1]
                if _ID_PATTERN.fullmatch(candidate):
                    return candidate
            if parsed.netloc in {"youtu.be", "www.youtu.be"}:
                candidate = path_parts[0]
                if _ID_PATTERN.fullmatch(candidate):
                    return candidate

    match = re.search(r"(?:v=|\/embed\/|youtu\.be\/)([A-Za-z0-9_-]{11})", raw)
    if match:
        return match.group(1)

    return ""
