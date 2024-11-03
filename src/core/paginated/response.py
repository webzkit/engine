from typing import Any


def paginated_response(
    crud_data: Any, page: int, items_per_page: int
) -> dict[str, Any]:
    print(crud_data)
    return {
        "data": crud_data,
        "total": 100,
        # "total_count": crud_data["total_count"],
        "has_more": False,
        # "has_more": (page * items_per_page) < crud_data["total_count"],
        "page": page,
        "items_per_page": items_per_page,
    }
