from typing import Optional

from fastapi import Request

from core.exceptions import UnAuthorizedExp


def get_token_header(request: Request) -> str:
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization:
        token = authorization.split(" ")[1]
        return token
    else:
        raise UnAuthorizedExp
