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

# -------------------- Helper functions --------------------
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
    flat['self_rating_overall'] = sub.get('self_rating_overall')
    flat['comments'] = sub.get('comments')
    flat['contributions'] = json.dumps(sub.get('contributions', {}), ensure_ascii=False)
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
    if not ws.get_all_values():
        ws.append_row(list(flat.keys()))
    ws.append_row(list(flat.values()))
    return True


# -------------------- UI Setup --------------------
st.set_page_config(page_title='Self Appraisal — SmartForm+', layout='wide', page_icon='📝')

st.markdown("""
<style>
.brand{font-size:30px;font-weight:700;color:#124265}
.subtitle{color:#475569;font-size:15px;margin-top:-8px}
.section-title{font-weight:600;font-size:18px;margin-top:20px}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 3])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=120)
with col2:
    st.markdown('<div class="brand">Smart Self-Appraisal+</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enhanced UI • Auto-organized by department</div>', unsafe_allow_html=True)
st.write('---')


# -------------------- Session state --------------------
if 'course_count' not in st.session_state:
    st.session_state.course_count = 3
if 'award_count' not in st.session_state:
    st.session_state.award_count = 3

# -------------------- Dynamic control buttons ABOVE the form --------------------
st.subheader("🧩 Add More Sections Before Filling")

cc1, cc2 = st.columns(2)
with cc1:
    if st.button("➕ Add another course field"):
        st.session_state.course_count += 1
with cc2:
    if st.button("🏅 Add another award field"):
        st.session_state.award_count += 1

st.caption("You can click the buttons above to show more input fields before submitting your form.")
st.write('---')


# -------------------- Appraisal Form --------------------
with st.form('appraisal_form'):
    name = st.text_input('👤 Full Name')
    email = st.text_input('📧 Work Email')
    dept = st.text_input('🏢 Department')
    role = st.text_input('💼 Role / Designation')

    st.markdown('<div class="section-title">📘 Courses / Training</div>', unsafe_allow_html=True)
    courses = []
    for i in range(st.session_state.course_count):
        cols = st.columns([4, 2])
        title = cols[0].text_input(f'Course title #{i+1}', key=f'course_title_{i}')
        hours = cols[1].number_input(f'Hours #{i+1}', min_value=0, step=1, key=f'course_hours_{i}')
        if title:
            courses.append({'title': title, 'hours': hours, 'points_per_course': 2})

    st.markdown('<div class="section-title">🏅 Awards & Certificates</div>', unsafe_allow_html=True)
    awards = []
    for i in range(st.session_state.award_count):
        cols = st.columns([3, 2])
        title = cols[0].text_input(f'Award #{i+1}', key=f'award_title_{i}')
        year = cols[1].text_input(f'Year #{i+1}', key=f'award_year_{i}')
        if title:
            awards.append({'title': title, 'year': year})

    st.markdown('<div class="section-title">📚 Research & Teaching</div>', unsafe_allow_html=True)
    papers = st.number_input('📰 Papers published', min_value=0, step=1)
    paper_titles = st.text_area('Paper titles (comma separated)')
    patents = st.number_input('🧠 Patents granted', min_value=0, step=1)
    patent_details = st.text_area('Patent IDs / details')
    corp_trainings = st.number_input('🏫 Corporate trainings conducted', min_value=0, step=1)
    corp_details = st.text_area('Company names / topics (one per line)')
    projects = st.number_input('💡 Consultancy / Projects completed', min_value=0, step=1)
    proj_details = st.text_area('Project details (one per line)')

    teaching = st.text_area('📘 Teaching summary')
    research = st.text_area('🔬 Research summary')
    rating = st.slider('⭐ Overall self-rating', 1, 5, 4)
    comments = st.text_area('💬 Additional Comments')

    submitted = st.form_submit_button('🚀 Submit Appraisal')

# -------------------- Submission Handling --------------------
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
    st.download_button('📥 Download submission (JSON)',
                       data=json.dumps(submission, indent=2),
                       file_name=f'appraisal_{submission["id"]}.json')

st.write('---')
st.markdown('**requirements.txt**')
st.code('''streamlit
gspread
google-auth
pandas
requests
''', language='bash')
