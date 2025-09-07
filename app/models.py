# app/models.py
from pydantic import BaseModel
from typing import List

class Stat(BaseModel):
    """
    Represents a single base stat for a Pokémon.
    e.g., {"name": "hp", "value": 45}
    """
    name: str
    value: int

class Pokemon(BaseModel):
    """
    Defines the structured data for a single Pokémon that our API will expose.
    This model includes the specific fields required by the assignment.
    """
    id: int
    name: str
    types: List[str]
    abilities: List[str]
    base_stats: List[Stat]
