# ================================
# LOCKED HEALTH METRICS SYSTEM
# ================================

def clean_columns(df):

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("%","", regex=False)
        .str.replace("(","", regex=False)
        .str.replace(")","", regex=False)
    )

    # Approved column mapping ONLY
    mapping = {
        "steps": "Steps",
        "calories": "Calories",
        "active minutes": "Active",
        "active": "Active",
        "heart rate": "HR",
        "heart rate bpm": "HR",
        "hr": "HR",
        "ecg": "ECG",
        "ecg abnormal": "ECG",
        "blood oxygen": "SpO2",
        "spo2": "SpO2",
        "stress": "Stress",
        "cycle phase": "Cycle",
        "menstrual cycle": "Cycle",
        "body fat": "Fat",
        "muscle mass": "Muscle",
        "deep sleep": "Deep",
        "deep sleep min": "Deep",
        "rem sleep": "REM",
        "rem sleep min": "REM",
        "light sleep": "Light",
        "light sleep min": "Light",
        "sleep apnea events": "Apnea",
        "systolic": "Sys",
        "diastolic": "Dia",
        "blood pressure systolic": "Sys",
        "blood pressure diastolic": "Dia",
        "antioxidant index": "Carot",
        "carotenoids": "Carot",
        "fall detected": "Fall"
    }

    df = df.rename(columns=mapping)

    # Keep ONLY approved metrics
    approved_columns = [
        "Steps", "Calories", "Active", "HR", "ECG", "SpO2",
        "Cycle", "Stress", "Fat", "Muscle",
        "Deep", "REM", "Light",
        "Apnea", "Sys", "Dia",
        "Carot", "Fall"
    ]

    df = df[[col for col in df.columns if col in approved_columns]]

    # Convert numeric columns safely
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df


# ================================
# USE AFTER CSV LOAD
# ================================

# Example:
# df = pd.read_csv(uploaded_file)
# df = clean_columns(df)
