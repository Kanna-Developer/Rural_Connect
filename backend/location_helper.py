# backend/location_helper.py

from config import NEARBY_CITY_MAP
from utils import safe_lower

def get_nearby_city_suggestions(current_location: str, preferred_city: str):
    suggestions = []

    location_key = safe_lower(current_location)

    if location_key in NEARBY_CITY_MAP:
        suggestions = NEARBY_CITY_MAP[location_key]

    # Always prioritize the user's preferred city first if not already present
    if preferred_city and preferred_city not in suggestions:
        suggestions.insert(0, preferred_city)

    # Remove duplicates while preserving order
    unique_suggestions = []
    seen = set()
    for city in suggestions:
        city_lower = city.lower()
        if city_lower not in seen:
            unique_suggestions.append(city)
            seen.add(city_lower)

    return unique_suggestions