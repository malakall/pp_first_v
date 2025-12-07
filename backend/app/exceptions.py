from fastapi import HTTPException, status


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="пользователь уже существует"
)


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="неверная почта или пароль"
)


TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="токен истек"
)


TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="токен отсутствует"
)


IncorrectFormatTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="неверный формат токена"
)


UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

