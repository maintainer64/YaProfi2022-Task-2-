from application.database.bind import db_manager
from application.database.participant import ParticipantDB
from application.dto.exception import GroupNotFound, ParticipantNotFound
from application.dto.participant import ParticipantCreateInputDTO
from application.use_cases.group_logic import exists_promo_uc


async def exists_pat_uc(pat_id: int) -> bool:
    query = ParticipantDB.select(ParticipantDB.id).where(ParticipantDB.id.in_((pat_id,))).limit(1)
    return await db_manager.count(query=query) == 1


async def add_pat_to_promo(participant: ParticipantCreateInputDTO, group_id: int) -> int:
    group_exists = await exists_promo_uc(group_id=group_id)
    if not group_exists:
        raise GroupNotFound()
    query = ParticipantDB.insert(name=participant.name, wish=participant.wish, group=group_id)
    identifier = await db_manager.execute(query=query)
    return identifier


async def delete_pat_to_promo(
    participant_id: int, group_id: int,
):
    group_exists = await exists_promo_uc(group_id=group_id)
    if not group_exists:
        raise GroupNotFound()
    if not await exists_pat_uc(pat_id=participant_id):
        raise ParticipantNotFound()
    query = ParticipantDB.delete().where(ParticipantDB.id.in_((participant_id,)) & ParticipantDB.group.in_((group_id,)))
    await db_manager.execute(query=query)
