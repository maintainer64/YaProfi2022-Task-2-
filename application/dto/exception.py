from fastapi import HTTPException


class GroupNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Group not found")


class ParticipantNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Participant not found")


class ParticipantOrGroupOrRecipientNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="ParticipantOrGroupOrRecipient not found")


class ConflictRaffleException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="Conflict")
