from dataclasses import dataclass
from typing import List

@dataclass
class InputData:
    people: int
    food: float
    transport: float
    camp: float
    names: List[str]
    food_exempt: List[bool]
    transport_exempt: List[bool]
    camp_exempt: List[bool]

@dataclass
class PersonResult:
    name: str
    total: float