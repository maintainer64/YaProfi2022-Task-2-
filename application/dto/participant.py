from typing import Optional, List

from pydantic import BaseModel

from application.dto.groups import GroupCreateOutputDTO


class ParticipantCreateInputDTO(BaseModel):
    name: str
    wish: Optional[str] = None


class ParticipantCreateOutputDTO(ParticipantCreateInputDTO):
    id: int


class ParticipantCreateOutputDTOWithRecipient(ParticipantCreateOutputDTO):
    recipient: Optional[ParticipantCreateOutputDTO] = None


class FullGroupById(GroupCreateOutputDTO):
    participants: List[ParticipantCreateOutputDTOWithRecipient] = []
