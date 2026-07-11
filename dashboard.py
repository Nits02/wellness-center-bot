"""Streamlit Admin Dashboard for Wellness Center POC."""

import pandas as pd
import streamlit as st

from supabase_client import get_supabase_client

st.set_page_config(page_title="Wellness Center Admin", layout="wide")
st.title("Wellness Center – Admin Dashboard")

# Manual refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

supabase = get_supabase_client()

# ─── Section 1: Upcoming Appointments ────────────────────────────────────────
st.header("📅 Upcoming Appointments")

appointments_result = (
    supabase.table("appointments")
    .select("id, user_id, service_type, appointment_time, status")
    .order("appointment_time", desc=False)
    .execute()
)

if appointments_result.data:
    df_appointments = pd.DataFrame(appointments_result.data)
    df_appointments["appointment_time"] = pd.to_datetime(df_appointments["appointment_time"])
    st.dataframe(df_appointments, use_container_width=True)
else:
    st.info("No appointments found.")

# ─── Section 2: Real-Time Occupancy Timeline ─────────────────────────────────
st.header("📊 Occupancy Timeline (Last 50 Records)")

occupancy_result = (
    supabase.table("occupancy")
    .select("timestamp, current_count")
    .order("timestamp", desc=True)
    .limit(50)
    .execute()
)

if occupancy_result.data:
    df_occupancy = pd.DataFrame(occupancy_result.data)
    df_occupancy["timestamp"] = pd.to_datetime(df_occupancy["timestamp"])
    df_occupancy = df_occupancy.sort_values("timestamp")
    df_occupancy = df_occupancy.set_index("timestamp")
    st.line_chart(df_occupancy["current_count"])
else:
    st.info("No occupancy data available.")
