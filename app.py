import pandas as pd
import random
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

# Step 1: Generate random data
def generate_random_data(num_records=30):
    today = datetime.today()
    dates = [today - timedelta(days=i) for i in range(num_records)]

    data = {
        'Date': dates,
        'Steps': [random.randint(2000, 10000) for _ in range(num_records)],
        'Calories': [random.randint(1500, 3500) for _ in range(num_records)],
        'HeartRate': [random.randint(60, 180) for _ in range(num_records)],
        'SpO2': [random.uniform(95.0, 100.0) for _ in range(num_records)],
        'StressLevel': [random.uniform(20.0, 100.0) for _ in range(num_records)],
        'ActivityMinutes': [random.randint(20, 120) for _ in range(num_records)],
        'SleepTime': [random.randint(6, 9) for _ in range(num_records)],
        'DeepSleep': [random.randint(2, 3) for _ in range(num_records)],
        'LightSleep': [random.randint(2, 3) for _ in range(num_records)],
        'REM': [random.randint(1, 2) for _ in range(num_records)],
        'Systolic': [random.randint(100, 140) for _ in range(num_records)],
        'Diastolic': [random.randint(60, 90) for _ in range(num_records)],
        'ECG': [random.choice([0, 1]) for _ in range(num_records)],
        'MenstrualCycle': [random.choice([None, 'Ovulation', 'Menstrual']) for _ in range(num_records)],
    }
    return pd.DataFrame(data)

# Step 2: Data Processing Functions
def process_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['SleepDuration'] = df['DeepSleep'] + df['LightSleep'] + df['REM']
    df['SleepScore'] = (0.4 * df['SleepDuration']) + (0.3 * df['SleepTime']) + (0.3 * (df['DeepSleep'] / df['SleepDuration']))
    df['ActivityScore'] = (df['ActivityMinutes'] / 60) * 10  # Simple scaling
    return df

def calculate_energy_score(df):
    df['EnergyScore'] = (0.35 * df['SleepScore']) + (0.30 * df['ActivityScore']) + (0.20 * df['HeartRate'].apply(lambda x: 100 - x)) + (0.15 * (df['StressLevel'] / 100))
    return df

# Step 3: Display Functions for Athlete, Trainer, Doctor, and Coach
def athlete_display(df):
    fig, ax = plt.subplots(3, 1, figsize=(10, 12))

    ax[0].plot(df['Date'], df['Steps'], color='b', label="Steps")
    ax[0].set_title("Daily Steps")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("Steps")

    ax[1].plot(df['Date'], df['Calories'], color='g', label="Calories")
    ax[1].set_title("Calories Burned")
    ax[1].set_xlabel("Date")
    ax[1].set_ylabel("Calories")

    ax[2].plot(df['Date'], df['EnergyScore'], color='r', label="Energy Score")
    ax[2].set_title("Energy Score")
    ax[2].set_xlabel("Date")
    ax[2].set_ylabel("Score")

    plt.tight_layout()
    st.pyplot(fig)

def trainer_display(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['HeartRate'], color='purple', label="Heart Rate")
    ax.set_title("Heart Rate Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Heart Rate (BPM)")

    plt.tight_layout()
    st.pyplot(fig)

def doctor_display(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['SpO2'], color='blue', label="SpO2")
    ax.set_title("Blood Oxygen (SpO2)")
    ax.set_xlabel("Date")
    ax.set_ylabel("SpO2 (%)")

    plt.tight_layout()
    st.pyplot(fig)

def coach_display(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['EnergyScore'], color='orange', label="Energy Score")
    ax.set_title("Energy Score Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Energy Score")

    plt.tight_layout()
    st.pyplot(fig)

# Step 4: Streamlit App Layout
def main():
    st.title("Galaxy Watch 8 Health Data Dashboard")

    # Select user role
    user_type = st.selectbox("Select User Type", ['Athlete', 'Trainer', 'Doctor', 'Coach'])

    # Simulate random data and process it
    df = generate_random_data(num_records=30)
    df = process_data(df)
    df = calculate_energy_score(df)

    # Display based on user type
    if user_type == 'Athlete':
        athlete_display(df)
    elif user_type == 'Trainer':
        trainer_display(df)
    elif user_type == 'Doctor':
        doctor_display(df)
    elif user_type == 'Coach':
        coach_display(df)

# Run the app
if __name__ == "__main__":
    main()
