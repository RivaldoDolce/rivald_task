from dataclasses import dataclass, field
from typing import List
from .card import CardModel

@dataclass
class ColumnModel:
    id: int
    title: str
    color: str = "#1E293B"
    position: int = 0
    cards: List[CardModel] = field(default_factory=list)
