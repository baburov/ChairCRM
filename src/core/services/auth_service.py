from __future__ import annotations

from src.core.interfaces.authorizer import IAuthorizer
from src.core.models.user import User
from src.data_access.repositories_interface import IUserRepo


class AuthService(IAuthorizer):
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    async def auth(self, login: str, password: str) -> User:
        try:
            return await self.user_repo.get_by_login_pswd(login, password) 
        except Exception as e:
            raise Exception(f"Authentication error: {e}")

    async def register(self, user_data: User) -> User:
        try:
            await self.user_repo.add_user(user_data)
        except Exception as e:
            raise Exception(f"Register error: {e}")
        return user_data
    