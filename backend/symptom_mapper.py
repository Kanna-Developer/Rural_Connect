# backend/symptom_mapper.py

from config import DEFAULT_SPECIALIST
from utils import safe_lower

def map_symptom_to_specialist(user_input: str, symptom_df):
    user_input_lower = safe_lower(user_input)

    best_match = None
    best_score = 0

    for _, row in symptom_df.iterrows():
        keywords = str(row["keywords"]).split(",")
        score = 0

        for keyword in keywords:
            keyword_clean = safe_lower(keyword)
            if keyword_clean and keyword_clean in user_input_lower:
                score += 1

        # Also check direct symptom/condition name
        condition_name = safe_lower(row["symptom_or_condition"])
        if condition_name and condition_name in user_input_lower:
            score += 2

        if score > best_score:
            best_score = score
            best_match = row

    if best_match is not None and best_score > 0:
        return {
            "specialist": best_match["mapped_specialist"],
            "emergency_level": best_match["emergency_level"],
            "matched_condition": best_match["symptom_or_condition"],
            "match_score": best_score
        }

    return {
        "specialist": DEFAULT_SPECIALIST,
        "emergency_level": "Low",
        "matched_condition": "general consultation",
        "match_score": 0
    }