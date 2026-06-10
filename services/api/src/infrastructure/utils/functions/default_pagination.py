from fastapi_pagination import Params


def set_custom_pagination(
    page: int = 1,
    size: int = 5,
) -> Params:
    return Params(
        page=page,
        size=size,
    )
