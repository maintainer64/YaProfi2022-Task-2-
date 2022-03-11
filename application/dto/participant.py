from pydantic import BaseModel


class ParticipantCreateInputDTO(BaseModel):
    name: str


class ParticipantCreateOutputDTO(BaseModel):
    id: int


class PrizeCreateInputDTO(BaseModel):
    description: str


class PrizeCreateOutputDTO(BaseModel):
    id: int
