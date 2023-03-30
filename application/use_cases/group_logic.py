import random
from typing import List, Dict

from peewee import JOIN

from application.database.group import GroupDB
from application.database.participant import ParticipantDB
from application.database.bind import db_manager
from application.dto.exception import (
    GroupNotFound,
    ConflictRaffleException,
    ParticipantOrGroupOrRecipientNotFound,
)
from application.dto.groups import (
    GroupCreateInputDTO,
    GroupCreateOutputDTO,
    GroupListOutputDTO,
)
from application.dto.participant import (
    ParticipantCreateOutputDTOWithRecipient,
    ParticipantCreateOutputDTO,
    FullGroupById,
)
from application.use_cases import validators


async def create_promo_uc(group: GroupCreateInputDTO) -> GroupCreateOutputDTO:
    query = GroupDB.insert(name=group.name, description=group.description)
    id_ = await db_manager.execute(query=query)
    return GroupCreateOutputDTO(id=id_, name=group.name, description=group.description,)


async def exists_promo_uc(group_id: int) -> bool:
    query = GroupDB.select(GroupDB.id).where(GroupDB.id.in_((group_id,))).limit(1)
    return await db_manager.count(query=query) == 1


async def update_promo_uc(group_id: int, group: GroupCreateInputDTO) -> GroupCreateOutputDTO:
    if not await exists_promo_uc(group_id=group_id):
        raise GroupNotFound()
    query = GroupDB.update(name=group.name, description=group.description).where(GroupDB.id.in_((group_id,)))
    await db_manager.execute(query=query)
    return GroupCreateOutputDTO(id=group_id, name=group.name, description=group.description,)


async def delete_promo_uc(group_id: int):
    if not await exists_promo_uc(group_id=group_id):
        raise GroupNotFound()
    query = GroupDB.delete().where(GroupDB.id.in_((group_id,)))
    await db_manager.execute(query=query)


async def get_list_promo_uc() -> GroupListOutputDTO:
    query = GroupDB.select().order_by(GroupDB.id.desc()).dicts()
    rows = await db_manager.execute(query=query)
    return validators.validate_list(response=rows, base_model=GroupCreateOutputDTO)


async def get_group_by_id(group_id: int) -> GroupCreateOutputDTO:
    query = GroupDB.select().where(GroupDB.id.in_((group_id,))).limit(1)
    rows = await db_manager.execute(query)
    if not rows:
        raise GroupNotFound()
    row = rows[0]
    return GroupCreateOutputDTO(id=row.id, name=row.name, description=row.description,)


async def get_recipients(group_id: int,) -> List[ParticipantCreateOutputDTOWithRecipient]:
    RecipientDB = ParticipantDB.alias("recipient")
    query = (
        ParticipantDB.select().join_from(
            ParticipantDB,
            RecipientDB,
            join_type=JOIN.LEFT_OUTER,
            on=((ParticipantDB.recipient == RecipientDB.id) & (ParticipantDB.group == RecipientDB.group)),
        )
    ).where(ParticipantDB.group == group_id)
    rows: List[ParticipantDB] = await db_manager.execute(query)
    return [
        ParticipantCreateOutputDTOWithRecipient(
            name=row.name,
            wish=row.wish,
            id=row.id,
            recipient=(
                ParticipantCreateOutputDTO(name=row.recipient.name, wish=row.recipient.wish, id=row.recipient.id,)
                if row.recipient
                else None
            ),
        )
        for row in rows
    ]


async def get_only_recipients_by_id_uc(group_id: int, participant_id: int) -> ParticipantCreateOutputDTO:
    RecipientDB = ParticipantDB.alias("recipient")
    query = (
        (
            ParticipantDB.select().join_from(
                ParticipantDB,
                RecipientDB,
                join_type=JOIN.INNER,
                on=((ParticipantDB.recipient == RecipientDB.id) & (ParticipantDB.group == RecipientDB.group)),
            )
        )
        .where((ParticipantDB.group == group_id) & (ParticipantDB.id == participant_id))
        .limit(1)
    )
    rows: List[ParticipantDB] = await db_manager.execute(query)
    if not rows:
        raise ParticipantOrGroupOrRecipientNotFound()
    row = rows[0].recipient
    return ParticipantCreateOutputDTO(name=row.name, wish=row.wish, id=row.id,)


async def get_group_by_id_uc(group_id: int) -> FullGroupById:
    group = await get_group_by_id(group_id=group_id)
    members = await get_recipients(group_id=group_id)
    group_output = FullGroupById.parse_obj(group)
    group_output.participants = members
    return group_output


def shuffle(participants_ids: List[int]) -> Dict[int, int]:
    if len(participants_ids) < 3:
        raise ConflictRaffleException()
    buffer = set(participants_ids)
    ans = dict()
    for participants_id, index in zip(participants_ids, range(len(participants_ids))):
        if (index == len(participants_ids) - 2) and (participants_ids[-1] in buffer or participants_ids[-2] in buffer):
            first = participants_ids[-2]
            if first in buffer:
                buffer.remove(first)
                recipient_id = random.choice(list(buffer))
                ans[first] = recipient_id
                buffer.remove(recipient_id)
                buffer.add(first)
            second = participants_ids[-1]
            if second in buffer:
                buffer.remove(second)
                recipient_id = random.choice(list(buffer))
                ans[second] = recipient_id
                buffer.remove(recipient_id)
                buffer.add(second)
            if first not in ans:
                recipient_id = random.choice(list(buffer))
                ans[first] = recipient_id
                buffer.remove(recipient_id)
            if second not in ans:
                recipient_id = random.choice(list(buffer))
                ans[second] = recipient_id
                buffer.remove(recipient_id)
            break
        returned = True
        try:
            buffer.remove(participants_id)
        except KeyError:
            returned = False
        recipient_id = random.choice(list(buffer))
        buffer.remove(recipient_id)
        if returned:
            buffer.add(participants_id)
        ans[participants_id] = recipient_id
    return ans


async def toss_uc(group_id: int) -> List[ParticipantCreateOutputDTOWithRecipient]:
    if not await exists_promo_uc(group_id=group_id):
        raise GroupNotFound()
    query = ParticipantDB.select(ParticipantDB.id).where(ParticipantDB.group.in_((group_id,)))
    rows = await db_manager.execute(query)
    ids = [row.id for row in rows]
    choices = shuffle(participants_ids=ids)
    async with db_manager.transaction():
        for key, value in choices.items():
            query = ParticipantDB.update(recipient=value).where(ParticipantDB.id.in_((key,)))
            await db_manager.execute(query)
    return await get_recipients(group_id=group_id)
