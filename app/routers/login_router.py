import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel

from app.models.user import UserResponse, UserResponseAll
from app.services.user_service import UserService
from app.settings import APP_CONFIG
from app.utils.auth import get_current_user_from_token
from app.utils.hasher import Hasher


logger = logging.getLogger(__name__)


class LoginForm(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


class AuthRouter:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @property
    def api_route(self) -> APIRouter:
        router = APIRouter()
        self._register(router)
        return router

    def _register(self, router: APIRouter):
        @router.post("/token", response_model=Token)
        async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
        ):
            user = await self.authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                )
            access_token_expires = timedelta(minutes=APP_CONFIG.access_token_expire_minutes)
            access_token = self.create_access_token(
                data={"sub": user.email, "cas_id": str(user.id)},
                expires_delta=access_token_expires,
            )
            return {"access_token": access_token, "token_type": "bearer"}

        @router.get("/get_token", response_model=UserResponse)
        async def get_current_user(
            current_user: UserResponseAll = Depends(self._get_current_user),
        ):
            return current_user

    async def _get_current_user(self, token: str = Depends(oauth2_scheme)) -> UserResponseAll:
        return await get_current_user_from_token(token, self._user_service)

    async def authenticate_user(self, email: str, password: str) -> UserResponseAll | None:
        user = await self._user_service.get_user_by_email(email)
        if user is None or not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, APP_CONFIG.secret_key, algorithm=APP_CONFIG.algorithm)
        return encoded_jwt
