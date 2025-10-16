# app.py
import streamlit as st
import pandas as pd
import json
import datetime
import uuid
from pathlib import Path

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GS_AVAILABLE = True
except Exception:
    GS_AVAILABLE = False

# --- Helper functions ---
def local_save(submission: dict, folder='submissions'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = Path(folder) / f"submission_{submission['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(submission, f, ensure_ascii=False, indent=2, default=str)
    return str(filename)

def flatten_submission(sub: dict) -> dict:
    flat = {}
    flat['id'] = sub.get('id')
    flat['timestamp'] = sub.get('timestamp')
    flat['employee_name'] = sub.get('employee_name')
    flat['employee_email'] = sub.get('employee_email')
    flat['department'] = sub.get('department')
    flat['role'] = sub.get('role')
    for k in ['contributions', 'achievements', 'teaching', 'research', 'others']:
        flat[k] = sub.get(k, {})
    flat['self_rating_overall'] = sub.get('self_rating_overall')
    flat['comments'] = sub.get('comments')
    return flat

def append_to_gsheet(submission: dict):
    if not GS_AVAILABLE:
        raise RuntimeError("gspread/google-auth not installed")

    service_account_info = st.secrets.get('gcp_service_account')
    sheet_id = st.secrets.get('GOOGLE_SHEET_ID')

    if not service_account_info or not sheet_id:
        raise RuntimeError('Missing Google Sheets credentials in st.secrets')

    creds = Credentials.from_service_account_info(service_account_info, scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])
    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_id)

    year = datetime.datetime.now().year
    dept = submission.get('department', 'General').strip().title() or 'General'
    worksheet_name = f"{year}_{dept}"

    try:
        ws = sh.worksheet(worksheet_name)
    except Exception:
        ws = sh.add_worksheet(title=worksheet_name, rows=1000, cols=30)

    flat = flatten_submission(submission)
    if ws.row_count == 0 or ws.get_all_values() == []:
        ws.append_row(list(flat.keys()))
    ws.append_row([json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v) for v in flat.values()])
    return True

# --- Page setup ---
st.set_page_config(page_title='Self Appraisal — SmartForm+', layout='wide', page_icon='📝')

