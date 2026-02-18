import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Galaxy Watch 8 Dashboard", layout="wide")

st.title("Galaxy Watch 8 Performance Dashboard")

# ---------------------------------------------------
# Generate Random Data (If No CSV Uploaded)
# ---------------------------------------------------
def generate_random_data(days=7):
    data = []
    for i in range(days):
        steps = random.randint(4000, 15000)
        active_minutes = random.randint(20, 120)
        heart_rate = random.randint(55, 170)
        sleep_hours = round(random.uniform(5.5, 9), 2)
        deep_sleep = round(random.uniform(1, 2.5), 2)
        rem_sleep = round(random.uniform(1, 2.5), 2)
        stress = random.randint(10, 90)
        spo2 = random.uniform(92, 100)
        systolic = random.randint(105, 140)
        diastolic = random.randint(65, 90)
        carotenoids = random.uniform(20000, 50000)

        data.append([
            steps, active_minutes, heart_rate,
            sleep_hours, deep_sleep, rem_sleep,
            stress, spo2, systolic, diastolic, carotenoids
        ])

    columns = [
        "Steps", "Active Minutes", "Heart Rate",
        "Sleep Hours", "Deep Sleep", "REM Sleep",
        "Stress", "SpO2", "Systolic", "Diastolic", "Carotenoids"
    ]

    return pd.DataFrame(data, columns=columns)


# ---------------------------------------------------
# Energy Score (Recovery Based)
# ---------------------------------------------------
def calculate_energy_score(df):
    sleep_score = (df["Sleep Hours"].mean() / 8) * 40
    stress_score = (1 - df["Stress"].mean() / 100) * 30
    hr_score = (1 - (df["Heart Rate"].mean() - 60) / 100) * 30

    score = sleep_score + stress_score + hr_score
    return max(0, min(100, round(score, 1)))


# ---------------------------------------------------
# Antioxidant Index (Carotenoid Based)
# ---------------------------------------------------
def calculate_antioxidant_index(df):
    avg_carotenoids = df["Carotenoids"].mean()
    index = (avg_carotenoids / 50000) * 100
    return max(0, min(100, round(index, 1)))


# ---------------------------------------------------
# Upload CSV
# ---------------------------------------------------
uploaded_file = st.file_uploader("Upload Galaxy Watch CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded — using simulated Galaxy Watch data.")
    df = generate_random_data()

energy_score = calculate_energy_score(df)
antioxidant_index = calculate_antioxidant_index(df)

view = st.selectbox("Select Display Role", ["Athlete", "Trainer", "Doctor", "Coach"])

st.divider()

# ===================================================
# ATHLETE VIEW
# ===================================================
if view == "Athlete":
    st.header("Athlete Dashboard")

    st.metric("Average Steps", int(df["Steps"].mean()))
    st.metric("Active Minutes (avg)", int(df["Active Minutes"].mean()))
    st.metric("Energy Score", energy_score)
    st.metric("Sleep (avg hrs)", round(df["Sleep Hours"].mean(), 2))

    if energy_score < 50:
        st.warning("Low recovery detected. Consider rest.")
    else:
        st.success("Recovery status good.")


# ===================================================
# TRAINER VIEW
# ===================================================
elif view == "Trainer":
    st.header("Trainer Dashboard")

    st.write("Weekly Performance Overview")

    st.write("Avg Heart Rate:", int(df["Heart Rate"].mean()))
    st.write("Avg Stress Level:", int(df["Stress"].mean()))
    st.write("Total Active Minutes:", int(df["Active Minutes"].sum()))

    if df["Stress"].mean() > 70:
        st.error("Overtraining risk detected.")


# ===================================================
# DOCTOR VIEW
# ===================================================
elif view == "Doctor":
    st.header("Doctor Dashboard")

    st.write("Average SpO2:", round(df["SpO2"].mean(), 2))
    st.write("Blood Pressure Avg:",
             f"{int(df['Systolic'].mean())}/{int(df['Diastolic'].mean())}")

    st.write("Sleep Apnea Risk Check:")
    if df["SpO2"].mean() < 94:
        st.warning("Possible oxygen desaturation detected.")
    else:
        st.success("Oxygen levels normal.")

    st.write("Antioxidant Index:", antioxidant_index)


# ===================================================
# COACH VIEW
# ===================================================
elif view == "Coach":
    st.header("Coach Dashboard")

    st.write("Consistency Score:", round(df["Steps"].std(), 1))
    st.write("Energy Score:", energy_score)

    if df["Steps"].std() > 3000:
        st.warning("Inconsistent training load.")
    else:
        st.success("Training consistency good.")
