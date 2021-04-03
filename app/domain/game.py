from typing import List

from pydantic.main import BaseModel

from app.domain.player import Player


class Game(BaseModel):
    code: str
    started: bool
    exp_seq: List[int]
    seq: List[int]
    players: List[Player]