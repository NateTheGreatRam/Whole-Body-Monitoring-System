import streamlit as st
import pandas as pd
import numpy as np
import random

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Galaxy Watch 8 Pro Dashboard",
    layout="wide",
    page_icon="⌚"
)

# -------------------------------------------------
# CUSTOM DARK THEME STYLING
# -------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.metric-title {
    font-size: 16px;
    color: #94a3b8;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}
.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
}
.good {color: #22c55e; font-weight: bold;}
.warning {color: #facc15; font-weight: bold;}
.danger {color: #ef4444; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("⌚ Galaxy Watch 8 Performance Intelligence System")

# -------------------------------------------------
# DATA GENERATOR
# -------------------------------------------------
def generate_data(days=14):
    data = []
    for i in range(days):
        data.append([
            random.randint(3000,16000),  # steps
            random.randint(1800,3500),   # calories
            random.randint(20,150),      # active
            random.randint(55,180),      # hr
            random.randint(10,95),       # stress
            random.uniform(90,100),      # spo2
            random.randint(105,145),     # sys
            random.randint(65,95),       # dia
            random.uniform(0.5,2.5),     # deep
            random.uniform(0.5,2.5),     # rem
            random.uniform(2,5),         # light
            random.randint(0,15),        # apnea
            random.uniform(12,25),       # fat
            random.uniform(70,95),       # muscle
            random.uniform(20000,50000), # carot
            random.choice([0,0,0,1]),    # ecg
            random.choice([0,0,0,1]),    # fall
            random.choice(["Follicular","Ovulation","Luteal","Menstrual"])
        ])
    columns = ["Steps","Calories","Active","HR","Stress","SpO2",
               "Sys","Dia","Deep","REM","Light","Apnea",
               "Fat","Muscle","Carot","ECG","Fall","Cycle"]
    return pd.DataFrame(data, columns=columns)

df = generate_data()

# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------
def energy_score(df):
    sleep = (df["Deep"].mean()+df["REM"].mean()+df["Light"].mean())/8*40
    stress = (1 - df["Stress"].mean()/100)*30
    hr = (1 - (df["HR"].mean()-60)/120)*30
    return round(max(0,min(100,sleep+stress+hr)),1)

def antioxidant(df):
    return round((df["Carot"].mean()/50000)*100,1)

energy = energy_score(df)
antiox = antioxidant(df)

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
st.sidebar.title("Select Role")
role = st.sidebar.radio(
    "Dashboard View",
    ["Athlete","Trainer","Coach","Doctor"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### ⚡ Energy Score: {energy}")
st.sidebar.markdown(f"### 🥕 Antioxidant: {antiox}")

# -------------------------------------------------
# CARD FUNCTION
# -------------------------------------------------
def card(title,value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# =================================================
# ATHLETE
# =================================================
if role == "Athlete":
    st.header("🏃 Athlete Performance View")

    col1,col2,col3 = st.columns(3)
    with col1:
        card("Steps (avg)", int(df["Steps"].mean()))
        card("Calories (avg)", int(df["Calories"].mean()))
        card("Active Minutes", int(df["Active"].mean()))

    with col2:
        card("Heart Rate (avg)", int(df["HR"].mean()))
        card("SpO₂", round(df["SpO2"].mean(),1))
        card("Stress Level", int(df["Stress"].mean()))

    with col3:
        card("Energy Score", energy)
        card("Body Fat %", round(df["Fat"].mean(),1))
        card("Muscle Mass", round(df["Muscle"].mean(),1))

    st.subheader("Sleep Stages")
    card("Deep Sleep", round(df["Deep"].mean(),2))
    card("REM Sleep", round(df["REM"].mean(),2))
    card("Light Sleep", round(df["Light"].mean(),2))

    if df["Apnea"].mean() > 5:
        st.markdown("<div class='danger'>Sleep Apnea Risk Detected</div>", unsafe_allow_html=True)

    if df["ECG"].sum()>0:
        st.markdown("<div class='warning'>ECG Irregularity Recorded</div>", unsafe_allow_html=True)

    st.write("Cycle Phase:", df["Cycle"].iloc[-1])
    st.write("Fall Events:", df["Fall"].sum())

# =================================================
# TRAINER
# =================================================
elif role == "Trainer":
    st.header("🏋️ Trainer Load Monitoring")

    card("Training Load (HR avg)", int(df["HR"].mean()))
    card("Steps", int(df["Steps"].mean()))
    card("Active Minutes", int(df["Active"].mean()))
    card("Calories", int(df["Calories"].mean()))
    card("Energy Score", energy)

    st.subheader("Recovery Indicators")
    card("Stress", int(df["Stress"].mean()))
    card("Sleep Avg (hrs)",
         round(df["Deep"].mean()+df["REM"].mean()+df["Light"].mean(),2))

    st.subheader("Vitals")
    card("Blood Pressure",
         f"{int(df['Sys'].mean())}/{int(df['Dia'].mean())}")
    card("SpO₂", round(df["SpO2"].mean(),1))

# =================================================
# COACH
# =================================================
elif role == "Coach":
    st.header("🎯 Coach Performance Intelligence")

    card("Active Minutes", int(df["Active"].mean()))
    card("Training Load", int(df["HR"].mean()))
    card("Energy Score", energy)
    card("Stress Level", int(df["Stress"].mean()))

    st.subheader("Sleep Summary")
    card("Deep", round(df["Deep"].mean(),2))
    card("REM", round(df["REM"].mean(),2))
    card("Light", round(df["Light"].mean(),2))

    st.subheader("Body Composition Trend")
    card("Body Fat %", round(df["Fat"].mean(),1))
    card("Muscle Mass", round(df["Muscle"].mean(),1))

    st.write("Fall Events:", df["Fall"].sum())
    if st.checkbox("Athlete opted to share menstrual data"):
        st.write("Cycle Phase:", df["Cycle"].iloc[-1])

# =================================================
# DOCTOR
# =================================================
elif role == "Doctor":
    st.header("🩺 Clinical Overview")

    card("Heart Rate", int(df["HR"].mean()))
    card("Blood Pressure",
         f"{int(df['Sys'].mean())}/{int(df['Dia'].mean())}")
    card("SpO₂", round(df["SpO2"].mean(),1))
    card("Stress", int(df["Stress"].mean()))
    card("Energy Score (Trend Avg)", energy)

    if df["ECG"].sum()>0:
        st.markdown("<div class='danger'>Abnormal ECG Reading</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='good'>ECG Normal</div>", unsafe_allow_html=True)

    if df["Apnea"].mean()>5:
        st.markdown("<div class='danger'>Sleep Apnea Risk</div>", unsafe_allow_html=True)

    st.subheader("Body Composition")
    card("Body Fat %", round(df["Fat"].mean(),1))
    card("Muscle Mass", round(df["Muscle"].mean(),1))

    st.write("Menstrual Cycle:", df["Cycle"].iloc[-1])
    card("Antioxidant Index", antiox)
    st.write("Fall Events:", df["Fall"].sum())
