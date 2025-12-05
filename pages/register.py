import re
import streamlit as st
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import sys

st.set_page_config(page_title="RiceFit API (Register)", layout="wide")

st.sidebar.page_link('pages/getting_started.py', label='Getting Started')
st.sidebar.page_link('pages/register.py', label='Register')
st.sidebar.page_link('pages/apidocs.py', label='API ที่ให้บริการ')

# ------------------------------
# Field Definitions
# ------------------------------
fields = [
    {"key": "first_name", "label": "ชื่อ", "required": True, "validator": lambda x: bool(x.strip())},
    {"key": "last_name", "label": "นามสกุล", "required": True, "validator": lambda x: bool(x.strip())},
    {"key": "email", "label": "อีเมล", "required": True, "validator": lambda x: re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', x)},
    {"key": "mobile", "label": "หมายเลขโทรศัพท์มือถือ", "required": True, "validator": lambda x: re.match(r'^\d{9,10}$', x)},
    {"key": "purpose", "label": "วัตถุประสงค์การใช้งาน", "required": True, "validator": lambda x: bool(x.strip())},
    {"key": "occupation", "label": "อาชีพ", "required": False},
    {"key": "organization", "label": "หน่วยงาน", "required": True, "validator": lambda x: bool(x.strip())},
    {"key": "location", "label": "สถานที่ตั้ง", "required": False},
    {"key": "org_type", "label": "ประเภทหน่วยงาน", "required": False},
    {"key": "phone", "label": "เบอร์โทรศัพท์ (หน่วยงาน)", "required": False},
]

# ------------------------------
# Helper Functions
# ------------------------------
def recording_submission(data):
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], scope)
        spreadsheet_id = '1_YHFcF6DJ74AyshIW7iGzku1u30vBfCSQU2kD2bDuIc'

        rows = [[str(v) for k, v in data.items()]]
        service = build('sheets', 'v4', credentials=credentials)
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="A:Z",
            body={"majorDimension": "ROWS", "values": rows},
            valueInputOption="USER_ENTERED"
        ).execute()
    except Exception as e:
        print(f"[recording_submission] ERROR: {e}", file=sys.stderr, flush=True)

def reset_form():
    for field in fields + [{"key": "pending_data"}, {"key": "to_submit"}]:
        st.session_state[field["key"] if isinstance(field, dict) else field] = ""

# ------------------------------
# Registration Dialog
# ------------------------------
@st.dialog("กรุณายืนยันการดำเนินการ")
def register_confirm():
    st.write("""
    คุณต้องการยืนยันการลงทะเบียนหรือไม่?  
    ระบบจะส่ง API Key สำหรับใช้งานไปยังอีเมลที่ท่านลงทะเบียนไว้
    """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ยืนยัน"):
            data = st.session_state["pending_data"]
            recording_submission(data)
            reset_form()
            st.rerun()
    with col2:
        if st.button("ยกเลิก"):
            st.rerun()

# ------------------------------
# Registration Form
# ------------------------------
st.title("ลงทะเบียนใช้งาน RiceFit API")

with st.form("register_form"):
    col1, col2 = st.columns(2)
    error_placeholders = {}

    # LEFT COLUMN: required fields
    with col1:
        for key in ["first_name", "last_name", "email", "mobile"]:
            field = next(f for f in fields if f["key"] == key)
            value = st.text_input(field["label"], key=key)
            placeholder = st.empty()  # placeholder สำหรับ error message
            error_placeholders[key] = placeholder

    # RIGHT COLUMN: other fields + purpose
    with col2:
        occupation = st.selectbox(
            "อาชีพ",
            ["นักพัฒนาอิสระ", "นักศึกษา/บุคลากรในสถานศึกษา", "พนักงานองค์กร/บริษัทเอกชน", "ข้าราชการ/พนักงานหน่วยงานของรัฐ"],
            key="occupation"
        )
        organization = st.text_input("หน่วยงาน", key="organization")
        error_placeholders["organization"] = st.empty()
        location = st.text_input("สถานที่ตั้ง", key="location")
        org_type = st.selectbox(
            "ประเภทหน่วยงาน",
            ["ในนามบุคคล", "สถานศึกษา", "องค์กร/บริษัทเอกชน", "หน่วยงานราชการ/หน่วยงานในกำกับของรัฐ", "หน่วยงานความร่วมมือระหว่างประเทศ"],
            key="org_type"
        )
        phone = st.text_input("เบอร์โทรศัพท์ (หน่วยงาน)", key="phone")
        purpose = st.text_area("วัตถุประสงค์การใช้งาน", key="purpose")
        error_placeholders["purpose"] = st.empty()

    submitted = st.form_submit_button("สมัครใช้งาน")

# ------------------------------
# Submit Logic
# ------------------------------
if submitted:
    errors = {}
    for field in fields:
        value = st.session_state.get(field["key"], "").strip()
        if field.get("required") and not value:
            errors[field["key"]] = f"{field['label']} เป็นฟิลด์ที่จำเป็นต้องกรอก"
        elif "validator" in field and value and not field["validator"](value):
            errors[field["key"]] = f"{field['label']} ไม่ถูกต้อง"

    # แสดง error ใต้แต่ละ input
    for key, placeholder in error_placeholders.items():
        if key in errors:
            placeholder.error(errors[key])
        else:
            placeholder.empty()  # ล้าง error ถ้าไม่มี

    # ถ้าไม่มี error ให้ไป confirm dialog
    if not errors:
        st.session_state["pending_data"] = {f["key"]: st.session_state.get(f["key"], "") for f in fields}
        st.session_state["pending_data"]["created_at"] = datetime.now().isoformat()
        st.session_state["pending_data"]["submitted"] = True
        register_confirm()

# ------------------------------
# Support Contact
# ------------------------------
st.markdown("---")
st.markdown(
    """
📩 **ติดต่อฝ่ายสนับสนุน (Support Team)**  
หากพบปัญหาในการลงทะเบียนหรือต้องการสอบถามข้อมูลเพิ่มเติม  
กรุณาติดต่อ: **teera.phatrapornnant@nectec.or.th**
"""
)

