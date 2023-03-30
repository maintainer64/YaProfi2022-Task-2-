from typing import Optional, List

from pydantic import BaseModel


class GroupCreateInputDTO(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreateOutputDTO(GroupCreateInputDTO):
    id: int


GroupListOutputDTO = List[GroupCreateOutputDTO]
