from typing import Optional
from urllib.parse import parse_qsl


def parse_query_str(query_str: Optional[str]) -> dict:
    if not query_str:
        return {}

    return dict(parse_qsl(query_str))
