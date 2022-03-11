from application.database.bind import db_manager
from application.database.prize import PrizeDB
from application.dto.exception import PromoNotFound
from application.dto.participant import PrizeCreateInputDTO
from application.use_cases.promo_logic import exists_promo_uc


async def add_prize_to_promo(prize: PrizeCreateInputDTO, promo_id: int) -> int:
    promo_exists = await exists_promo_uc(promo_id=promo_id)
    if not promo_exists:
        raise PromoNotFound()
    return await add_prize_to_promo_uc(prize_description=prize.description, promo_id=promo_id,)


async def add_prize_to_promo_uc(prize_description: str, promo_id: int) -> int:
    query = PrizeDB.insert(description=prize_description, promo=promo_id,)
    return await db_manager.execute(query=query)


async def delete_prize_to_promo(
    prize_id: int, promo_id: int,
):
    query = PrizeDB.delete().where(PrizeDB.id.in_((prize_id,)) & PrizeDB.promo.in_((promo_id,)))
    await db_manager.execute(query=query)
