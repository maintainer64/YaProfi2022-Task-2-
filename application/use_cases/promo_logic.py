from typing import List

from peewee import JOIN

from application.database.promo import PromoDB
from application.database.prize import PrizeDB
from application.database.participant import MemberDB
from application.database.bind import db_manager
from application.dto.exception import PromoNotFound
from application.dto.promos import PromoCreateInputDTO, PromoItemOutputDTO, PromoItemFullOutputDTO
from application.use_cases import validators


async def create_promo_uc(promo: PromoCreateInputDTO) -> int:
    query = PromoDB.insert(name=promo.name, description=promo.description)
    return await db_manager.execute(query=query)


async def update_promo_uc(promo_id: int, promo: PromoCreateInputDTO):
    query = PromoDB.update(name=promo.name, description=promo.description).where(PromoDB.id.in_((promo_id,)))
    await db_manager.execute(query=query)


async def delete_promo_uc(promo_id: int):
    query = PromoDB.delete().where(PromoDB.id.in_((promo_id,)))
    await db_manager.execute(query=query)


async def exists_promo_uc(promo_id: int) -> bool:
    query = PromoDB.select(PromoDB.id).where(PromoDB.id.in_((promo_id,))).limit(1)
    return await db_manager.count(query=query) == 1


async def get_list_promo_uc() -> List[PromoItemOutputDTO]:
    query = PromoDB.select().order_by(PromoDB.id.desc()).dicts()
    rows = await db_manager.execute(query=query)
    return validators.validate_list(response=rows, base_model=PromoItemOutputDTO)


async def __get_db_promo_by_id(promo_id: int):
    query = (
        PromoDB.select(
            PromoDB.id.alias("promo_id"),
            PromoDB.name.alias("promo_name"),
            PromoDB.description.alias("promo_desc"),
            PrizeDB.id.alias("prize_id"),
            PrizeDB.description.alias("prize_desc"),
            MemberDB.id.alias("member_id"),
            MemberDB.name.alias("member_name"),
        )
        .join_from(PromoDB, PrizeDB, JOIN.LEFT_OUTER)
        .join_from(PromoDB, MemberDB, JOIN.LEFT_OUTER)
        .where(PromoDB.id.in_((promo_id,)))
        .order_by(PromoDB.id.desc(), PrizeDB.id.desc(), MemberDB.id.desc())
        .dicts()
    )
    rows = await db_manager.execute(query)
    if not rows:
        raise PromoNotFound()
    return rows


async def get_promo_by_id(promo_id: int) -> PromoItemFullOutputDTO:
    h_table = await __get_db_promo_by_id(promo_id=promo_id)
    dto = PromoItemFullOutputDTO(
        id=h_table[0].get("promo_id"), name=h_table[0].get("promo_name"), description=h_table[0].get("promo_desc"),
    )
    prize_ids = set()
    member_ids = set()
    for row in h_table:
        if row.get("prize_id") and row.get("prize_id") not in prize_ids:
            prize_ids.add(row.get("prize_id"))
            dto.add_prize(
                id=row.get("prize_id"), description=row.get("prize_desc"),
            )
        if row.get("member_id") and row.get("member_id") not in member_ids:
            member_ids.add(row.get("member_id"))
            dto.add_participant(id=row.get("member_id"), name=row.get("member_name"))
    return dto
