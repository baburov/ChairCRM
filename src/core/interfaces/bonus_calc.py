from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.models.user import User


class IBonusCalc(ABC):
    @abstractmethod
    async def calc_user_bonuses(self, user_data: User) -> float:
        pass