st.markdown("""
<style>
.card {background:linear-gradient(90deg,#ffffffcc,#f1f7ff);padding:18px;border-radius:16px;box-shadow:0 6px 18px rgba(22,61,105,0.1);}
.brand{font-size:30px;font-weight:700;color:#124265}
.subtitle{color:#475569;font-size:15px;margin-top:-8px}
.section-title{font-weight:600;font-size:18px;margin-top:12px}
.small-muted{color:#6b7280;font-size:13px}
</style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([2, 3])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=120)
with col2:
    st.markdown('<div class="brand">Smart Self-Appraisal+</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enhanced UI & auto-organized by department</div>', unsafe_allow_html=True)

st.write('---')

# --- Session state management for dynamic inputs ---
if 'course_count' not in st.session_state:
    st.session_state.course_count = 3
if 'award_count' not in st.session_state:
    st.session_state.award_count = 3

# --- Main Form ---
with st.form('appraisal_form'):
    name = st.text_input('👤 Full Name')
    email = st.text_input('📧 Work Email')
    dept = st.text_input('🏢 Department')
    role = st.text_input('💼 Role / Designation')

    # Courses section header + place for Add button (button must be outside form)
    st.markdown('<div class="section-title">📘 Courses / Training</div>', unsafe_allow_html=True)
    st.caption("Add course titles and hours. To add more than the shown fields, use the 'Add another course' button below the section (outside the form).", unsafe_allow_html=True)
    courses = []
    for i in range(st.session_state.course_count):
        cols = st.columns([4, 2])
        title = cols[0].text_input(f'Course title #{i+1}', key=f'course_title_{i}')
        hours = cols[1].number_input(f'Hours #{i+1}', min_value=0, step=1, key=f'course_hours_{i}')
        if title:
            courses.append({'title': title, 'hours': hours, 'points_per_course': 2})

    st.markdown('<div class="section-title">📚 Research & Teaching</div>', unsafe_allow_html=True)
    papers = st.number_input('📰 Papers published', min_value=0, step=1)
    paper_titles = st.text_area('Paper titles (comma separated)')
    patents = st.number_input('🧠 Patents granted', min_value=0, step=1)
    patent_details = st.text_area('Patent IDs / details')
    corp_trainings = st.number_input('🏫 Corporate trainings conducted', min_value=0, step=1)
    corp_details = st.text_area('Company names / topics (one per line)')
    projects = st.number_input('💡 Consultancy / Projects completed', min_value=0, step=1)
    proj_details = st.text_area('Project details (one per line)')

    st.markdown('<div class="section-title">🏅 Awards & Certificates</div>', unsafe_allow_html=True)
    st.caption("Enter awards or certificates. Use 'Add another award' below the section to show more fields.", unsafe_allow_html=True)
    awards = []
    for i in range(st.session_state.award_count):
        cols = st.columns([3, 2])
        title = cols[0].text_input(f'Award #{i+1}', key=f'award_title_{i}')
        year = cols[1].text_input(f'Year #{i+1}', key=f'award_year_{i}')
        if title:
            awards.append({'title': title, 'year': year})

    teaching = st.text_area('📚 Teaching summary (courses, topics, target audience)')
    research = st.text_area('🔬 Research summary (proposals, grants, etc.)')
    rating = st.slider('⭐ Overall self-rating', 1, 5, 4)
    comments = st.text_area('💬 Comments (achievements, goals for next period)')

    submitted = st.form_submit_button('🚀 Submit appraisal')

# --- Add-buttons placed under their sections but kept OUTSIDE the form ---
# We reproduce the visual placement by placing the buttons right after the form,
# each labeled so users understand which section they affect.

st.markdown(" ")  # spacer
cols = st.columns(2)
with cols[0]:
    st.markdown("**Courses / Training — add more**")
    if st.button("➕ Add another course"):
        st.session_state.course_count += 1
        # No st.experimental_rerun() — Streamlit will rerun automatically on button click.
with cols[1]:
    st.markdown("**Awards & Certificates — add more**")
    if st.button("🏅 Add another award"):
        st.session_state.award_count += 1
        # No st.experimental_rerun()

st.write('---')

# --- Submission handling (runs when form_submit_button was pressed) ---
if submitted:
    submission = {
        'id': str(uuid.uuid4())[:8],
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'employee_name': name,
        'employee_email': email,
        'department': dept,
        'role': role,
        'contributions': {
            'courses': courses,
            'papers': {'count': papers, 'titles': [p.strip() for p in paper_titles.split(',') if p.strip()]},
            'patents': {'count': patents, 'details': patent_details},
            'corporate_trainings': {'count': corp_trainings, 'details': corp_details},
            'projects': {'count': projects, 'details': [p.strip() for p in proj_details.split('\n') if p.strip()]},
            'awards': awards
        },
        'teaching': teaching,
        'research': research,
        'self_rating_overall': rating,
        'comments': comments
    }

    try:
        if GS_AVAILABLE and 'gcp_service_account' in st.secrets and 'GOOGLE_SHEET_ID' in st.secrets:
            append_to_gsheet(submission)
            st.success('✅ Saved to Google Sheets (auto-organized by department/year)')
        else:
            raise RuntimeError('Google Sheets credentials missing')
    except Exception as e:
        path = local_save(submission)
        st.warning(f'⚠️ Could not save to Google Sheets. Saved locally at {path}')

    st.balloons()
    st.json(submission)
    st.download_button('📥 Download submission (JSON)', data=json.dumps(submission, indent=2),
                       file_name=f'appraisal_{submission['id']}.json')

st.write('---')
st.markdown('**requirements.txt**')
st.code('''streamlit
gspread
google-auth
pandas
requests
''', language='bash')
