import streamlit as st
import pandas as pd
import json
import datetime
import uuid
from pathlib import Path

# --- Page configuration MUST be the very first Streamlit call after imports ---
st.set_page_config(page_title='Employee Self Appraisal 2025', page_icon='📝', layout='wide')

# Optional Google libs
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GS_AVAILABLE = True
except Exception:
    GS_AVAILABLE = False

# Note: google-api-python-client is imported lazily in upload_json_to_drive()

# -------------------- Helper functions --------------------
def local_save(submission: dict, folder='submissions'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = Path(folder) / f"submission_{submission['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(submission, f, ensure_ascii=False, indent=2, default=str)
    return str(filename)


def upload_json_to_drive(local_path: str, filename: str, folder_id: str, service_account_info: dict):
    """Upload a local JSON file to Google Drive using a service account.
    Returns the created Drive file id.
    Requires google-api-python-client in requirements.txt.
    """
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.service_account import Credentials as GACreds
    except Exception as e:
        raise RuntimeError('google-api-python-client not installed; add it to requirements.txt') from e

    scopes = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = GACreds.from_service_account_info(service_account_info, scopes=scopes)
    drive_service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': filename}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(local_path, mimetype='application/json')
    created = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return created.get('id')


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
    # store contributions as JSON string to avoid complex sheet cells
    flat['contributions'] = json.dumps(sub.get('contributions', {}), ensure_ascii=False)
    return flat


def append_to_gsheet(submission: dict):
    if not GS_AVAILABLE:
        raise RuntimeError('gspread/google-auth not installed')

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


def load_all_submissions(folder='submissions'):
    p = Path(folder)
    if not p.exists():
        return pd.DataFrame()
    files = sorted(p.glob('submission_*.json'))
    records = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
                flat = flatten_submission(data)
                records.append(flat)
        except Exception:
            continue
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df


# -------------------- Styling & header (integrating both images) --------------------
st.markdown(
    """
    <style>
    body {background: linear-gradient(120deg, #f6f9ff 0%, #ffffff 100%);}
    .brand{font-size:28px;font-weight:800;color:#0f172a}
    .subtitle{color:#475569;font-size:14px;margin-top:-6px}
    .section-title{font-weight:700;font-size:16px;margin-top:14px;margin-bottom:6px;color:#093169}
    .divider{height:2px;border:none;background:linear-gradient(to right,#2563eb22,#60a5fa22);margin:18px 0}
    .summary-card{background:#ffffffcc;padding:12px;border-radius:10px;box-shadow:0 6px 18px rgba(16,24,40,0.06)}
    .muted{color:#6b7280}
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([2, 3])
with col1:
    st.image('https://cdn-icons-png.flaticon.com/512/1055/1055646.png', width=110)
with col2:
    st.markdown('<div class="brand">Employee Self Appraisal 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">A friendly, mobile-first appraisal form — inspired by your two design references</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# -------------------- Session state for dynamic fields --------------------
if 'course_count' not in st.session_state:
    st.session_state.course_count = 3
if 'award_count' not in st.session_state:
    st.session_state.award_count = 3

# -------------------- Employee info compact form (optional confirm) --------------------
st.markdown('### Employee information')
colA, colB, colC = st.columns([2,2,2])
with colA:
    emp_name = st.text_input('Full name', key='emp_name')
with colB:
    emp_id = st.text_input('Employee ID', key='emp_id')
with colC:
    dept_default = st.session_state.get('default_dept', '')
    emp_dept = st.text_input('Department', value=dept_default, key='emp_dept')

st.markdown('<div class="muted">Tip: press the Add buttons to create more input rows before filling the form.</div>', unsafe_allow_html=True)
st.write('---')

# -------------------- Dynamic control buttons (placed visibly above form) --------------------
ctrl1, ctrl2 = st.columns(2)
with ctrl1:
    if st.button('➕ Add another course field'):
        st.session_state.course_count += 1
with ctrl2:
    if st.button('🏅 Add another award field'):
        st.session_state.award_count += 1

st.write('---')

# -------------------- Main Appraisal Form --------------------
with st.form('appraisal_form'):
    st.markdown('<div class="section-title">Achievements & Summary</div>', unsafe_allow_html=True)
    achievements = st.text_area('Summarize your key contributions this year', key='achievements')

    st.markdown('<div class="section-title">Courses / Trainings</div>', unsafe_allow_html=True)
    courses = []
    for i in range(st.session_state.course_count):
        c1, c2 = st.columns([4, 2])
        title = c1.text_input(f'Course title #{i+1}', key=f'course_title_{i}')
        hours = c2.number_input(f'Hours #{i+1}', min_value=0, step=1, key=f'course_hours_{i}')
        if title:
            courses.append({'title': title, 'hours': hours})

    st.markdown('<div class="section-title">Awards & Certificates</div>', unsafe_allow_html=True)
    awards = []
    for i in range(st.session_state.award_count):
        a1, a2 = st.columns([3, 2])
        atitle = a1.text_input(f'Award / Certificate #{i+1}', key=f'award_title_{i}')
        ayear = a2.text_input(f'Year #{i+1}', key=f'award_year_{i}')
        if atitle:
            awards.append({'title': atitle, 'year': ayear})

    st.markdown('<div class="section-title">Research & Projects</div>', unsafe_allow_html=True)
    papers = st.number_input('Papers published', min_value=0, step=1, key='papers')
    paper_titles = st.text_area('Paper titles (comma separated)', key='paper_titles')
    patents = st.number_input('Patents granted', min_value=0, step=1, key='patents')
    patent_details = st.text_area('Patent details', key='patent_details')
    projects = st.number_input('Consultancy / Projects completed', min_value=0, step=1, key='projects')
    project_details = st.text_area('Project details', key='project_details')

    st.markdown('<div class="section-title">Teaching & Goals</div>', unsafe_allow_html=True)
    teaching = st.text_area('Teaching summary', key='teaching')
    goals = st.text_area('Goals for next year', key='goals')

    st.markdown('<div class="section-title">Self rating & comments</div>', unsafe_allow_html=True)
    rating = st.slider('Overall self-rating (1 = Needs improvement, 5 = Excellent)', 1, 5, 4, key='rating')
    comments = st.text_area('Additional comments', key='comments')

    # Review expander (from 2nd image)
    with st.expander('🔍 Review & Preview submission'):
        st.markdown('**Employee**')
        st.write(f"Name: {emp_name}")
        st.write(f"Employee ID: {emp_id}")
        st.write(f"Department: {emp_dept}")
        st.markdown('**Contributions**')
        st.write('Achievements:', achievements)
        st.write('Courses:', courses)
        st.write('Awards:', awards)
        st.write('Papers:', paper_titles)
        st.write('Projects:', project_details)
        st.write('Goals:', goals)
        st.write('Rating:', rating)

    submitted = st.form_submit_button('✅ Submit appraisal')

# -------------------- Submission handling --------------------
if submitted:
    submission = {
        'id': str(uuid.uuid4())[:8],
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'employee_name': emp_name,
        'employee_email': '',
        'department': emp_dept,
        'role': '',
        'contributions': {
            'achievements': achievements,
            'courses': courses,
            'awards': awards,
            'papers': {'count': int(papers), 'titles': [t.strip() for t in str(paper_titles).split(',') if t.strip()]},
            'patents': {'count': int(patents), 'details': patent_details},
            'projects': {'count': int(projects), 'details': [l.strip() for l in str(project_details).split('\n') if l.strip()]}
        },
        'teaching': teaching,
        'research': '',
        'self_rating_overall': int(rating),
        'comments': comments,
        'goals': goals
    }

    # Save local JSON file per submission
    local_path = local_save(submission)
    st.success(f'Local JSON saved: {local_path}')

    # Append to Google Sheets (flattened row) if configured
    try:
        if GS_AVAILABLE and 'gcp_service_account' in st.secrets and 'GOOGLE_SHEET_ID' in st.secrets:
            append_to_gsheet(submission)
            st.info('Appended to Google Sheet')
        else:
            st.warning('Google Sheets not configured; saved locally only')
    except Exception as e:
        st.warning(f'Could not append to Google Sheets: {e}')

    # Optionally upload the JSON into Drive folder
    try:
        drive_folder = st.secrets.get('GOOGLE_DRIVE_FOLDER_ID')
        service_account_info = st.secrets.get('gcp_service_account')
        if drive_folder and service_account_info:
            try:
                file_id = upload_json_to_drive(local_path, Path(local_path).name, drive_folder, service_account_info)
                st.info(f'Uploaded JSON to Drive (file id: {file_id})')
            except Exception as e:
                st.warning(f'Drive upload failed: {e}')
    except Exception:
        pass

    st.balloons()
    st.download_button('📥 Download submission (JSON)', data=json.dumps(submission, indent=2), file_name=f'appraisal_{submission["id"]}.json')

# -------------------- Admin / Combine view --------------------
st.write('---')
if st.checkbox('📊 Show integrated local submission DataFrame'):
    df = load_all_submissions()
    if df.empty:
        st.info('No local submissions found')
    else:
        st.dataframe(df)
        st.download_button('⬇️ Download all (CSV)', df.to_csv(index=False), 'all_submissions.csv')

# -------------------- requirements snippet --------------------
st.markdown('**requirements.txt**')
st.code('''
streamlit
gspread
google-auth
pandas
requests
google-api-python-client
''', language='bash')
