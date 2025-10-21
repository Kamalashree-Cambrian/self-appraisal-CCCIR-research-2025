import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

st.set_page_config(page_title="Employee Self Appraisal", page_icon="📝", layout="centered")
st.title("📝 Employee Self Appraisal Form")

# --- Google Setup ---
GSHEET_ID = "PASTE_YOUR_SHEET_ID_HERE"
DRIVE_FOLDER_ID = "PASTE_YOUR_FOLDER_ID_HERE"

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
gc = gspread.authorize(CREDS)
sheet = gc.open_by_key(GSHEET_ID).sheet1
drive_service = build("drive", "v3", credentials=CREDS)

# --- Form ---
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
        data = [
            name,
            department,
            designation,
            patents,
            papers,
            courses,
            awards or "None",
            contributions or "None",
            next_goals or "None",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        # --- Append to Google Sheet ---
        sheet.append_row(data)

        # --- Create local CSV for backup ---
        df = pd.DataFrame([data], columns=[
            "Name", "Department", "Designation", "Patents", "Papers", "Courses",
            "Awards", "Contributions", "Next Year Goals", "Timestamp"
        ])
        csv_name = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(csv_name, index=False)

        # --- Upload to Google Drive folder ---
        file_metadata = {"name": csv_name, "parents": [DRIVE_FOLDER_ID]}
        media = MediaFileUpload(csv_name, mimetype="text/csv")
        drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        # --- Clean up local file ---
        os.remove(csv_name)

        st.success("✅ Your self-appraisal has been successfully submitted!")
