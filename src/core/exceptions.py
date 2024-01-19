from fastapi import HTTPException, status

UnAuthorizedExp = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

NotFoundExp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found",
)

ForbiddenExp = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have enough permissions",
)

ValidationExp = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Validation error",
)


ConflictExp = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Conflict error",
)

BadRequestExp = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request",
)
