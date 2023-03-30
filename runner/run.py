import logging
from typing import List

from fastapi import FastAPI, Response

from application.dto.groups import (
    GroupCreateInputDTO,
    GroupCreateOutputDTO,
    GroupListOutputDTO,
)
from application.dto.participant import (
    ParticipantCreateOutputDTO,
    ParticipantCreateInputDTO,
    FullGroupById,
    ParticipantCreateOutputDTOWithRecipient,
)
from application.use_cases.group_logic import (
    create_promo_uc,
    get_list_promo_uc,
    update_promo_uc,
    delete_promo_uc,
    get_group_by_id_uc,
    toss_uc,
    get_only_recipients_by_id_uc,
)
from application.use_cases.participant_logic import (
    add_pat_to_promo,
    delete_pat_to_promo,
)
from runner.configs import config

logger = logging.getLogger(__name__)

app = FastAPI()


#
# System
#


@app.on_event("startup")
async def startup_event():
    logger.info("Setup webhook")
    if config.environment.LOCAL == config.environment:
        logger.debug("On migrate")
        logger.debug(
            "pw_migrate create --auto --directory application/migrations "
            f"--database postgresql://{config.db_user}:{config.db_password}@"
            f"{config.db_host}:{config.db_port}/{config.db_name}"
        )
    from application.database.bind import db_manager

    logger.debug("<Application startup>")
    await db_manager.connect()
    logger.debug("<Application db-connected>")


@app.on_event("shutdown")
async def shutdown():
    from application.database.bind import db_manager

    logger.debug("<Application shutdown>")
    await db_manager.close()
    logger.debug("<Application db-disconnected>")


@app.get("/health")
def health():
    return Response("ok")


#
# API
#
@app.post("/group", response_model=GroupCreateOutputDTO)
async def create_group(group: GroupCreateInputDTO):
    return await create_promo_uc(group=group)


@app.get("/groups", response_model=GroupListOutputDTO)
async def list_group():
    return await get_list_promo_uc()


@app.get("/group/{group_id}", response_model=FullGroupById)
async def details_group(group_id: int):
    return await get_group_by_id_uc(group_id=group_id)


@app.put("/group/{group_id}", response_model=GroupCreateOutputDTO)
async def update_group(group_id: int, group: GroupCreateInputDTO):
    return await update_promo_uc(group_id=group_id, group=group)


@app.delete("/group/{group_id}")
async def delete_group(group_id: int):
    await delete_promo_uc(group_id=group_id)
    return Response()


@app.post("/group/{group_id}/participant", response_model=ParticipantCreateOutputDTO)
async def create_participant(participant: ParticipantCreateInputDTO, group_id: int):
    identifier = await add_pat_to_promo(participant=participant, group_id=group_id)
    return ParticipantCreateOutputDTO(id=identifier, name=participant.name, wish=participant.wish)


@app.delete("/group/{group_id}/participant/{participant_id}")
async def delete_participant(participant_id: int, group_id: int):
    await delete_pat_to_promo(participant_id=participant_id, group_id=group_id)
    return Response()


@app.post(
    "/group/{group_id}/toss", response_model=List[ParticipantCreateOutputDTOWithRecipient],
)
async def raffle(group_id: int):
    return await toss_uc(group_id=group_id)


@app.post(
    "/group/{group_id}/participant/{participant_id}/recipient", response_model=ParticipantCreateOutputDTO,
)
async def recipient(group_id: int, participant_id: int):
    return await get_only_recipients_by_id_uc(group_id=group_id, participant_id=participant_id)
