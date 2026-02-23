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

st.title("⌚ Galaxy Watch 8 Performance Intelligence System")

# -------------------------------------------------
# DARK UI STYLE
# -------------------------------------------------
st.markdown("""
<style>
.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.metric-title { font-size:16px; color:#94a3b8; }
.metric-value { font-size:28px; font-weight:bold; color:white; }
.good {color:#22c55e; font-weight:bold;}
.warning {color:#facc15; font-weight:bold;}
.danger {color:#ef4444; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DEFAULT SIMULATED DATA (FALLBACK)
# -------------------------------------------------
def generate_data(days=14):
    random.seed(42)
    np.random.seed(42)

    data = []
    for i in range(days):
        data.append([
            random.randint(3000,16000),
            random.randint(1800,3500),
            random.randint(20,150),
            random.randint(55,180),
            random.randint(10,95),
            random.uniform(90,100),
            random.randint(105,145),
            random.randint(65,95),
            random.uniform(0.5,2.5),
            random.uniform(0.5,2.5),
            random.uniform(2,5),
            random.randint(0,15),
            random.uniform(12,25),
            random.uniform(70,95),
            random.uniform(20000,50000),
            random.choice([0,0,0,1]),
            random.choice([0,0,0,1]),
            random.choice(["Follicular","Ovulation","Luteal","Menstrual"])
        ])
    columns = ["Steps","Calories","Active","HR","Stress","SpO2",
               "Sys","Dia","Deep","REM","Light","Apnea",
               "Fat","Muscle","Carot","ECG","Fall","Cycle"]
    return pd.DataFrame(data, columns=columns)

# -------------------------------------------------
# CSV INGESTION
# -------------------------------------------------
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()

    mapping = {
        "steps": "Steps",
        "calories": "Calories",
        "active minutes": "Active",
        "heart rate": "HR",
        "stress": "Stress",
        "spo2": "SpO2",
        "blood oxygen": "SpO2",
        "systolic": "Sys",
        "diastolic": "Dia",
        "deep sleep": "Deep",
        "rem sleep": "REM",
        "light sleep": "Light",
        "sleep apnea events": "Apnea",
        "body fat": "Fat",
        "muscle mass": "Muscle",
        "carotenoids": "Carot",
        "ecg abnormal": "ECG",
        "fall detected": "Fall",
        "cycle phase": "Cycle"
    }

    df = df.rename(columns=mapping)
    return df

uploaded_file = st.sidebar.file_uploader("Upload Galaxy Watch CSV", type=["csv"])

if uploaded_file:
    raw_df = pd.read_csv(uploaded_file)
    df = clean_columns(raw_df)
    st.sidebar.success("Real Galaxy Watch data loaded.")
else:
    if "galaxy_data" not in st.session_state:
        st.session_state.galaxy_data = generate_data()
    df = st.session_state.galaxy_data
    st.sidebar.info("Using simulated demo data.")

# -------------------------------------------------
# SAFE COLUMN ACCESS (prevents crashes)
# -------------------------------------------------
def get_col(name, default=0):
    return df[name] if name in df.columns else pd.Series([default]*len(df))

# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------
def energy_score():
    deep = get_col("Deep").mean()
    rem = get_col("REM").mean()
    light = get_col("Light").mean()
    stress = get_col("Stress").mean()
    hr = get_col("HR").mean()

    sleep_component = (deep+rem+light)/8*40
    stress_component = (1 - stress/100)*30
    hr_component = (1 - (hr-60)/120)*30

    return round(max(0,min(100,sleep_component+stress_component+hr_component)),1)

def antioxidant():
    return round((get_col("Carot").mean()/50000)*100,1)

energy = energy_score()
antiox = antioxidant()

# -------------------------------------------------
# CARD UI
# -------------------------------------------------
def card(title,value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# ROLE SELECTION
# -------------------------------------------------
role = st.sidebar.radio("Select Role",
                        ["Athlete","Trainer","Coach","Doctor"])

st.sidebar.markdown(f"### ⚡ Energy Score: {energy}")
st.sidebar.markdown(f"### 🥕 Antioxidant: {antiox}")

# =================================================
# ATHLETE
# =================================================
if role == "Athlete":
    st.header("🏃 Athlete View")
    card("Steps", int(get_col("Steps").mean()))
    card("Calories", int(get_col("Calories").mean()))
    card("Active Minutes", int(get_col("Active").mean()))
    card("Heart Rate", int(get_col("HR").mean()))
    card("SpO₂", round(get_col("SpO2").mean(),1))
    card("Stress", int(get_col("Stress").mean()))
    card("Energy Score", energy)
    card("Body Fat %", round(get_col("Fat").mean(),1))
    card("Muscle Mass", round(get_col("Muscle").mean(),1))
    card("Cycle Phase", get_col("Cycle").iloc[-1] if "Cycle" in df.columns else "N/A")
    card("Fall Events", int(get_col("Fall").sum()))

# =================================================
# TRAINER
# =================================================
elif role == "Trainer":
    st.header("🏋️ Trainer View")
    card("Steps", int(get_col("Steps").mean()))
    card("Calories", int(get_col("Calories").mean()))
    card("Active Minutes", int(get_col("Active").mean()))
    card("Training Load (HR)", int(get_col("HR").mean()))
    card("Stress", int(get_col("Stress").mean()))
    card("Blood Pressure",
         f"{int(get_col('Sys').mean())}/{int(get_col('Dia').mean())}")
    card("SpO₂", round(get_col("SpO2").mean(),1))
    card("Energy Score", energy)

# =================================================
# COACH
# =================================================
elif role == "Coach":
    st.header("🎯 Coach View")
    card("Active Minutes", int(get_col("Active").mean()))
    card("Training Load", int(get_col("HR").mean()))
    card("Stress", int(get_col("Stress").mean()))
    card("Energy Score", energy)
    card("Deep Sleep", round(get_col("Deep").mean(),2))
    card("REM Sleep", round(get_col("REM").mean(),2))
    card("Light Sleep", round(get_col("Light").mean(),2))
    card("Body Fat %", round(get_col("Fat").mean(),1))
    card("Muscle Mass", round(get_col("Muscle").mean(),1))
    card("Fall Events", int(get_col("Fall").sum()))

# =================================================
# DOCTOR
# =================================================
elif role == "Doctor":
    st.header("🩺 Doctor View")
    card("Heart Rate", int(get_col("HR").mean()))
    card("Blood Pressure",
         f"{int(get_col('Sys').mean())}/{int(get_col('Dia').mean())}")
    card("SpO₂", round(get_col("SpO2").mean(),1))
    card("Stress", int(get_col("Stress").mean()))
    card("Energy Score (Trend)", energy)
    card("Antioxidant Index", antiox)
    card("Body Fat %", round(get_col("Fat").mean(),1))
    card("Muscle Mass", round(get_col("Muscle").mean(),1))
    card("Cycle Phase", get_col("Cycle").iloc[-1] if "Cycle" in df.columns else "N/A")
    card("Fall Events", int(get_col("Fall").sum()))
