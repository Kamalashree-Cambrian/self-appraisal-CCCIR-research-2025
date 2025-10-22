# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from io import BytesIO

# # ---------------------------------------
# # PAGE CONFIGURATION
# # ---------------------------------------
# st.set_page_config(page_title="Faculty Performance Form", page_icon="🎓", layout="wide")

# # ---------------------------------------
# # CUSTOM STYLING
# # ---------------------------------------
# st.markdown("""
#     <style>
#         .main {
#             background-color: #f8f9fc;
#             font-family: 'Helvetica Neue', sans-serif;
#             padding: 1rem 3rem;
#         }
#         h1, h2, h3 {
#             color: #4a4a8a;
#         }
#         .stButton>button {
#             background-color: #4a4a8a;
#             color: white;
#             border-radius: 8px;
#             padding: 0.6em 1.2em;
#         }
#         .stButton>button:hover {
#             background-color: #5d5dbb;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ---------------------------------------
# # PAGE TITLE
# # ---------------------------------------
# st.title("🎓 Faculty Performance Submission Form")
# st.write("Please fill in all relevant sections below. You can skip any part that does not apply to you.")

# # ---------------------------------------
# # SESSION STATE SETUP
# # ---------------------------------------
# for key in ["courses", "patents", "papers", "projects", "certificates"]:
#     if key not in st.session_state:
#         st.session_state[key] = []

# # ---------------------------------------
# # ADD BUTTONS
# # ---------------------------------------
# st.write("### ➕ Add More Entries (Optional)")
# colA, colB, colC, colD, colE = st.columns(5)
# with colA:
#     if st.button("Add Course"):
#         st.session_state.courses.append({})
# with colB:
#     if st.button("Add Patent"):
#         st.session_state.patents.append({})
# with colC:
#     if st.button("Add Paper"):
#         st.session_state.papers.append({})
# with colD:
#     if st.button("Add Project"):
#         st.session_state.projects.append({})
# with colE:
#     if st.button("Add Certificate"):
#         st.session_state.certificates.append({})

# st.write("---")

# # ---------------------------------------
# # FORM
# # ---------------------------------------
# with st.form("faculty_form", clear_on_submit=False):

#     st.subheader("👤 Basic Information")
#     name = st.text_input("Full Name *")
#     designation = st.text_input("Designation *")

#     # --- COURSES ---
#     st.subheader("📘 Courses Conducted (Optional)")
#     if not st.session_state.courses:
#         st.info("No courses added. Click 'Add Course' above if applicable.")
#     for i, course in enumerate(st.session_state.courses):
#         st.write(f"**Course {i+1}**")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.session_state.courses[i]["Title"] = st.text_input(f"Course Title {i+1}", key=f"course_title_{i}")
#         with col2:
#             st.session_state.courses[i]["Hours"] = st.number_input(f"Hours {i+1}", min_value=0, key=f"course_hours_{i}")
#         with col3:
#             st.session_state.courses[i]["Type"] = st.selectbox(
#                 f"Type {i+1}", ["None", "Internal", "External", "Corporate"], key=f"course_type_{i}"
#             )

#     # --- PATENTS ---
#     st.subheader("🔬 Patents (Optional)")
#     if not st.session_state.patents:
#         st.info("No patents added. Click 'Add Patent' above if applicable.")
#     for i, patent in enumerate(st.session_state.patents):
#         st.write(f"**Patent {i+1}**")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.session_state.patents[i]["Status"] = st.selectbox(
#                 f"Patent Status {i+1}", ["None", "Filed", "Granted"], key=f"patent_status_{i}"
#             )
#         with col2:
#             st.session_state.patents[i]["People"] = st.number_input(
#                 f"People Filed With {i+1}", min_value=0, key=f"patent_people_{i}"
#             )

