import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import os

st.set_page_config(page_title="AI Lifestyle Optimizer", layout="centered")

# ---------- Load/Create Logs ----------
LOG_FILE = "user_logs.csv"

if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["date", "mood", "productivity", "sleep_hours", "screen_time", "wellness_score", "micro_habit"])
    df.to_csv(LOG_FILE, index=False)

df = pd.read_csv(LOG_FILE)

# ---------- Title ----------
st.title("🧠 AI Lifestyle Optimizer")
st.markdown("Track mood, sleep, screen time & get AI wellness tips!")

# ---------- Input Form ----------
with st.form("daily_checkin"):
    st.subheader("📋 Daily Check-in")

    mood = st.select_slider("How do you feel today?", options=["😞", "😐", "🙂", "😄"])
    productivity = st.slider("How productive were you today? (1 = Low, 10 = High)", 1, 10)
    sleep_hours = st.slider("Hours you slept last night", 0.0, 12.0, step=0.5)
    screen_time = st.slider("Screen time today (in hours)", 0.0, 16.0, step=0.5)

    submitted = st.form_submit_button("Submit")

# ---------- Wellness Score Logic ----------
def calculate_wellness_score(mood, productivity, sleep_hours, screen_time):
    mood_score = {"😞": 2, "😐": 5, "🙂": 8, "😄": 10}[mood]
    sleep_score = max(0, 10 - abs(8 - sleep_hours) * 2)
    screen_penalty = max(0, 10 - screen_time)
    return round((mood_score * 0.3 + productivity * 0.3 + sleep_score * 0.2 + screen_penalty * 0.2), 2)

def get_micro_habit(score):
    habits = [
        "Drink 2L water today 💧",
        "Go for a 15-min walk 🚶‍♂️",
        "Meditation for 5 mins 🧘",
        "No screens 1 hour before bed 📵",
        "Write one thing you're grateful for ✍️"
    ]
    if score < 5:
        return random.choice(habits[:3])
    else:
        return random.choice(habits[2:])

# ---------- On Submit ----------
if submitted:
    today = datetime.now().strftime("%Y-%m-%d")
    score = calculate_wellness_score(mood, productivity, sleep_hours, screen_time)
    habit = get_micro_habit(score)

    new_row = {
        "date": today,
        "mood": mood,
        "productivity": productivity,
        "sleep_hours": sleep_hours,
        "screen_time": screen_time,
        "wellness_score": score,
        "micro_habit": habit
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

    st.success(f"✅ Logged! Your Wellness Score today: **{score}/10**")
    st.info(f"🧠 Today's Micro Habit: **{habit}**")

# ---------- Mood Journal ----------
st.subheader("📈 Mood Journal & Streak Tracker")

if df.empty:
    st.write("No data yet. Do a daily check-in!")
else:
    st.line_chart(df.set_index("date")[["wellness_score", "productivity"]])

    streak = 0
    for d in reversed(df["date"].tolist()):
        if d == (datetime.now() - pd.Timedelta(days=streak)).strftime("%Y-%m-%d"):
            streak += 1
        else:
            break
    st.markdown(f"🔥 **Current Check-in Streak: {streak} day(s)**")

# ---------- Footer ----------
st.markdown("---")
st.caption("Built with 💙 for wellness hackathons")
