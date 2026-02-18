import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Galaxy Watch 8 Role Dashboard", layout="wide")
st.title("Galaxy Watch 8 Multi-Role Health Dashboard")

# ---------------------------------------------------------
# RANDOM DATA GENERATOR (SIMULATED GALAXY WATCH 8 DATA)
# ---------------------------------------------------------
def generate_data(days=14):
    data = []
    for i in range(days):

        steps = random.randint(3000, 16000)
        calories = random.randint(1800, 3500)
        active_minutes = random.randint(20, 150)
        heart_rate = random.randint(55, 180)
        stress = random.randint(10, 95)
        spo2 = random.uniform(90, 100)
        systolic = random.randint(105, 145)
        diastolic = random.randint(65, 95)
        deep = random.uniform(0.5, 2.5)
        rem = random.uniform(0.5, 2.5)
        light = random.uniform(2, 5)
        sleep_hours = deep + rem + light
        apnea_events = random.randint(0, 15)
        body_fat = random.uniform(12, 25)
        muscle_mass = random.uniform(70, 95)
        carotenoids = random.uniform(20000, 50000)
        ecg_abnormal = random.choice([0, 0, 0, 1])  # mostly normal
        fall_detected = random.choice([0, 0, 0, 1])
        cycle_phase = random.choice(["Follicular", "Ovulation", "Luteal", "Menstrual"])

        data.append([
            steps, calories, active_minutes, heart_rate,
            stress, spo2, systolic, diastolic,
            deep, rem, light, sleep_hours,
            apnea_events, body_fat, muscle_mass,
            carotenoids, ecg_abnormal, fall_detected,
            cycle_phase
        ])

    columns = [
        "Steps","Calories","Active Minutes","Heart Rate",
        "Stress","SpO2","Systolic","Diastolic",
        "Deep Sleep","REM Sleep","Light Sleep","Sleep Hours",
        "Apnea Events","Body Fat %","Muscle Mass",
        "Carotenoids","ECG Abnormal","Fall Detected",
        "Cycle Phase"
    ]

    return pd.DataFrame(data, columns=columns)

df = generate_data()

# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------

def energy_score(df):
    sleep_component = (df["Sleep Hours"].mean()/8)*40
    stress_component = (1 - df["Stress"].mean()/100)*30
    hr_component = (1 - (df["Heart Rate"].mean()-60)/120)*30
    score = sleep_component + stress_component + hr_component
    return max(0, min(100, round(score,1)))

def antioxidant_index(df):
    return round((df["Carotenoids"].mean()/50000)*100,1)

def training_zone(hr):
    if hr < 100:
        return "Zone 1 (Recovery)"
    elif hr < 130:
        return "Zone 2 (Endurance)"
    elif hr < 160:
        return "Zone 3 (Tempo)"
    else:
        return "Zone 4/5 (High Intensity)"

def sleep_apnea_risk(df):
    return df["Apnea Events"].mean() > 5

energy = energy_score(df)
antioxidant = antioxidant_index(df)

role = st.selectbox("Select Role View",
                    ["Coach","Trainer","Doctor","Athlete"])

st.divider()

# =========================================================
# COACH
# =========================================================
if role == "Coach":
    st.header("Coach View")

    st.write("Active Minutes (avg):", int(df["Active Minutes"].mean()))
    st.write("Training Load (Avg HR):", int(df["Heart Rate"].mean()))
    st.write("Energy Score:", energy)
    st.write("Stress Level (avg):", int(df["Stress"].mean()))

    st.subheader("Sleep Stage Summary")
    st.write("Deep:", round(df["Deep Sleep"].mean(),2),"hrs")
    st.write("REM:", round(df["REM Sleep"].mean(),2),"hrs")
    st.write("Light:", round(df["Light Sleep"].mean(),2),"hrs")

    st.write("Fall Detection Events:", int(df["Fall Detected"].sum()))

    st.subheader("Seasonal Body Composition")
    st.write("Body Fat % (avg):", round(df["Body Fat %"].mean(),1))
    st.write("Muscle Mass (avg):", round(df["Muscle Mass"].mean(),1))

    if st.checkbox("Athlete opted to share menstrual data"):
        st.write("Current Cycle Phase:",
                 df["Cycle Phase"].iloc[-1])


