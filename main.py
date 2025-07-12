# EPO + BPC-157 Cycle Tracker for Umar
# Interactive Python Dashboard using Streamlit

import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="EPO + BPC-157 Cycle Tracker", layout="centered")
st.title("🩸 EPO + BPC-157 Cycle Tracker")

# Sidebar inputs
st.sidebar.header("🔧 Input Daily Metrics")
today = st.sidebar.date_input("Date", datetime.date.today())
resting_hr = st.sidebar.number_input("Resting Heart Rate (bpm)", min_value=30, max_value=200, value=45)
bp_systolic = st.sidebar.number_input("Systolic BP", min_value=80, max_value=200, value=120)
bp_diastolic = st.sidebar.number_input("Diastolic BP", min_value=40, max_value=150, value=75)
epo_dose = st.sidebar.selectbox("EPO Injected Today?", ["No", "2,000 IU"])
bpc_dose = st.sidebar.selectbox("BPC-157 Injected Today?", ["None", "250 mcg", "250 mcg (x2)"])
notes = st.sidebar.text_area("Notes (pain, fatigue, etc.)")

# Save daily entry
if 'log' not in st.session_state:
    st.session_state.log = []

if st.sidebar.button("➕ Log Entry"):
    st.session_state.log.append({
        'Date': today,
        'Resting HR': resting_hr,
        'BP': f"{bp_systolic}/{bp_diastolic}",
        'EPO': epo_dose,
        'BPC-157': bpc_dose,
        'Notes': notes
    })
    st.success("Entry saved!")

# Show log table
st.header("📊 Daily Log")
if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No entries logged yet.")

# Red flag detector
st.header("🚨 Risk Flags")
flagged = []
for entry in st.session_state.log:
    if entry['Resting HR'] > 55:
        flagged.append(f"High resting HR on {entry['Date']}: {entry['Resting HR']} bpm")
    if int(entry['BP'].split("/")[0]) > 140:
        flagged.append(f"High systolic BP on {entry['Date']}: {entry['BP']}")
    if "headache" in entry['Notes'].lower() or "tingling" in entry['Notes'].lower():
        flagged.append(f"Symptom warning on {entry['Date']}: {entry['Notes']}")

if flagged:
    for item in flagged:
        st.error(item)
else:
    st.success("No critical risks detected.")

st.markdown("---")
st.caption("Built for Umar's endurance cycle — log daily and stay safe.")