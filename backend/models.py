# backend/models.py

from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    symptoms: str
    city: str
    language: str
    severity: str = "Normal"
    current_location: Optional[str] = ""

class DoctorResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    specialty: str
    subspecialty: str
    hospital_name: str
    city: str
    area: str
    languages_spoken: str
    phone_number: str
    consultation_mode: str
    booking_link: str
    video_consult_link: str
    emergency_supported: str
    rating: float
    recommendation_score: float

class RecommendationResponse(BaseModel):
    input: dict
    matched_condition: str
    recommended_specialist: str
    emergency_level: str
    emergency_message: Optional[str]
    nearby_city_suggestions: List[str]
    recommended_doctors: List[dict]