from fastapi import HTTPException


class PromoNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Promo not found")


class ConflictRaffleException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="Conflict raffle")
