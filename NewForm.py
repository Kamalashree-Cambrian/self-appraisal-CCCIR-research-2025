import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ----------------------------
# App Configuration
# ----------------------------
st.set_page_config(page_title="Employee Self Appraisal", page_icon="📝", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #4a4a8a;
            text-align: center;
        }
        .stForm {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Page Header
# ----------------------------
st.title("📝 Employee Self Appraisal Form")
st.write("Please fill in the details below. Fields marked with * are mandatory.")

# ----------------------------
# File path (commented out)
# ----------------------------
# file_path = "self_appraisal_data.csv"

# ----------------------------
# Form Layout
# ----------------------------
with st.form("faculty_form", clear_on_submit=False):
    st.subheader("👤 Basic Information")
    name = st.text_input("Full Name *", placeholder="e.g. Dr. A. B. Sharma")
    department = st.text_input("Department *", placeholder="e.g. Electronics and Communication Engineering")
    designation = st.text_input("Designation *", placeholder="e.g. Associate Professor")

    st.divider()

    st.subheader("📚 Academic and Research Activities (Optional)")
    patents = st.number_input("Number of Patents Filed", min_value=0, step=1)
    papers = st.number_input("Number of Research Papers Published", min_value=0, step=1)
    courses = st.number_input("Number of Courses/Workshops Attended", min_value=0, step=1)

    st.text_area("Additional Research Notes", placeholder="Describe other academic or research work if any...")

    st.divider()

    st.subheader("🏆 Achievements (Optional)")
    awards = st.text_area("List any awards or recognitions", placeholder="Optional")
    contributions = st.text_area("Describe contributions to research/consultancy projects", placeholder="Optional")

    st.divider()

    st.subheader("💡 Goals for Next Year (Optional)")
    next_goals = st.text_area("What do you aim to achieve next year?", placeholder="Optional")

    submitted = st.form_submit_button("Submit")

# ----------------------------
# Submission Behavior (Preview)
# ----------------------------
if submitted:
    if not name or not department or not designation:
        st.error("⚠️ Please fill in all *required* fields (Name, Department, Designation).")
    else:
        st.success("✅ Thank you! (Preview mode only — data not saved).")

        # Prepare preview DataFrame
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
        
        # Show preview of what would be saved
        st.write("### 📋 Form Data Preview")
        st.dataframe(df)

        # (Commented-out save logic)
        """
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            df = pd.concat([df_existing, df], ignore_index=True)
        df.to_csv(file_path, index=False)
        """