#     # --- PAPERS ---
#     st.subheader("📝 Papers (Optional)")
#     if not st.session_state.papers:
#         st.info("No papers added. Click 'Add Paper' above if applicable.")
#     for i, paper in enumerate(st.session_state.papers):
#         st.write(f"**Paper {i+1}**")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.session_state.papers[i]["Status"] = st.selectbox(
#                 f"Status {i+1}", ["None", "Published", "In Progress", "Submitted"], key=f"paper_status_{i}"
#             )
#         with col2:
#             st.session_state.papers[i]["Worked_With"] = st.radio(
#                 f"Worked Alone or With Others? {i+1}", ["None", "Alone", "With Others"], key=f"paper_with_{i}"
#             )
#         with col3:
#             st.session_state.papers[i]["Count"] = st.number_input(
#                 f"Number of Papers {i+1}", min_value=0, key=f"paper_count_{i}"
#             )

#     # --- PROJECTS ---
#     st.subheader("💼 Consultancy Projects (Optional)")
#     if not st.session_state.projects:
#         st.info("No projects added. Click 'Add Project' above if applicable.")
#     for i, proj in enumerate(st.session_state.projects):
#         st.write(f"**Project {i+1}**")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.session_state.projects[i]["Title"] = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
#         with col2:
#             st.session_state.projects[i]["Status"] = st.selectbox(
#                 f"Status {i+1}", ["None", "Ongoing", "Complete"], key=f"proj_status_{i}"
#             )
#         with col3:
#             st.session_state.projects[i]["Worked_With"] = st.radio(
#                 f"Worked Alone or With Others? {i+1}", ["None", "Alone", "With Others"], key=f"proj_with_{i}"
#             )

#     # --- CERTIFICATES ---
#     st.subheader("🏆 Awards and Certificates (Optional)")
#     if not st.session_state.certificates:
#         st.info("No awards/certificates added. Click 'Add Certificate' above if applicable.")
#     for i, cert in enumerate(st.session_state.certificates):
#         st.write(f"**Certificate {i+1}**")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.session_state.certificates[i]["Title"] = st.text_input(f"Award Title {i+1}", key=f"award_title_{i}")
#         with col2:
#             st.session_state.certificates[i]["Month"] = st.text_input(f"Month (e.g. March 2025) {i+1}", key=f"award_month_{i}")

#     submitted = st.form_submit_button("Submit ✨")

# # ---------------------------------------
# # SUBMIT HANDLER
# # ---------------------------------------
# if submitted:
#     if not name or not designation:
#         st.error("⚠️ Please fill in the *required* fields (Name and Designation).")
#     else:
#         total_score = 0
#         for c in st.session_state.courses:
#             if c.get("Type") == "Internal":
#                 total_score += 2
#             elif c.get("Type") in ["External", "Corporate"]:
#                 total_score += 4
#         for p in st.session_state.patents:
#             if p.get("Status") != "None":
#                 total_score += 4 if p.get("People") == 1 else 2
#         for p in st.session_state.papers:
#             if p.get("Status") != "None":
#                 total_score += 4 if p.get("Worked_With") == "Alone" else 2
#         for p in st.session_state.projects:
#             if p.get("Status") != "None":
#                 total_score += 4 if p.get("Worked_With") == "Alone" else 2
#         for a in st.session_state.certificates:
#             total_score += 2 if a.get("Title") else 0

#         st.success(f"✅ Thank you, **{name}**! Your total performance score is **{total_score} points.**")

#         combined_data = {
#             "Name": [name],
#             "Designation": [designation],
#             "Courses": [st.session_state.courses or None],
#             "Patents": [st.session_state.patents or None],
#             "Papers": [st.session_state.papers or None],
#             "Projects": [st.session_state.projects or None],
#             "Certificates": [st.session_state.certificates or None],
#             "Total_Score": [total_score],
#         }
#         df = pd.DataFrame(combined_data)

#         file_path = "faculty_responses.xlsx"
#         if os.path.exists(file_path):
#             existing_df = pd.read_excel(file_path)
#             df = pd.concat([existing_df, df], ignore_index=True)
#         df.to_excel(file_path, index=False)

#         st.write("### 📄 Your Recorded Entry")
#         st.dataframe(df.tail(1))

#         categories = ["Courses", "Patents", "Papers", "Projects", "Certificates"]
#         scores = [
#             len(st.session_state.courses),
#             len(st.session_state.patents),
#             len(st.session_state.papers),
#             len(st.session_state.projects),
#             len(st.session_state.certificates),
#         ]
#         fig, ax = plt.subplots()
#         ax.barh(categories, scores)
#         ax.set_xlabel("Count")
#         ax.set_title("Entries by Category")
#         st.pyplot(fig)

