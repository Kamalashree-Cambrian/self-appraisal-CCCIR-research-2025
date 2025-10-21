import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO

try:
    import streamlit
    import pandas
    import matplotlib
    import openpyxl
except ImportError:
    import os
    os.system('pip install -r requirements.txt')
# -------------------------------
# App configuration
# -------------------------------
st.set_page_config(page_title="Faculty Performance Form", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
        .main {
            background-color: #f8f9fc;
            font-family: 'Helvetica Neue', sans-serif;
        }
        h1, h2, h3 {
            color: #4a4a8a;
        }
        .stButton>button {
            background-color: #4a4a8a;
            color: white;
            border-radius: 8px;
            padding: 0.6em 1.2em;
        }
        .stButton>button:hover {
            background-color: #5d5dbb;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Faculty Performance Submission Form")
st.write("Please fill in all relevant sections below. A final score and graph will be shown after submission.")

# -------------------------------
# FORM START
# -------------------------------
with st.form("faculty_form", clear_on_submit=True):

    st.subheader("👤 Basic Information")
    name = st.text_input("Full Name")
    designation = st.text_input("Designation")

    # --- Courses Conducted ---
    st.subheader("📘 Courses Conducted")
    course_title = st.text_input("Course Title")
    course_hours = st.number_input("Number of Hours Taught", min_value=0)
    course_type = st.selectbox("Type", ["Internal", "External", "Corporate"])
    course_points = 2 if course_type == "Internal" else 4

    # --- Patents ---
    st.subheader("🔬 Patents")
    patent_status = st.selectbox("Status", ["Filed", "Granted"])
    patent_people = st.number_input("Number of People Filed With", min_value=1)
    patent_points = 4 if patent_people == 1 else 2

    # --- Papers Published ---
    st.subheader("📝 Papers Published")
    papers_published = st.number_input("Number of Papers Published", min_value=0)
    published_alone = st.radio("Worked alone or with others?", ["Alone", "With Others"])
    published_points = 4 if published_alone == "Alone" else 2

    # --- Papers in Progress ---
    st.subheader("⏳ Papers in Progress")
    papers_progress = st.number_input("Number of Papers in Progress", min_value=0)
    progress_alone = st.radio("Worked alone or with others?", ["Alone", "With Others"], key="progress")
    progress_points = 4 if progress_alone == "Alone" else 2

    # --- Papers Submitted ---
    st.subheader("📤 Papers Submitted")
    papers_submitted = st.number_input("Number of Papers Submitted", min_value=0)
    submitted_alone = st.radio("Worked alone or with others?", ["Alone", "With Others"], key="submitted")
    submitted_points = 4 if submitted_alone == "Alone" else 2

    # --- Consultancy Projects ---
    st.subheader("💼 Consultancy Projects")
    project_title = st.text_input("Project Title")
    project_status = st.selectbox("Project Status", ["Ongoing", "Complete"])
    project_team = st.radio("Worked alone or with others?", ["Alone", "With Others"], key="consult")
    project_points = 4 if project_team == "Alone" else 2

    # --- Awards and Certificates ---
    st.subheader("🏆 Awards and Certificates")
    award_title = st.text_input("Award/Certificate Title")
    award_month = st.text_input("Month Collected (e.g. March 2025)")
    award_points = 2 if award_title else 0

    # --- UG Courses ---
    st.subheader("🎓 UG Courses Taught")
    ug_course = st.text_input("UG Course Title")
    ug_hours = st.number_input("UG Hours Taught", min_value=0)

    # --- PG Courses ---
    st.subheader("🎓 PG Courses Taught")
    pg_course = st.text_input("PG Course Title")
    pg_hours = st.number_input("PG Hours Taught", min_value=0)

    # --- Submit ---
    submitted = st.form_submit_button("Submit ✨")

# -------------------------------
# ON SUBMIT
# -------------------------------
if submitted:
    # --- Calculate Total Points ---
    total_score = (
        course_points
        + patent_points
        + published_points
        + progress_points
        + submitted_points
        + project_points
        + award_points
    )

    st.success(f"✅ Thank you, **{name}**! Your performance score is **{total_score} points.**")

    # --- Prepare data for saving ---
    data = {
        "Name": [name],
        "Designation": [designation],
        "Course_Title": [course_title],
        "Course_Hours": [course_hours],
        "Course_Type": [course_type],
        "Course_Points": [course_points],
        "Patent_Status": [patent_status],
        "Patent_People": [patent_people],
        "Patent_Points": [patent_points],
        "Papers_Published": [papers_published],
        "Published_Points": [published_points],
        "Papers_Progress": [papers_progress],
        "Progress_Points": [progress_points],
        "Papers_Submitted": [papers_submitted],
        "Submitted_Points": [submitted_points],
        "Consultancy_Title": [project_title],
        "Consultancy_Status": [project_status],
        "Consultancy_Points": [project_points],
        "Award_Title": [award_title],
        "Award_Month": [award_month],
        "Award_Points": [award_points],
        "UG_Course": [ug_course],
        "UG_Hours": [ug_hours],
        "PG_Course": [pg_course],
        "PG_Hours": [pg_hours],
        "Total_Score": [total_score],
    }

    df = pd.DataFrame(data)

    # --- Save to Excel ---
    file_path = "faculty_responses.xlsx"
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_excel(file_path, index=False)

    # --- Show DataFrame ---
    st.write("### 📄 Your Recorded Entry")
    st.dataframe(df)

    # --- Graph of Points ---
    st.write("### 📊 Your Performance Breakdown")
    categories = [
        "Courses",
        "Patents",
        "Published",
        "Progress",
        "Submitted",
        "Projects",
        "Awards",
    ]
    scores = [
        course_points,
        patent_points,
        published_points,
        progress_points,
        submitted_points,
        project_points,
        award_points,
    ]

    fig, ax = plt.subplots()
    ax.barh(categories, scores)
    ax.set_xlabel("Points")
    ax.set_title("Performance Breakdown by Category")
    st.pyplot(fig)

    # --- Download Option ---
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Download Your Record (Excel)",
        data=buffer.getvalue(),
        file_name=f"{name}_faculty_performance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
