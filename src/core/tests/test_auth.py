from __future__ import annotations

import pytest

from src.core.services.auth_service import AuthService
from src.data_access.repositories.mock import MockUserRepo


@pytest.mark.asyncio
async def test_auth() -> None:
    user_repo = MockUserRepo()
    auth_service = AuthService(user_repo)
    user = await auth_service.auth("login123", "password123")
    assert user.login == "login123" and user.password == "password123"


@pytest.mark.asyncio
async def test_auth_without_login() -> None:
    user_repo = MockUserRepo()
    auth_service = AuthService(user_repo)
    user = await auth_service.auth("", "password123")
    assert user.login == "" and user.password == "password123"


@pytest.mark.asyncio
async def test_auth_without_password() -> None:
    user_repo = MockUserRepo()
    auth_service = AuthService(user_repo)
    user = await auth_service.auth("login123", "")
    assert user.login == "login123" and user.password == ""


@pytest.mark.asyncio
async def test_auth_without_password_and_login() -> None:
    user_repo = MockUserRepo()
    auth_service = AuthService(user_repo)
    user = await auth_service.auth("", "")
    assert user.login == "" and user.password == ""
