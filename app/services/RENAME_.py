from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.models.user import UserResponse
from app.services.user_service import UserService
from app.settings import APP_CONFIG


async def get_current_user_from_token(token: str, user_service: UserService) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
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
    return user
