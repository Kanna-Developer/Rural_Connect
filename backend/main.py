from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from pathlib import Path

app = FastAPI(title="Rural Connect API", version="1.0")

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Rural_Connect
DATA_DIR = BASE_DIR / "data"

DOCTORS_CSV = DATA_DIR / "doctors.csv"
SYMPTOMS_CSV = DATA_DIR / "symptom_specialist_map.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    doctors_df = pd.read_csv(DOCTORS_CSV, encoding="utf-8-sig")
    symptoms_df = pd.read_csv(SYMPTOMS_CSV, encoding="utf-8-sig")

    # Normalize column names (remove spaces / BOM issues)
    doctors_df.columns = doctors_df.columns.str.strip().str.lower()
    symptoms_df.columns = symptoms_df.columns.str.strip().str.lower()

    # Clean text columns
    for col in doctors_df.select_dtypes(include="object").columns:
        doctors_df[col] = doctors_df[col].fillna("").astype(str).str.strip()

    for col in symptoms_df.select_dtypes(include="object").columns:
        symptoms_df[col] = symptoms_df[col].fillna("").astype(str).str.strip()

    print("Doctors CSV loaded successfully")
    print("Doctors columns:", doctors_df.columns.tolist())

    print("Symptoms CSV loaded successfully")
    print("Symptoms columns:", symptoms_df.columns.tolist())

except Exception as e:
    print("CSV loading error:", e)
    doctors_df = pd.DataFrame()
    symptoms_df = pd.DataFrame()

# -----------------------------
# REQUEST MODEL
# -----------------------------
class RecommendationRequest(BaseModel):
    symptoms: str
    city: str
    language: str = ""
    top_k: int = 5

# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {"message": "Rural Connect Backend is running"}

# -----------------------------
# HELPER: MAP SYMPTOMS TO SPECIALIST
# -----------------------------
def map_symptom_to_specialist(user_symptom: str):
    user_symptom = user_symptom.lower().strip()

    best_match = None

    for _, row in symptoms_df.iterrows():
        symptom_text = str(row.get("symptom_or_condition", "")).lower()
        keywords = str(row.get("keywords", "")).lower()

        # Direct symptom match
        if user_symptom in symptom_text or symptom_text in user_symptom:
            return {
                "specialist": row.get("mapped_specialist", ""),
                "emergency_level": row.get("emergency_level", "Low")
            }

        # Keyword match
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
        if any(k in user_symptom for k in keyword_list):
            best_match = {
                "specialist": row.get("mapped_specialist", ""),
                "emergency_level": row.get("emergency_level", "Low")
            }

    return best_match

# -----------------------------
# RECOMMENDATION ENDPOINT
# -----------------------------
@app.post("/recommend")
def recommend_doctors(request: RecommendationRequest):
    try:
        if doctors_df.empty or symptoms_df.empty:
            raise HTTPException(status_code=500, detail="CSV data not loaded properly.")

        user_symptom = request.symptoms.strip()
        user_city = request.city.strip().lower()
        user_language = request.language.strip().lower()
        top_k = request.top_k

        # Step 1: Map symptom to specialist
        mapping = map_symptom_to_specialist(user_symptom)

        if not mapping:
            return {
                "recommendations": [],
                "message": f"No specialist mapping found for symptom/condition: {user_symptom}"
            }

        required_specialist = str(mapping["specialist"]).strip().lower()
        emergency_level = mapping["emergency_level"]

        # Step 2: Filter by specialist
        filtered = doctors_df[
            doctors_df["specialty"].str.lower().str.contains(required_specialist, na=False)
        ].copy()

        # Step 3: Filter by city
        filtered = filtered[
            filtered["city"].str.lower().str.contains(user_city, na=False)
        ].copy()

        # Step 4: Optional language filter
        if user_language:
            filtered = filtered[
                filtered["languages_spoken"].str.lower().str.contains(user_language, na=False)
            ].copy()

        if filtered.empty:
            return {
                "recommendations": [],
                "message": f"No doctors found for {required_specialist} in {request.city}"
            }

        # Step 5: Scoring logic
        def calculate_score(row):
            score = 0.0

            # Higher rating = better
            try:
                score += float(row.get("rating", 0)) * 2
            except:
                pass

            # Emergency supported = bonus
            if str(row.get("emergency_supported", "")).strip().lower() == "yes":
                score += 3.0

            # Video consult = bonus
            if str(row.get("video_consult_link", "")).strip():
                score += 1.5

            # Exact language match = bonus
            if user_language and user_language in str(row.get("languages_spoken", "")).lower():
                score += 2.0

            return score

        filtered["score"] = filtered.apply(calculate_score, axis=1)

        # Step 6: Sort and limit
        filtered = filtered.sort_values(by="score", ascending=False).head(top_k)

        # Step 7: Convert to JSON-friendly output
        recommendations = []
        for _, row in filtered.iterrows():
            recommendations.append({
                "doctor_id": row.get("doctor_id", ""),
                "doctor_name": row.get("doctor_name", ""),
                "specialty": row.get("specialty", ""),
                "subspecialty": row.get("subspecialty", ""),
                "hospital_name": row.get("hospital_name", ""),
                "city": row.get("city", ""),
                "area": row.get("area", ""),
                "languages_spoken": row.get("languages_spoken", ""),
                "phone_number": str(row.get("phone_number", "")),
                "consultation_mode": row.get("consultation_mode", ""),
                "booking_link": row.get("booking_link", ""),
                "video_consult_link": row.get("video_consult_link", ""),
                "emergency_supported": row.get("emergency_supported", ""),
                "rating": row.get("rating", ""),
                "score": round(float(row.get("score", 0)), 3),
                "matched_specialist": required_specialist.title(),
                "emergency_level": emergency_level
            })

        return {
            "recommendations": recommendations,
            "mapped_specialist": required_specialist.title(),
            "emergency_level": emergency_level,
            "total_found": len(recommendations)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")