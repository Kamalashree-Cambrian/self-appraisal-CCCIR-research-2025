import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Employee Self Appraisal", page_icon="📝", layout="centered")

st.title("📝 Employee Self Appraisal Form")

# File to save local data
file_path = "self_appraisal_data.csv"

with st.form("faculty_form", clear_on_submit=False):
    st.subheader("👤 Basic Information")
    name = st.text_input("Full Name *")
    department = st.text_input("Department *")
    designation = st.text_input("Designation *")

    st.divider()

    st.subheader("📚 Academic and Research Activities (Optional)")
    patents = st.number_input("Number of Patents Filed", min_value=0, step=1)
    papers = st.number_input("Number of Research Papers Published", min_value=0, step=1)
    courses = st.number_input("Number of Courses/Workshops Attended", min_value=0, step=1)

    st.divider()

    st.subheader("🏆 Achievements (Optional)")
    awards = st.text_area("List any awards or recognitions", placeholder="Optional")
    contributions = st.text_area("Describe contributions to research/consultancy projects", placeholder="Optional")

    st.divider()

    st.subheader("💡 Goals for Next Year (Optional)")
    next_goals = st.text_area("What do you aim to achieve in the next year?", placeholder="Optional")

    submitted = st.form_submit_button("Submit")

if submitted:
    if not name or not department or not designation:
        st.error("⚠️ Please fill in all *required* fields (Name, Department, Designation).")
    else:
        data = {
            "Name": name,
            "Department": department,
            "Designation": designation,
            "Patents": patents or 0,
            "Papers": papers or 0,
            "Courses": courses or 0,
            "Awards": awards or "None",
            "Contributions": contributions or "None",
            "Next Year Goals": next_goals or "None",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.DataFrame([data])

        # Save locally
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            df = pd.concat([df_existing, df], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success("✅ Your self-appraisal has been successfully submitted!")
        st.dataframe(df.tail(1))
