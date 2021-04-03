import uuid
from typing import List

from pydantic.main import BaseModel


class Player(BaseModel):
    id: uuid.UUID
    name: str
    all_numbers: List[int]
    used_numbers: List[int]