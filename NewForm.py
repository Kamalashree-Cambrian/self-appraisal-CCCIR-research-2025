# --- Inside the form ---
with st.form("faculty_form", clear_on_submit=False):
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

    # remove st.button() from inside form
    submitted = st.form_submit_button("Submit ✨")

# --- Outside the form ---
st.write("---")
colA, colB, colC, colD, colE = st.columns(5)
with colA:
    if st.button("➕ Add Course"):
        st.session_state.courses.append({})
with colB:
    if st.button("➕ Add Patent"):
        st.session_state.patents.append({})
with colC:
    if st.button("➕ Add Paper"):
        st.session_state.papers.append({})
with colD:
    if st.button("➕ Add Project"):
        st.session_state.projects.append({})
with colE:
    if st.button("➕ Add Certificate"):
        st.session_state.certificates.append({})
