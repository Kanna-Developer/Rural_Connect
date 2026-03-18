# backend/data_loader.py

import pandas as pd
from config import DOCTORS_CSV_PATH, SYMPTOM_MAP_CSV_PATH

def load_doctors():
    try:
        df = pd.read_csv(DOCTORS_CSV_PATH)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load doctors CSV: {e}")

def load_symptom_map():
    try:
        df = pd.read_csv(SYMPTOM_MAP_CSV_PATH)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load symptom map CSV: {e}")
    