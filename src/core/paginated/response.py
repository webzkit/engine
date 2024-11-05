from typing import Any


def paginated_response(
    crud_data: Any, page: int, items_per_page: int
) -> dict[str, Any]:
    return {
        "data": crud_data["data"],
        "total": crud_data["total_count"],
        "has_more": (page * items_per_page) < crud_data["total_count"],
        "page": page,
        "items_per_page": items_per_page,
    }
