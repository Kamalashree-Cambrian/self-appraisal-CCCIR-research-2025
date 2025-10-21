import streamlit as st
import pandas as pd
from datetime import datetime
# import gspread
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
import os

# ----------------------------
# App Configuration
# ----------------------------
st.set_page_config(page_title="Employee Self Appraisal", page_icon="📝", layout="wide")

# ----------------------------
# Header & Intro
# ----------------------------
st.title("📝 Employee Self Appraisal Form")
st.markdown("Please fill in the details below. Fields marked with * are mandatory.")

# ----------------------------
# (Backend setup commented out)
# ----------------------------
"""
# GSHEET_ID = "YOUR_SHEET_ID"
# DRIVE_FOLDER_ID = "YOUR_FOLDER_ID"
# SCOPE = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
# ]
# CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
# gc = gspread.authorize(CREDS)
# sheet = gc.open_by_key(GSHEET_ID).sheet1
# drive_service = build("drive", "v3", credentials=CREDS)
"""

# ----------------------------
# Form UI
# ----------------------------
with st.form("faculty_form", clear_on_submit=False):

    # ----- Basic Info -----
    st.subheader("👤 Basic Information")
    name = st.text_input("Full Name *", placeholder="e.g. Dr. A. B. Sharma")
    department = st.text_input("Department *", placeholder="e.g. Electronics and Communication")
    designation = st.text_input("Designation *", placeholder="e.g. Associate Professor")

    # ----- Academic Activities -----
    st.divider()
    st.subheader("📚 Academic and Research Activities (Optional)")
    patents = st.number_input("Number of Patents Filed", min_value=0, step=1)
    papers = st.number_input("Number of Research Papers Published", min_value=0, step=1)
    courses = st.number_input("Number of Courses/Workshops Attended", min_value=0, step=1)

    st.text_area("Additional Research Contributions", placeholder="Describe any research or consultancy contributions...")

    # ----- Achievements -----
    st.divider()
    st.subheader("🏆 Achievements (Optional)")
    awards = st.text_area("List any awards or recognitions", placeholder="Optional")

    # ----- Goals -----
    st.divider()
    st.subheader("💡 Goals for Next Year (Optional)")
    next_goals = st.text_area("What do you aim to achieve next year?", placeholder="Optional")

    # Submit button
    submitted = st.form_submit_button("Submit")

# ----------------------------
# Post-submission behavior
# ----------------------------
if submitted:
    if not name or not department or not designation:
        st.error("⚠️ Please fill in all required fields (Name, Department, Designation).")
    else:
        st.success("✅ Thank you! Your form would be submitted successfully (demo mode).")
        
        # Show what data would be sent
        st.write("### 📋 Data Preview")
        df = pd.DataFrame([{
            "Name": name,
            "Department": department,
            "Designation": designation,
            "Patents": patents,
            "Papers": papers,
            "Courses": courses,
            "Awards": awards,
            "Next Year Goals": next_goals,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        st.dataframe(df)

        # Placeholder for the actual saving (commented out)
        """
        # sheet.append_row(data)
        # df.to_csv(csv_name, index=False)
        # drive_service.files().create(...)
        """

