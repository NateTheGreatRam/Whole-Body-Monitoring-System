import streamlit as st
import pandas as pd

st.set_page_config(page_title="Galaxy Watch Performance Dashboard", layout="wide")

st.title("Galaxy Watch 8 Performance Dashboard")

# -----------------------------
# Upload Multiple CSV Files
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload one or more Galaxy Watch CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:

    dataframes = []

    for file in uploaded_files:
        df = pd.read_csv(file)
        dataframes.append(df)

    # Combine all CSVs
    df = pd.concat(dataframes, ignore_index=True)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convert date if available
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values("date")

    st.success(f"Loaded {len(uploaded_files)} files successfully.")
else:
    st.info("Please upload CSV files to begin.")
    st.stop()

# ----------------------------------
# Sidebar Role Selection
# ----------------------------------
role = st.sidebar.selectbox(
    "Select View",
    ["Athlete", "Trainer", "Coach", "Doctor"]
)

latest = df.iloc[-1]

# ==================================
# ATHLETE VIEW
# ==================================
if role == "Athlete":
    st.header("Athlete Dashboard")

    st.metric("Steps", latest.get("steps", "N/A"))
    st.metric("Calories", latest.get("calories", "N/A"))
    st.metric("Active Minutes", latest.get("active_minutes", "N/A"))
    st.metric("Heart Rate", latest.get("heart_rate", "N/A"))
    st.metric("Stress", latest.get("stress", "N/A"))
    st.metric("SpO2", latest.get("spo2", "N/A"))
    st.metric("Energy Score", latest.get("energy_score", "N/A"))
    st.metric("Body Fat %", latest.get("body_fat_percent", "N/A"))
    st.metric("Cycle Phase", latest.get("cycle_phase", "N/A"))
    st.metric("Sleep Apnea Events", latest.get("sleep_apnea_events", "N/A"))
    st.metric("ECG Status", latest.get("ecg_status", "N/A"))
    st.metric("Fall Detection", latest.get("fall_detected", "N/A"))

# ==================================
# TRAINER VIEW
# ==================================
elif role == "Trainer":
    st.header("Trainer Dashboard")

    st.metric("Steps", latest.get("steps", "N/A"))
    st.metric("Calories", latest.get("calories", "N/A"))
    st.metric("Active Minutes", latest.get("active_minutes", "N/A"))
    st.metric("Heart Rate", latest.get("heart_rate", "N/A"))
    st.metric("Stress", latest.get("stress", "N/A"))
    st.metric("SpO2", latest.get("spo2", "N/A"))
    st.metric("Blood Pressure", latest.get("blood_pressure", "N/A"))
    st.metric("Energy Score", latest.get("energy_score", "N/A"))
    st.metric("Sleep (Deep)", latest.get("deep_sleep_minutes", "N/A"))
    st.metric("Sleep (REM)", latest.get("rem_sleep_minutes", "N/A"))
    st.metric("Body Fat %", latest.get("body_fat_percent", "N/A"))

# ==================================
# COACH VIEW
# ==================================
elif role == "Coach":
    st.header("Coach Dashboard")

    st.metric("Active Minutes", latest.get("active_minutes", "N/A"))
    st.metric("Heart Rate", latest.get("heart_rate", "N/A"))
    st.metric("Training Load", df["heart_rate"].mean() if "heart_rate" in df else "N/A")
    st.metric("Energy Score", latest.get("energy_score", "N/A"))
    st.metric("Stress", latest.get("stress", "N/A"))
    st.metric("Sleep Summary (Total)", latest.get("total_sleep_minutes", "N/A"))
    st.metric("Body Fat % (Seasonal Avg)", df["body_fat_percent"].mean() if "body_fat_percent" in df else "N/A")
    st.metric("Cycle Phase", latest.get("cycle_phase", "N/A"))
    st.metric("Fall Detection", latest.get("fall_detected", "N/A"))

# ==================================
# DOCTOR VIEW
# ==================================
elif role == "Doctor":
    st.header("Doctor Dashboard")

    st.metric("Heart Rate", latest.get("heart_rate", "N/A"))
    st.metric("ECG", latest.get("ecg_status", "N/A"))
    st.metric("Blood Pressure", latest.get("blood_pressure", "N/A"))
    st.metric("SpO2", latest.get("spo2", "N/A"))
    st.metric("Sleep Apnea Events", latest.get("sleep_apnea_events", "N/A"))
    st.metric("Stress", latest.get("stress", "N/A"))
    st.metric("Body Fat %", latest.get("body_fat_percent", "N/A"))
    st.metric("Cycle Phase", latest.get("cycle_phase", "N/A"))
    st.metric("Antioxidant Index", latest.get("carotenoids_score", "N/A"))
    st.metric("Fall Detection", latest.get("fall_detected", "N/A"))
    st.metric("Energy Score Trend (Avg)", df["energy_score"].mean() if "energy_score" in df else "N/A")
