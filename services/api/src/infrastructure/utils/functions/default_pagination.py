from fastapi_pagination import Params


def set_custom_pagination(
    page: int = 1,
    size: int = 10,
) -> Params:
    return Params(
        page=page,
        size=size,
    )
