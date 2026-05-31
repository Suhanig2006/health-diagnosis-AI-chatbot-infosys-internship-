import pandas as pd
import re

# ---------- Load Reference CSV ----------
def load_reference_ranges(csv_path):
    df = pd.read_csv(csv_path)
    df["parameter"] = df["parameter"].str.lower().str.strip()
    df["gender"] = df["gender"].str.lower().str.strip()
    return df

# ---------- Normalize Gender ----------
def normalize_gender(text):
    text = text.lower()
    if "female" in text or "f" in text:
        return "female"
    if "male" in text or "m" in text:
        return "male"
    return "any"

# ---------- Extract Age ----------
def extract_age(text):
    match = re.search(r'(\d{1,3})\s*(years|yrs|y)?', text.lower())
    return int(match.group(1)) if match else None

# ---------- Extract Parameters ----------
PARAMETER_PATTERNS = {
    "hemoglobin": r"(hemoglobin|hb)\s*[:\-]?\s*(\d+\.?\d*)",
    "rbc count": r"(rbc)\s*[:\-]?\s*(\d+\.?\d*)",
    "wbc count": r"(wbc)\s*[:\-]?\s*(\d+\.?\d*)",
    "platelet count": r"(platelet)\s*[:\-]?\s*(\d+)",
    "glucose (fasting)": r"(glucose).*?(\d+\.?\d*)",
    "hba1c": r"(hba1c)\s*[:\-]?\s*(\d+\.?\d*)",
    "total cholesterol": r"(total cholesterol)\s*[:\-]?\s*(\d+)",
    "ldl cholesterol": r"(ldl)\s*[:\-]?\s*(\d+)",
    "hdl cholesterol": r"(hdl)\s*[:\-]?\s*(\d+)",
    "triglycerides": r"(triglycerides)\s*[:\-]?\s*(\d+)",
    "creatinine": r"(creatinine)\s*[:\-]?\s*(\d+\.?\d*)",
}

def extract_parameters(text):
    results = {}
    text_lower = text.lower()
    for param, pattern in PARAMETER_PATTERNS.items():
        match = re.search(pattern, text_lower)
        if match:
            results[param] = float(match.group(2))
    return results

# ---------- Compare With Reference ----------
def analyze_report(text, csv_path):
    ref_df = load_reference_ranges(csv_path)

    age = extract_age(text)
    gender = normalize_gender(text)
    parameters = extract_parameters(text)

    analysis = []

    for param, value in parameters.items():
        matches = ref_df[
            (ref_df["parameter"] == param) &
            ((ref_df["gender"] == gender) | (ref_df["gender"] == "any")) &
            (ref_df["min_age"] <= age) &
            (ref_df["max_age"] >= age)
        ]

        if matches.empty:
            status = "Reference not found"
            risk = "Unknown"
        else:
            lower = matches.iloc[0]["lower"]
            upper = matches.iloc[0]["upper"]

            if value < lower:
                status = "Low"
                risk = "Possible deficiency"
            elif value > upper:
                status = "High"
                risk = "Possible risk"
            else:
                status = "Normal"
                risk = "Healthy"

        analysis.append({
            "parameter": param,
            "value": value,
            "status": status,
            "risk": risk
        })

    return {
        "age": age,
        "gender": gender,
        "results": analysis
    }