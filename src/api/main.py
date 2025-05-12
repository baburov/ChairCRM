from __future__ import annotations

import os

from uuid import UUID

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.core.models.client import Client
from src.core.models.item import Item
from src.core.models.user import User
from src.core.services.auth_service import AuthService
from src.core.services.bonus_calc_service import BonusCalcService
from src.data_access.repositories_interface import IClientRepo
from src.data_access.repositories_interface import IInteractionHistoryRepo
from src.data_access.repositories_interface import IItemRepo
from src.data_access.repositories_interface import IOrderRepo
from src.data_access.repositories_interface import IUserRepo
from src.data_access.repository_factory import RepositoryFactory


app = FastAPI(title="ChairCRM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    login: str
    password: str


class CalcLoginRequest(BaseModel):
    id: str


class UserCreateRequest(BaseModel):
    fio: str
    login: str
    password: str
    contacts: str
    role: str = "user"
    bonus: float = 0.0


async def get_user_repo() -> IUserRepo:
    if not RepositoryFactory._initialized:
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/test_db")
        await RepositoryFactory.initialize(db_url)
    return RepositoryFactory.get_user_repo()


def get_client_repo() -> IClientRepo:
    return RepositoryFactory.get_client_repo()


def get_interaction_repo() -> IInteractionHistoryRepo:
    return RepositoryFactory.get_interaction_repo()


def get_item_repo() -> IItemRepo:
    return RepositoryFactory.get_item_repo()


def get_order_repo() -> IOrderRepo:
    return RepositoryFactory.get_order_repo()


@app.post("/auth/login", response_model=User)
async def login(
    request: LoginRequest,
) -> User:
    user_repo = await get_user_repo()
    auth_service = AuthService(user_repo)
    try:
        user = await auth_service.auth(request.login, request.password)
        if not user.fio: 
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/register", response_model=User)
async def register(
    request: UserCreateRequest,
) -> User:
    user_repo = await get_user_repo()
    auth_service = AuthService(user_repo)
    try:
        user = User(**request.dict())
        return await auth_service.register(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/bonuses", response_model=float)
async def calc_user_bonuses(
    _id: str
) -> float:
    interaction_repo = get_interaction_repo()
    user_repo = await get_user_repo()
    bonus_service = BonusCalcService(interaction_repo, user_repo)
    try:
        return await bonus_service.calc_user_bonuses(User(id=UUID(_id)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{fio}", response_model=User)
async def get_user_by_fio(
    fio: str,
) -> User:
    user_repo = await get_user_repo()
    try:
        user = await user_repo.get_by_fio(fio)
        if not user.fio:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients", response_model=list[Client])
async def get_all_clients(
) -> list[Client]:
    client_repo = get_client_repo()
    try:
        return await client_repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items", response_model=list[Item])
async def get_items(
    name: str = "",
) -> list[Item]:
    item_repo = get_item_repo()
    try:
        params = Item(name=name)
        return await item_repo.get_by_params(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup() -> None:
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/test_db")
    await RepositoryFactory.initialize(db_url)


@app.on_event("shutdown")
async def shutdown() -> None:
    await RepositoryFactory.close() 