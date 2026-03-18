# backend/utils.py

def safe_lower(value):
    if value is None:
        return ""
    return str(value).strip().lower()

def parse_languages(language_string):
    return [lang.strip().lower() for lang in str(language_string).split(",") if lang.strip()]

def has_video_consultation(consultation_mode):
    return "video" in str(consultation_mode).lower()

def is_emergency_supported(value):
    return str(value).strip().lower() == "yes"