# ===== Streamlit App Header =====
st.set_page_config(page_title="Employee Self Appraisal 2025", page_icon="📝", layout="wide")

# --- Custom CSS inspired by both design images ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f0f4ff 0%, #f9fbff 100%);
    }
    .main-title {
        font-size: 2.2em; font-weight: 700; color: #1e3a8a;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
        margin-bottom: -0.2em;
    }
    .section-title {
        font-size: 1.3em; font-weight: 600; color: #1e40af;
        margin-top: 1em; margin-bottom: 0.5em;
        border-left: 5px solid #2563eb; padding-left: 10px;
    }
    .divider {
        height: 2px; margin: 1.5em 0; border: none;
        background: linear-gradient(to right, #2563eb33, #60a5fa33);
    }
    .employee-summary {
        background: #ffffffcc; border-radius: 12px;
        padding: 1em 1.5em; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Banner ---
col1, col2 = st.columns([2, 3])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055646.png", width=100)
    st.markdown('<h1 class="main-title">Employee Self Appraisal 2025</h1>', unsafe_allow_html=True)
with col2:
    with st.container():
        st.markdown("#### Employee Information")
        with st.form("employee_info_form", clear_on_submit=False):
            name = st.text_input("Full Name")
            emp_id = st.text_input("Employee ID")
            department = st.selectbox("Department", ["Research", "Engineering", "Marketing", "Operations"])
            year = st.number_input("Appraisal Year", value=2025, step=1)
            submitted_info = st.form_submit_button("Confirm Info")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Compact employee summary display (from 2nd image) ---
if submitted_info:
    st.markdown(
        f"""
        <div class="employee-summary">
        <strong>Name:</strong> {name} &nbsp; | &nbsp;
        <strong>ID:</strong> {emp_id} &nbsp; | &nbsp;
        <strong>Department:</strong> {department} &nbsp; | &nbsp;
        <strong>Year:</strong> {int(year)}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# === Main Self Appraisal Form ===
with st.form("appraisal_form", clear_on_submit=False):
    st.markdown('<h3 class="section-title">Achievements</h3>', unsafe_allow_html=True)
    achievements = st.text_area("Describe your key achievements this year")

    st.markdown('<h3 class="section-title">Skills & Courses</h3>', unsafe_allow_html=True)
    num_courses = st.session_state.get("course_count", 3)
    for i in range(num_courses):
        c1, c2 = st.columns([4, 2])
        c1.text_input(f"Course #{i+1}", key=f"course_{i}")
        c2.text_input(f"Hours or Certification #{i+1}", key=f"hours_{i}")

    st.markdown('<h3 class="section-title">Awards & Recognitions</h3>', unsafe_allow_html=True)
    num_awards = st.session_state.get("award_count", 3)
    for i in range(num_awards):
        a1, a2 = st.columns([4, 2])
        a1.text_input(f"Award #{i+1}", key=f"award_{i}")
        a2.date_input(f"Date Received #{i+1}", key=f"award_date_{i}")

    st.markdown('<h3 class="section-title">Goals for Next Year</h3>', unsafe_allow_html=True)
    next_goals = st.text_area("List your goals or improvement plans for next year")

    st.markdown('<h3 class="section-title">Self-Rating</h3>', unsafe_allow_html=True)
    rating = st.slider("Rate your performance (1 = Poor, 10 = Excellent)", 1, 10, 7)

    # === Review Summary Panel ===
    with st.expander("🔍 Review Your Entries Before Submitting"):
        st.write("**Achievements:**", achievements)
        st.write("**Courses:**", [st.session_state[f"course_{i}"] for i in range(num_courses)])
        st.write("**Awards:**", [st.session_state[f"award_{i}"] for i in range(num_awards)])
        st.write("**Goals:**", next_goals)
        st.write("**Rating:**", rating)

    submit = st.form_submit_button("✅ Submit Appraisal")

# === Add buttons below sections ===
st.markdown("### Add More Entries")
c1, c2 = st.columns(2)
if c1.button("➕ Add Another Course"):
    st.session_state.course_count = st.session_state.get("course_count", 3) + 1
if c2.button("🏆 Add Another Award"):
    st.session_state.award_count = st.session_state.get("award_count", 3) + 1