#         buffer = BytesIO()
#         df.to_excel(buffer, index=False)
#         st.download_button(
#             label="📥 Download Your Record (Excel)",
#             data=buffer.getvalue(),
#             file_name=f"{name}_faculty_performance.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from io import BytesIO
# from datetime import datetime

# # ---------------------------------------
# # PAGE CONFIG
# # ---------------------------------------
# st.set_page_config(page_title="Faculty Performance Form",
#                    page_icon="🎓",
#                    layout="wide",
#                    initial_sidebar_state="collapsed")

# # ---------------------------------------
# # STYLES + LAYOUT
# # ---------------------------------------
# st.markdown(
#     """
#     <style>
#     /* Page background and font */
#     .reportview-container .main {
#         background-color: #f6f7fb;
#         font-family: Inter, 'Helvetica Neue', Arial, sans-serif;
#     }
#     /* Card wrapper */
#     .card {
#         background: #ffffff;
#         border-radius: 12px;
#         padding: 18px;
#         box-shadow: 0 6px 18px rgba(41, 56, 88, 0.06);
#         margin-bottom: 16px;
#     }
#     .section-title {
#         color: #2f3562;
#         font-weight: 600;
#         margin-bottom: 8px;
#     }
#     .small-muted {
#         color: #7a7f9a;
#         font-size: 13px;
#     }
#     /* Buttons */
#     .stButton>button {
#         background-color: #3f46a1;
#         color: white;
#         border-radius: 8px;
#         padding: 0.55rem 1rem;
#     }
#     .stButton>button:hover {
#         background-color: #5059c9;
#     }
#     /* Logo sizing */
#     .logo {
#         height: 56px;
#         object-fit: contain;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ---------------------------------------
# # HEADER with optional logo
# # ---------------------------------------
# col_logo, col_title = st.columns([1, 8], gap="small")
# with col_logo:
#     # Option 1: load a local logo file (logo.png)
#     if os.path.exists("logo.png"):
#         st.image("logo.png", use_column_width=False, width=220, clamp=True)
#     else:
#         # Option 2: allow upload in UI (not persisted across sessions)
#         uploaded_logo = st.file_uploader("Upload logo (optional)", type=["png", "jpg", "jpeg"], key="logo_upload")
#         if uploaded_logo:
#             st.image(uploaded_logo, use_column_width=False, width=220)

# with col_title:
#     st.markdown("<h1 style='margin:0; color:#2f3562;'>🎓 Faculty Performance Submission Form</h1>", unsafe_allow_html=True)
#     st.markdown("<div class='small-muted'>Fill optional fields only if applicable. You can add multiple entries for courses/papers/etc.</div>", unsafe_allow_html=True)

# st.write("")  # spacer

# # ---------------------------------------
# # session state lists (optional entries)
# # ---------------------------------------
# for key in ["courses", "patents", "papers", "projects", "certificates"]:
#     if key not in st.session_state:
#         st.session_state[key] = []

# # Add buttons (outside form)
# st.markdown("<div class='card'><div style='display:flex; gap:8px; align-items:center'><strong>Add Entries (optional)</strong></div></div>", unsafe_allow_html=True)
# colA, colB, colC, colD, colE = st.columns(5)
# with colA:
#     if st.button("Add Course"):
#         st.session_state.courses.append({})
# with colB:
#     if st.button("Add Patent"):
#         st.session_state.patents.append({})
# with colC:
#     if st.button("Add Paper"):
#         st.session_state.papers.append({})
# with colD:
#     if st.button("Add Project"):
#         st.session_state.projects.append({})
# with colE:
#     if st.button("Add Certificate"):
#         st.session_state.certificates.append({})

# st.write("---")

# # ---------------------------------------
# # FORM (main)
# # ---------------------------------------
# with st.form("faculty_form", clear_on_submit=False):

#     # Basic information card
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>👤 Basic Information</div>", unsafe_allow_html=True)
#     name = st.text_input("Full Name *", placeholder="e.g. Dr. Anil Kumar")
#     designation = st.text_input("Designation *", placeholder="e.g. Associate Professor")
#     st.markdown("</div>", unsafe_allow_html=True)

