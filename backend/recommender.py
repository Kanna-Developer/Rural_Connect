# backend/recommender.py

from utils import safe_lower, parse_languages, has_video_consultation, is_emergency_supported

def calculate_recommendation_score(row, specialist, city, language):
    score = 0

    # 1. Specialty exact match
    if safe_lower(row["specialty"]) == safe_lower(specialist):
        score += 40

    # 2. City exact match
    if safe_lower(row["city"]) == safe_lower(city):
        score += 25

    # 3. Language match
    doctor_languages = parse_languages(row["languages_spoken"])
    if safe_lower(language) in doctor_languages:
        score += 20
    elif "english" in doctor_languages:
        # Fallback if requested language not found but English exists
        score += 8

    # 4. Teleconsultation availability
    if has_video_consultation(row["consultation_mode"]):
        score += 10

    # 5. Emergency support
    if is_emergency_supported(row["emergency_supported"]):
        score += 15

    # 6. Rating bonus (max 5)
    try:
        score += min(float(row["rating"]), 5)
    except:
        pass

    return round(score, 2)

def recommend_doctors(doctors_df, specialist, preferred_city, language, nearby_city_suggestions=None, top_n=5):
    if nearby_city_suggestions is None:
        nearby_city_suggestions = [preferred_city]

    # Filter by specialist first
    specialist_filtered = doctors_df[
        doctors_df["specialty"].astype(str).str.strip().str.lower() == safe_lower(specialist)
    ].copy()

    if specialist_filtered.empty:
        return []

    # Keep doctors from preferred city + nearby city suggestions
    city_set = set([safe_lower(city) for city in nearby_city_suggestions if city])
    city_filtered = specialist_filtered[
        specialist_filtered["city"].astype(str).str.strip().str.lower().isin(city_set)
    ].copy()

    # Fallback: if no city-based match, return all specialist matches
    if city_filtered.empty:
        city_filtered = specialist_filtered.copy()

    # Score each doctor
    city_filtered["recommendation_score"] = city_filtered.apply(
        lambda row: calculate_recommendation_score(
            row=row,
            specialist=specialist,
            city=preferred_city,
            language=language
        ),
        axis=1
    )

    # Sort by score descending
    city_filtered = city_filtered.sort_values(by="recommendation_score", ascending=False)

    # Return top N
    results = city_filtered.head(top_n).to_dict(orient="records")
    return results