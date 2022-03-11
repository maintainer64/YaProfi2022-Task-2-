import random
from typing import List

from application.dto.exception import ConflictRaffleException
from application.dto.promos import RaffleItemDTO
from application.use_cases.promo_logic import get_promo_by_id


async def raffle_uc(promo_id: int) -> List[RaffleItemDTO]:
    ans = []
    promo_model = await get_promo_by_id(promo_id=promo_id)
    if len(promo_model.prizes) != len(promo_model.participants):
        raise ConflictRaffleException()
    random.shuffle(promo_model.participants, random.random)
    for prize, member in zip(promo_model.prizes, promo_model.participants):
        ans.append(RaffleItemDTO(winner=member, prize=prize,))
    return ans
