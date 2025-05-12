from __future__ import annotations

import pytest

from src.core.models.user import User
from src.core.services.bonus_calc_service import BonusCalcService
from src.data_access.repositories.mock import MockInteractionHistoryRepo
from src.data_access.repositories.mock import MockUserRepo


EXPECTED_BONUS = 1000


@pytest.mark.asyncio
async def test_bonus_calc() -> None:
    int_repo = MockInteractionHistoryRepo()
    user_repo = MockUserRepo()
    service = BonusCalcService(interaction_repo=int_repo, user_repo=user_repo)
    assert await service.calc_user_bonuses(User(fio="123")) == EXPECTED_BONUS


@pytest.mark.asyncio
async def test_bonus_calc_1() -> None:
    int_repo = MockInteractionHistoryRepo()
    user_repo = MockUserRepo()
    service = BonusCalcService(interaction_repo=int_repo, user_repo=user_repo)
    assert await service.calc_user_bonuses(User(fio="3")) == EXPECTED_BONUS


@pytest.mark.asyncio
async def test_bonus_calc_2() -> None:
    int_repo = MockInteractionHistoryRepo()
    user_repo = MockUserRepo()
    service = BonusCalcService(interaction_repo=int_repo, user_repo=user_repo)
    assert await service.calc_user_bonuses(User(fio="")) == EXPECTED_BONUS
