from __future__ import annotations

from src.core.interfaces.bonus_calc import IBonusCalc
from src.core.models.user import User
from src.data_access.repositories_interface import IInteractionHistoryRepo
from src.data_access.repositories_interface import IUserRepo


class BonusCalcService(IBonusCalc):
    def __init__(self, interaction_repo: IInteractionHistoryRepo, user_repo: IUserRepo):
        self.interation_repo = interaction_repo
        self.user_repo = user_repo
    
    async def calc_user_bonuses(self, user_data: User) -> float:
        coeff = 1000
        try:
            interactions = await self.interation_repo.get_by_user(user_data)
            sells = sum(1 if interaction.type == "sell" else 0 for interaction in interactions)
            return sells * coeff
        except Exception as e:
            raise Exception(f"Calculation bonus error: {e}")