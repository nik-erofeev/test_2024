from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from app.models.user import UserResponseAll
from app.services.user_service import UserService
from app.settings import APP_CONFIG


async def get_current_user_from_token(token: str, user_service: UserService) -> UserResponseAll:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    inactive_user_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Ваш аккаунт деактивирован/удален",
    )
    try:
        payload = jwt.decode(token, APP_CONFIG.secret_key, algorithms=[APP_CONFIG.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise inactive_user_exception

    return user
