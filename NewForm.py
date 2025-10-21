import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Employee Self Appraisal", page_icon="📝", layout="centered")

st.title("📝 Employee Self Appraisal Form")

# --- Google Sheet setup ---
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(CREDS)
SHEET = client.open("Self Appraisal Data").sheet1  # change sheet name if needed

# --- Form starts here ---
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
    awards = st.text_area("List any awards or recognitions (if none, leave blank)", placeholder="Optional")
    contributions = st.text_area("Describe contributions to research/consultancy projects", placeholder="Optional")

    st.divider()

    st.subheader("💡 Goals for Next Year (Optional)")
    next_goals = st.text_area("What do you aim to achieve in the next year?", placeholder="Optional")

    submitted = st.form_submit_button("Submit")

# --- Form submission handling ---
if submitted:
    if not name or not department or not designation:
        st.error("⚠️ Please fill in all *required* fields (Name, Department, Designation).")
    else:
        # Handle optional fields by converting empty ones to 0 or 'None'
        data = [
            name,
            department,
            designation,
            patents if patents else 0,
            papers if papers else 0,
            courses if courses else 0,
            awards if awards else "None",
            contributions if contributions else "None",
            next_goals if next_goals else "None",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ]

        SHEET.append_row(data)
        st.success("✅ Your self-appraisal has been successfully submitted!")

        # Optional: show summary
        with st.expander("📋 Submitted Data Preview"):
            st.write({
                "Name": name,
                "Department": department,
                "Designation": designation,
                "Patents": patents,
                "Papers": papers,
                "Courses": courses,
                "Awards": awards or "None",
                "Contributions": contributions or "None",
                "Next Year Goals": next_goals or "None",
            })
