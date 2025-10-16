import streamlit as st
import pandas as pd
import json
import datetime
import uuid
from pathlib import Path
from streamlit_lottie import st_lottie
import requests

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GS_AVAILABLE = True
except Exception:
    GS_AVAILABLE = False

# --- Helper functions ---

def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

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
</style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([2,3])
with col1:
    st.image('/mnt/data/WhatsApp Image 2025-10-15 at 3.23.45 PM.jpeg', width=200)
with col2:
    st.markdown('<div class="brand">Smart Self-Appraisal+</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enhanced, animated & auto-organized by department</div>', unsafe_allow_html=True)

st_lottie(load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"), height=150, key="intro_anim")

st.write('---')

# --- Form ---
with st.form('appraisal_form'):
    name = st.text_input('👤 Full Name')
    email = st.text_input('📧 Work Email')
    dept = st.text_input('🏢 Department')
    role = st.text_input('💼 Role / Designation')

    st.markdown('<div class="section-title">📘 Contributions</div>', unsafe_allow_html=True)
    if 'courses' not in st.session_state:
        st.session_state['courses'] = [{ 'title':'', 'hours':'', 'points_per_course':2 }]
    for i, c in enumerate(st.session_state['courses']):
        cols = st.columns([4,2,1])
        st.session_state['courses'][i]['title'] = cols[0].text_input(f'Course title #{i+1}', value=c['title'], key=f'course_title_{i}')
        st.session_state['courses'][i]['hours'] = cols[1].number_input(f'Hours #{i+1}', min_value=0, step=1, value=int(c['hours']) if str(c['hours']).isdigit() else 0, key=f'course_hours_{i}')
        if cols[2].button('➕', key=f'add_course_{i}'):
            st.session_state['courses'].append({ 'title':'', 'hours':'', 'points_per_course':2 })
            st.experimental_rerun()

    papers = st.number_input('📰 Papers published', min_value=0, step=1)
    paper_titles = st.text_area('Paper titles (comma separated)')

    patents = st.number_input('🧠 Patents granted', min_value=0, step=1)
    patent_details = st.text_area('Patent IDs / details')

    corp_trainings = st.number_input('🏫 Corporate trainings conducted', min_value=0, step=1)
    corp_details = st.text_area('Company names / topics (one per line)')

    projects = st.number_input('💡 Consultancy / Projects completed', min_value=0, step=1)
    proj_details = st.text_area('Project details (one per line)')

    if 'awards' not in st.session_state:
        st.session_state['awards'] = [{ 'title':'', 'year':'' }]
    st.markdown('<div class="section-title">🏅 Awards & Certificates</div>', unsafe_allow_html=True)
    for i, a in enumerate(st.session_state['awards']):
        cols = st.columns([3,2,1])
        st.session_state['awards'][i]['title'] = cols[0].text_input(f'Award #{i+1}', value=a['title'], key=f'award_title_{i}')
        st.session_state['awards'][i]['year'] = cols[1].text_input(f'Year #{i+1}', value=a['year'], key=f'award_year_{i}')
        if cols[2].button('➕', key=f'add_award_{i}'):
            st.session_state['awards'].append({ 'title':'', 'year':'' })
            st.experimental_rerun()

    teaching = st.text_area('📚 Teaching summary (courses, topics, target audience)')
    research = st.text_area('🔬 Research summary (proposals, grants, etc.)')
    rating = st.slider('⭐ Overall self-rating', 1, 5, 4)
    comments = st.text_area('💬 Comments (achievements, goals for next period)')

    submitted = st.form_submit_button('🚀 Submit appraisal')

if submitted:
    submission = {
        'id': str(uuid.uuid4())[:8],
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'employee_name': name,
        'employee_email': email,
        'department': dept,
        'role': role,
        'contributions': {
            'courses': st.session_state.get('courses', []),
            'papers': {'count': papers, 'titles': [p.strip() for p in paper_titles.split(',') if p.strip()]},
            'patents': {'count': patents, 'details': patent_details},
            'corporate_trainings': {'count': corp_trainings, 'details': corp_details},
            'projects': {'count': projects, 'details': [p.strip() for p in proj_details.split('\n') if p.strip()]},
            'awards': st.session_state.get('awards', [])
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
    st.download_button('📥 Download submission (JSON)', data=json.dumps(submission, indent=2), file_name=f'appraisal_{submission["id"]}.json')

st.write('---')
st.markdown('**requirements.txt**')
st.code('''
streamlit
streamlit-lottie
gspread
google-auth
pandas
requests
''', language='bash')
