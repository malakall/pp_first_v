from datetime import datetime
from fastapi import Depends, Request
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from app.exceptions import IncorrectFormatTokenException, TokenAbsentException, TokenExpiredException, UserIsNotPresentException
from app.users.dao import UsersDAO

load_dotenv()


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)): # наша функция зависит от функции get_token
    try:
        payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), os.getenv("ALGORITMN")
        )

    except JWTError:
        raise IncorrectFormatTokenException

    expire: str = payload.get("exp")
    if not (expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException


    return user