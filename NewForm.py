import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO

st.set_page_config(page_title="Faculty Performance Form", page_icon="🎓", layout="wide")

# -----------------------------------
# Custom CSS
# -----------------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fc;
            font-family: 'Helvetica Neue', sans-serif;
            padding: 1rem 3rem;
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
st.write("Please fill in all relevant sections below. You can add multiple entries where applicable.")

# -----------------------------------
# Session state setup
# -----------------------------------
if "courses" not in st.session_state:
    st.session_state.courses = [{}]
if "patents" not in st.session_state:
    st.session_state.patents = [{}]
if "papers" not in st.session_state:
    st.session_state.papers = [{}]
if "certificates" not in st.session_state:
    st.session_state.certificates = [{}]
if "projects" not in st.session_state:
    st.session_state.projects = [{}]

# -----------------------------------
# FORM
# -----------------------------------
with st.form("faculty_form", clear_on_submit=False):

    st.subheader("👤 Basic Information")
    name = st.text_input("Full Name")
    designation = st.text_input("Designation")

    # --- Courses Conducted ---
    st.subheader("📘 Courses Conducted")
    for i, course in enumerate(st.session_state.courses):
        st.write(f"**Course {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.courses[i]["Title"] = st.text_input(f"Course Title {i+1}", key=f"course_title_{i}")
        with col2:
            st.session_state.courses[i]["Hours"] = st.number_input(f"Hours {i+1}", min_value=0, key=f"course_hours_{i}")
        with col3:
            st.session_state.courses[i]["Type"] = st.selectbox(f"Type {i+1}", ["Internal", "External", "Corporate"], key=f"course_type_{i}")

    if st.button("➕ Add Another Course"):
        st.session_state.courses.append({})

    # --- Patents ---
    st.subheader("🔬 Patents")
    for i, patent in enumerate(st.session_state.patents):
        st.write(f"**Patent {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.patents[i]["Status"] = st.selectbox(f"Patent Status {i+1}", ["Filed", "Granted"], key=f"patent_status_{i}")
        with col2:
            st.session_state.patents[i]["People"] = st.number_input(f"People Filed With {i+1}", min_value=1, key=f"patent_people_{i}")

    if st.button("➕ Add Another Patent"):
        st.session_state.patents.append({})

    # --- Papers Published ---
    st.subheader("📝 Papers Published / In Progress / Submitted")
    for i, paper in enumerate(st.session_state.papers):
        st.write(f"**Paper {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.papers[i]["Status"] = st.selectbox(f"Status {i+1}", ["Published", "In Progress", "Submitted"], key=f"paper_status_{i}")
        with col2:
            st.session_state.papers[i]["Worked_With"] = st.radio(f"Worked Alone or With Others? {i+1}", ["Alone", "With Others"], key=f"paper_with_{i}")
        with col3:
            st.session_state.papers[i]["Count"] = st.number_input(f"Number of Papers {i+1}", min_value=1, key=f"paper_count_{i}")

    if st.button("➕ Add Another Paper"):
        st.session_state.papers.append({})

    # --- Consultancy Projects ---
    st.subheader("💼 Consultancy Projects")
    for i, proj in enumerate(st.session_state.projects):
        st.write(f"**Project {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.projects[i]["Title"] = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
        with col2:
            st.session_state.projects[i]["Status"] = st.selectbox(f"Status {i+1}", ["Ongoing", "Complete"], key=f"proj_status_{i}")
        with col3:
            st.session_state.projects[i]["Worked_With"] = st.radio(f"Worked Alone or With Others? {i+1}", ["Alone", "With Others"], key=f"proj_with_{i}")

    if st.button("➕ Add Another Project"):
        st.session_state.projects.append({})

    # --- Awards and Certificates ---
    st.subheader("🏆 Awards and Certificates")
    for i, cert in enumerate(st.session_state.certificates):
        st.write(f"**Certificate {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.certificates[i]["Title"] = st.text_input(f"Award Title {i+1}", key=f"award_title_{i}")
        with col2:
            st.session_state.certificates[i]["Month"] = st.text_input(f"Month (e.g. March 2025) {i+1}", key=f"award_month_{i}")

    if st.button("➕ Add Another Certificate"):
        st.session_state.certificates.append({})

    submitted = st.form_submit_button("Submit ✨")

# -----------------------------------
# SUBMIT HANDLER
# -----------------------------------
if submitted:
    # Simple scoring logic
    total_score = 0
    for c in st.session_state.courses:
        if c.get("Type") == "Internal": total_score += 2
        elif c.get("Type") in ["External", "Corporate"]: total_score += 4
    for p in st.session_state.patents:
        total_score += 4 if p.get("People") == 1 else 2
    for p in st.session_state.papers:
        total_score += (4 if p.get("Worked_With") == "Alone" else 2)
    for p in st.session_state.projects:
        total_score += (4 if p.get("Worked_With") == "Alone" else 2)
    for a in st.session_state.certificates:
        total_score += 2 if a.get("Title") else 0

    st.success(f"✅ Thank you, **{name}**! Your total performance score is **{total_score} points.**")

    # Convert all data into DataFrame
    combined_data = {
        "Name": [name],
        "Designation": [designation],
        "Courses": [st.session_state.courses],
        "Patents": [st.session_state.patents],
        "Papers": [st.session_state.papers],
        "Projects": [st.session_state.projects],
        "Certificates": [st.session_state.certificates],
        "Total_Score": [total_score]
    }
    df = pd.DataFrame(combined_data)

    file_path = "faculty_responses.xlsx"
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(file_path, index=False)

    st.write("### 📄 Your Recorded Entry")
    st.dataframe(df)

    # Chart
    categories = ["Courses", "Patents", "Papers", "Projects", "Certificates"]
    scores = [
        len(st.session_state.courses),
        len(st.session_state.patents),
        len(st.session_state.papers),
        len(st.session_state.projects),
        len(st.session_state.certificates),
    ]
    fig, ax = plt.subplots()
    ax.barh(categories, scores)
    ax.set_xlabel("Count")
    ax.set_title("Entries by Category")
    st.pyplot(fig)

    # Download
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Download Your Record (Excel)",
        data=buffer.getvalue(),
        file_name=f"{name}_faculty_performance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