# =========================================================
# TRAINER
# =========================================================
elif role == "Trainer":
    st.header("Trainer View")

    st.write("Steps (avg):", int(df["Steps"].mean()))
    st.write("Calories (avg):", int(df["Calories"].mean()))
    st.write("Active Minutes (avg):", int(df["Active Minutes"].mean()))

    avg_hr = df["Heart Rate"].mean()
    st.write("Training Zone:", training_zone(avg_hr))

    st.write("Energy Score:", energy)
    st.write("Stress Level (avg):", int(df["Stress"].mean()))

    st.subheader("Sleep Stages")
    st.write("Deep:", round(df["Deep Sleep"].mean(),2))
    st.write("REM:", round(df["REM Sleep"].mean(),2))
    st.write("Light:", round(df["Light Sleep"].mean(),2))

    st.subheader("Body Composition")
    st.write("Body Fat %:", round(df["Body Fat %"].mean(),1))
    st.write("Muscle Mass:", round(df["Muscle Mass"].mean(),1))

    st.write("Blood Pressure:",
             f"{int(df['Systolic'].mean())}/{int(df['Diastolic'].mean())}")
    st.write("Blood Oxygen (SpO2):", round(df["SpO2"].mean(),1))


# =========================================================
# DOCTOR
# =========================================================
elif role == "Doctor":
    st.header("Doctor View")

    st.write("Heart Rate (avg):", int(df["Heart Rate"].mean()))

    if df["ECG Abnormal"].sum() > 0:
        st.warning("Abnormal ECG readings detected.")
    else:
        st.success("ECG Normal")

    st.write("Blood Pressure:",
             f"{int(df['Systolic'].mean())}/{int(df['Diastolic'].mean())}")
    st.write("Blood Oxygen (SpO2):", round(df["SpO2"].mean(),1))

    if sleep_apnea_risk(df):
        st.error("Sleep Apnea Risk Detected")
    else:
        st.success("No Sleep Apnea Risk")

    st.write("Stress Level (avg):", int(df["Stress"].mean()))

    st.subheader("Body Composition")
    st.write("Body Fat %:", round(df["Body Fat %"].mean(),1))
    st.write("Muscle Mass:", round(df["Muscle Mass"].mean(),1))

    st.write("Menstrual Cycle Phase:",
             df["Cycle Phase"].iloc[-1])

    st.write("Antioxidant Index:", antioxidant)

    st.write("Fall Detection Events:", int(df["Fall Detected"].sum()))

    st.subheader("Energy Score Trend (14 Day Avg)")
    st.write("Current Energy Score:", energy)


# =========================================================
# ATHLETE
# =========================================================
elif role == "Athlete":
    st.header("Athlete View")

    st.write("Steps (avg):", int(df["Steps"].mean()))
    st.write("Calories (avg):", int(df["Calories"].mean()))
    st.write("Active Minutes (avg):", int(df["Active Minutes"].mean()))
    st.write("Heart Rate (avg):", int(df["Heart Rate"].mean()))

    st.subheader("Sleep Breakdown")
    st.write("Deep:", round(df["Deep Sleep"].mean(),2))
    st.write("REM:", round(df["REM Sleep"].mean(),2))
    st.write("Light:", round(df["Light Sleep"].mean(),2))

    if sleep_apnea_risk(df):
        st.warning("Possible Sleep Apnea Risk")

    st.write("Stress Level (avg):", int(df["Stress"].mean()))
    st.write("Blood Oxygen (SpO2):", round(df["SpO2"].mean(),1))
    st.write("Energy Score:", energy)

    st.subheader("Body Composition")
    st.write("Body Fat %:", round(df["Body Fat %"].mean(),1))
    st.write("Muscle Mass:", round(df["Muscle Mass"].mean(),1))

    st.write("Menstrual Cycle Phase:",
             df["Cycle Phase"].iloc[-1])

    if df["ECG Abnormal"].sum() > 0:
        st.warning("Abnormal ECG reading recorded.")

    st.write("Fall Detection Events:", int(df["Fall Detected"].sum()))
