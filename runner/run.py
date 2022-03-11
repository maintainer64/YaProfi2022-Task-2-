import logging
from typing import List

from fastapi import FastAPI, Response

from application.dto.participant import (
    ParticipantCreateInputDTO,
    ParticipantCreateOutputDTO,
    PrizeCreateInputDTO,
    PrizeCreateOutputDTO,
)
from application.dto.promos import (
    PromoCreateInputDTO,
    PromoCreateOutputDTO,
    PromoItemOutputDTO,
    PromoItemFullOutputDTO,
    RaffleItemDTO,
)
from application.use_cases.participant_logic import add_pat_to_promo, delete_pat_to_promo
from application.use_cases.prizes_logic import add_prize_to_promo, delete_prize_to_promo
from application.use_cases.promo_logic import (
    create_promo_uc,
    get_list_promo_uc,
    update_promo_uc,
    delete_promo_uc,
    get_promo_by_id,
)
from application.use_cases.raffle_logic import raffle_uc
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
@app.post("/promo", response_model=PromoCreateOutputDTO)
async def create_promo(promo: PromoCreateInputDTO):
    identifier = await create_promo_uc(promo=promo)
    return PromoCreateOutputDTO(id=identifier)


@app.get("/promo", response_model=List[PromoItemOutputDTO])
async def list_promo():
    return await get_list_promo_uc()


@app.get("/promo/{promo_id}", response_model=PromoItemFullOutputDTO)
async def details_promo(promo_id: int):
    return await get_promo_by_id(promo_id=promo_id)


@app.put("/promo/{promo_id}")
async def update_promo(promo_id: int, promo: PromoCreateInputDTO):
    await update_promo_uc(promo_id=promo_id, promo=promo)
    return Response()


@app.delete("/promo/{promo_id}")
async def delete_promo(promo_id: int):
    await delete_promo_uc(promo_id=promo_id)
    return Response()


@app.post("/promo/{promo_id}/participant", response_model=ParticipantCreateOutputDTO)
async def create_participant(participant: ParticipantCreateInputDTO, promo_id: int):
    identifier = await add_pat_to_promo(participant=participant, promo_id=promo_id)
    return ParticipantCreateOutputDTO(id=identifier)


@app.delete("/promo/{promo_id}/participant/{participant_id}")
async def delete_participant(participant_id: int, promo_id: int):
    await delete_pat_to_promo(participant_id=participant_id, promo_id=promo_id)
    return Response()


@app.post("/promo/{promo_id}/prize", response_model=PrizeCreateOutputDTO)
async def create_prize(promo_id: int, prize: PrizeCreateInputDTO):
    identifier = await add_prize_to_promo(prize=prize, promo_id=promo_id,)
    return PrizeCreateOutputDTO(id=identifier)


@app.post("/promo/{promo_id}/prize/{prize_id}")
async def delete_prize(promo_id: int, prize_id: int):
    await delete_prize_to_promo(
        prize_id=prize_id, promo_id=promo_id,
    )


@app.post("/promo/{promo_id}/raffle", response_model=List[RaffleItemDTO])
async def raffle(promo_id: int):
    return await raffle_uc(promo_id=promo_id)
