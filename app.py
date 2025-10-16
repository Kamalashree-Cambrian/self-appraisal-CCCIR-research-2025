import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Employee Self-Appraisal", page_icon="🧾", layout="centered")

st.title("🧾 Employee Self-Appraisal Form")
st.write("Please fill out your self-appraisal details below:")

# Replace this with your deployed Apps Script web app URL
WEBHOOK_URL = "https://script.google.com/macros/s/PUT_YOUR_SCRIPT_ID/exec"

with st.form("self_appraisal"):
    st.header("Contribution")
    courses_conducted = st.number_input("Number of Courses Conducted", min_value=0)
    hours_taught = st.number_input("Number of Hours Taught", min_value=0)
    papers_published = st.number_input("Number of Papers Published", min_value=0)
    patents_granted = st.number_input("Number of Patents Granted", min_value=0)

    st.header("Significant Achievements")
    products_developed = st.text_area("Products Developed")
    support_for_companies = st.text_area("Support for Companies on Campus")
    courses_developed = st.text_area("Courses Developed")
    patents_awarded = st.text_area("Patents Awarded")

    st.header("Teaching & Research")
    teaching_courses = st.text_area("Courses Taught")
    proposals_submitted = st.text_area("Proposals Submitted")
    proposals_awarded = st.text_area("Proposals Awarded")

    submitted = st.form_submit_button("Submit")

if submitted:
    data = {
        "courses_conducted": courses_conducted,
        "hours_taught": hours_taught,
        "papers_published": papers_published,
        "patents_granted": patents_granted,
        "products_developed": products_developed,
        "support_for_companies": support_for_companies,
        "courses_developed": courses_developed,
        "patents_awarded": patents_awarded,
        "teaching_courses": teaching_courses,
        "proposals_submitted": proposals_submitted,
        "proposals_awarded": proposals_awarded,
        "timestamp": str(datetime.datetime.now()),
    }

    try:
        res = requests.post(WEBHOOK_URL, json=data)
        if res.status_code == 200:
            st.success("✅ Submitted successfully! Saved to Google Sheet.")
        else:
            st.warning("⚠️ Submission sent, but Google Script didn’t respond as expected.")
    except Exception as e:
        st.error(f"❌ Failed to submit: {e}")