#     # Courses card
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>📘 Courses Conducted (Optional)</div>", unsafe_allow_html=True)
#     if not st.session_state.courses:
#         st.info("No courses added. Click 'Add Course' above to add entries.")
#     for i, course in enumerate(st.session_state.courses):
#         st.write(f"**Course {i+1}**")
#         c1, c2, c3 = st.columns([4,2,2])
#         with c1:
#             st.session_state.courses[i]["Title"] = st.text_input(f"Course Title {i+1}", key=f"course_title_{i}")
#         with c2:
#             st.session_state.courses[i]["Hours"] = st.number_input(f"Hours {i+1}", min_value=0, key=f"course_hours_{i}")
#         with c3:
#             st.session_state.courses[i]["Type"] = st.selectbox(f"Type {i+1}", ["None","Internal","External","Corporate"], key=f"course_type_{i}")
#     st.markdown("</div>", unsafe_allow_html=True)

#     # Patents card
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>🔬 Patents (Optional)</div>", unsafe_allow_html=True)
#     if not st.session_state.patents:
#         st.info("No patents added. Click 'Add Patent' above to add entries.")
#     for i, patent in enumerate(st.session_state.patents):
#         st.write(f"**Patent {i+1}**")
#         p1, p2 = st.columns(2)
#         with p1:
#             st.session_state.patents[i]["Status"] = st.selectbox(f"Patent Status {i+1}", ["None","Filed","Granted"], key=f"patent_status_{i}")
#         with p2:
#             st.session_state.patents[i]["People"] = st.number_input(f"People Filed With {i+1}", min_value=0, key=f"patent_people_{i}")
#     st.markdown("</div>", unsafe_allow_html=True)

#     # Papers card
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>📝 Papers (Optional)</div>", unsafe_allow_html=True)
#     if not st.session_state.papers:
#         st.info("No papers added. Click 'Add Paper' above to add entries.")
#     for i, paper in enumerate(st.session_state.papers):
#         st.write(f"**Paper {i+1}**")
#         q1, q2, q3 = st.columns(3)
#         with q1:
#             st.session_state.papers[i]["Status"] = st.selectbox(f"Status {i+1}", ["None","Published","In Progress","Submitted"], key=f"paper_status_{i}")
#         with q2:
#             st.session_state.papers[i]["Worked_With"] = st.radio(f"Worked Alone or With Others? {i+1}", ["None","Alone","With Others"], key=f"paper_with_{i}")
#         with q3:
#             st.session_state.papers[i]["Count"] = st.number_input(f"Count {i+1}", min_value=0, key=f"paper_count_{i}")
#     st.markdown("</div>", unsafe_allow_html=True)

#     # Projects card
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>💼 Consultancy Projects (Optional)</div>", unsafe_allow_html=True)
#     if not st.session_state.projects:
#         st.info("No projects added. Click 'Add Project' above to add entries.")
#     for i, proj in enumerate(st.session_state.projects):
#         r1, r2, r3 = st.columns(3)
#         with r1:
#             st.session_state.projects[i]["Title"] = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
#         with r2:
#             st.session_state.projects[i]["Status"] = st.selectbox(f"Status {i+1}", ["None","Ongoing","Complete"], key=f"proj_status_{i}")
#         with r3:
#             st.session_state.projects[i]["Worked_With"] = st.radio(f"Worked Alone or With Others? {i+1}", ["None","Alone","With Others"], key=f"proj_with_{i}")
#     st.markdown("</div>", unsafe_allow_html=True)

#     # Certificates card
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>🏆 Awards & Certificates (Optional)</div>", unsafe_allow_html=True)
#     if not st.session_state.certificates:
#         st.info("No awards added. Click 'Add Certificate' above to add entries.")
#     for i, cert in enumerate(st.session_state.certificates):
#         s1, s2 = st.columns(2)
#         with s1:
#             st.session_state.certificates[i]["Title"] = st.text_input(f"Award Title {i+1}", key=f"award_title_{i}")
#         with s2:
#             st.session_state.certificates[i]["Month"] = st.text_input(f"Month (e.g. March 2025) {i+1}", key=f"award_month_{i}")
#     st.markdown("</div>", unsafe_allow_html=True)

