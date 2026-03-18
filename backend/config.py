# backend/config.py

DOCTORS_CSV_PATH = "../data/doctors.csv"
SYMPTOM_MAP_CSV_PATH = "../data/symptom_specialist_map.csv"

# Default fallback specialist if no match is found
DEFAULT_SPECIALIST = "General Physician"

# Emergency levels
HIGH_RISK_LEVELS = ["high", "critical"]

# Supported cities for recommendation
SUPPORTED_CITIES = ["Chennai", "Bengaluru", "Madurai", "Coimbatore", "Thoothukudi", "Tirunelveli"]

# Nearby city mapping for rural / district-level support
NEARBY_CITY_MAP = {
    "udangudi": ["Thoothukudi", "Tirunelveli", "Madurai", "Chennai"],
    "thoothukudi": ["Thoothukudi", "Tirunelveli", "Madurai", "Chennai"],
    "tuticorin": ["Thoothukudi", "Tirunelveli", "Madurai", "Chennai"],
    "tirunelveli": ["Tirunelveli", "Madurai", "Chennai"],
    "kovilpatti": ["Thoothukudi", "Tirunelveli", "Madurai"],
    "madurai": ["Madurai", "Chennai", "Coimbatore"],
    "chengalpattu": ["Chennai"],
    "kanchipuram": ["Chennai"],
    "villupuram": ["Chennai", "Puducherry"],
    "salem": ["Coimbatore", "Bengaluru", "Chennai"]
}