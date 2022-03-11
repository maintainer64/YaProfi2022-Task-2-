from application.database.bind import db_manager
from application.database.participant import MemberDB
from application.dto.exception import PromoNotFound
from application.dto.participant import ParticipantCreateInputDTO
from application.use_cases.promo_logic import exists_promo_uc


async def add_pat_to_promo(participant: ParticipantCreateInputDTO, promo_id: int) -> int:
    promo_exists = await exists_promo_uc(promo_id=promo_id)
    if not promo_exists:
        raise PromoNotFound()
    return await add_pat_to_promo_uc(participant_name=participant.name, promo_id=promo_id,)


async def add_pat_to_promo_uc(participant_name: str, promo_id: int) -> int:
    query = MemberDB.insert(name=participant_name, promo=promo_id,)
    identifier = await db_manager.execute(query=query)
    return identifier


async def delete_pat_to_promo(
    participant_id: int, promo_id: int,
):
    query = MemberDB.delete().where(MemberDB.id.in_((participant_id,)) & MemberDB.promo.in_((promo_id,)))
    await db_manager.execute(query=query)
