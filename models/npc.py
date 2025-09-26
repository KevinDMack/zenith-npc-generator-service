from pydantic import BaseModel
from typing import Optional


class NPC(BaseModel):
    """NPC data model with all required attributes"""
    Name: str
    Age: int
    Species: str
    PhysicalDescription: str
    PersonalityDescription: str
    ResidentDistrict: str


class NPCGenerationRequest(BaseModel):
    """Request model for NPC generation"""
    count: Optional[int] = 1
    species_preference: Optional[str] = None
    district_preference: Optional[str] = None
    age_range: Optional[str] = None