#     # submit
#     submitted = st.form_submit_button("Submit ✨")

# # ---------------------------------------
# # SUBMIT HANDLER (unchanged logic, safe defaults)
# # ---------------------------------------
# if submitted:
#     if not name or not designation:
#         st.error("⚠️ Please fill in the required fields (Name and Designation).")
#     else:
#         # scoring (same as before but robust for optional None)
#         total_score = 0
#         for c in st.session_state.courses:
#             if c.get("Type") == "Internal":
#                 total_score += 2
#             elif c.get("Type") in ["External", "Corporate"]:
#                 total_score += 4
#         for p in st.session_state.patents:
#             if p.get("Status") and p.get("Status") != "None":
#                 total_score += 4 if p.get("People") == 1 else 2
#         for p in st.session_state.papers:
#             if p.get("Status") and p.get("Status") != "None":
#                 total_score += 4 if p.get("Worked_With") == "Alone" else 2
#         for p in st.session_state.projects:
#             if p.get("Status") and p.get("Status") != "None":
#                 total_score += 4 if p.get("Worked_With") == "Alone" else 2
#         for a in st.session_state.certificates:
#             total_score += 2 if a.get("Title") else 0

#         st.success(f"✅ Thank you, **{name}**! Your total performance score: **{total_score}**")

#         # prepare data
#         combined_data = {
#             "Name": [name],
#             "Designation": [designation],
#             "Courses": [st.session_state.courses or None],
#             "Patents": [st.session_state.patents or None],
#             "Papers": [st.session_state.papers or None],
#             "Projects": [st.session_state.projects or None],
#             "Certificates": [st.session_state.certificates or None],
#             "Total_Score": [total_score],
#             "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
#         }
#         df = pd.DataFrame(combined_data)

#         # Local save (keeps original behavior)
#         file_path = "faculty_responses.xlsx"
#         try:
#             if os.path.exists(file_path):
#                 existing_df = pd.read_excel(file_path)
#                 df = pd.concat([existing_df, df], ignore_index=True)
#             df.to_excel(file_path, index=False)
#         except Exception as e:
#             st.warning("Couldn't save to local Excel (maybe missing dependency).")

#         # show last entry + plot
#         st.write("### 📄 Recorded Entry (preview)")
#         st.dataframe(df.tail(1))

#         categories = ["Courses","Patents","Papers","Projects","Certificates"]
#         scores = [len(st.session_state.courses), len(st.session_state.patents), len(st.session_state.papers), len(st.session_state.projects), len(st.session_state.certificates)]
#         fig, ax = plt.subplots()
#         ax.barh(categories, scores)
#         ax.set_xlabel("Count")
#         ax.set_title("Entries by Category")
#         st.pyplot(fig)

#         # download button
#         buffer = BytesIO()
#         df.to_excel(buffer, index=False)
#         st.download_button(
#             label="📥 Download Record (Excel)",
#             data=buffer.getvalue(),
#             file_name=f"{name.replace(' ','_')}_faculty_performance.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )





import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Employee Self Appraisal", page_icon="📝", layout="centered")

# Display logo safely (local or hosted)
try:
    st.image("CCCIR Logo.png", use_container_width=True)
except Exception:
    st.info("Logo not found — please ensure 'CCCIR Logo.png' is in the app folder.")

st.title("📝 Employee Self Appraisal Form")

# ---------------- GOOGLE SHEETS SETUP ----------------
SHEET_ID = "1HBYGDHOb2qVZ9rrZz-74rzw7UY_7SotnwmL8EakwcfI"  # paste only the ID part from the sheet link
SHEET_NAME = "Sheet1"             # or change to your sheet tab name

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# ---------------- FORM ----------------
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

# ---------------- DATA HANDLING ----------------
if submitted:
    if not name or not department or not designation:
        st.error("⚠️ Please fill in all *required* fields (Name, Department, Designation).")
    else:
        data_row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            department,
            designation,
            patents,
            papers,
            courses,
            awards if awards else "None",
            contributions if contributions else "None",
            next_goals if next_goals else "None"
        ]

        # Append to Google Sheet
        sheet.append_row(data_row)

        st.success("✅ Your self-appraisal has been successfully submitted!")
        st.balloons()
