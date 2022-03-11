from typing import Optional, List

from pydantic import BaseModel


class PromoCreateInputDTO(BaseModel):
    name: str
    description: Optional[str] = None


class PromoCreateOutputDTO(BaseModel):
    id: int


class PromoItemOutputDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class PrizeItemModel(BaseModel):
    id: int
    description: str


class ParticipantItemModel(BaseModel):
    id: int
    name: str


class PromoItemFullOutputDTO(PromoItemOutputDTO):
    prizes: List[PrizeItemModel] = []
    participants: List[ParticipantItemModel] = []

    def add_prize(self, **kwargs):
        model = PrizeItemModel.parse_obj(kwargs)
        self.prizes.append(model)

    def add_participant(self, **kwargs):
        model = ParticipantItemModel.parse_obj(kwargs)
        self.participants.append(model)


class RaffleItemDTO(BaseModel):
    winner: ParticipantItemModel
    prize: PrizeItemModel
