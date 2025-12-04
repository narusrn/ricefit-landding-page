import os
import re
import sys
import time
import hashlib
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime

st.set_page_config(page_title="Ricefit API (Register)", layout="wide")

st.sidebar.page_link('pages/getting_started.py', label='Getting Started')
st.sidebar.markdown("""
<style>
/* base style */
.sidebar-subitem {
    margin-left: 16px;
    font-size: 14px;
    display: block;
    color: #333 !important;   /* เริ่มต้นเป็นสีดำ */
    padding: 4px 0;
    text-decoration: none !important;
}

/* hover = ฟ้า */
.sidebar-subitem:hover {
    color: #1a73e8 !important;
    text-decoration: none !important;
}

/* active (คลิกขณะกด) */
.sidebar-subitem:active {
    color: #1a73e8 !important;
}

}
</style>

<a class="sidebar-subitem" href="/?page=getting_started&section=การสมัครการใช้งาน#การสมัครการใช้งาน">การสมัครการใช้งาน</a>
<a class="sidebar-subitem" href="#การยืนยันสิทธิ์การใช้งาน">การยืนยันสิทธิ์การใช้งาน</a>
""", unsafe_allow_html=True)

st.sidebar.page_link('pages/register.py', label='Register')


@st.dialog("กรุณายืนยันการดำเนินการ")
def register_confirm():
    st.write("คุณต้องการยืนยันการลงทะเบียนหรือไม่?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("ยืนยัน"):
            data = st.session_state["pending_data"]
            recording_submition(data)
            reset_form()
            st.rerun()

    with col2:
        if st.button("ยกเลิก"):
            st.rerun()

def reset_form():
    for key in ["first_name", "last_name", "email", "mobile", "occupation",
                "organization", "location", "org_type", "phone", "purpose",
                "pending_data", "to_submit"]:
        st.session_state[key] = ""

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Please enter a valid email address"
    return True, ""


def validate_phone(phone):
    pattern = r'^\d{9,10}$'
    if not re.match(pattern, phone):
        return False, "Please enter a valid phone number"
    return True, ""

def recording_submition(data):
    try : 
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict( st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], scope)
        spreadsheet_id = '1_YHFcF6DJ74AyshIW7iGzku1u30vBfCSQU2kD2bDuIc'

        rows = [
            [str(v) for k, v in data.items()],
        ]
        service = build('sheets', 'v4', credentials=credentials)
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="A:Z",
            body={
                "majorDimension": "ROWS",
                "values": rows
            },
            valueInputOption="USER_ENTERED"
        ).execute()
                    
    except Exception as e:
        print(f"[recording_submition] ERROR: {e}", file=sys.stderr, flush=True)


st.title("ลงทะเบียนใช้งาน API")

with st.form("register_form"):
    col1, col2 = st.columns(2)

    # ------------- LEFT COLUMN -------------
    with col1:
        first_name = st.text_input("ชื่อ", key="first_name")
        last_name = st.text_input("นามสกุล", key="last_name")

        email = st.text_input("อีเมล", key="email")
        if email:
            is_valid, message = validate_email(email)
            if not is_valid:
                st.error(message)

        mobile = st.text_input("หมายเลขโทรศัพท์มือถือ", key="mobile")
        if mobile:
            is_valid, message = validate_phone(mobile)
            if not is_valid:
                st.error(message)

    # ------------- RIGHT COLUMN -------------
    with col2:
        occupation = st.selectbox(
            "อาชีพ",
            [
                "นักพัฒนาอิสระ",
                "นักศึกษา/บุคลากรในสถานศึกษา",
                "พนักงานองค์กร/บริษัทเอกชน",
                "ข้าราชการ/พนักงานหน่วยงานของรัฐ",
            ],
            key="occupation"
        )
        organization = st.text_input("หน่วยงาน", key="organization")
        location = st.text_input("สถานที่ตั้ง", key="location")
        org_type = st.selectbox(
            "ประเภทหน่วยงาน",
            [
                "ในนามบุคคล",
                "สถานศึกษา",
                "องค์กร/บริษัทเอกชน",
                "หน่วยงานราชการ/หน่วยงานในกำกับของรัฐ",
                "หน่วยงานความร่วมมือระหว่างประเทศ",
            ],
            key="org_type"
        )
        phone = st.text_input("เบอร์โทรศัพท์ (หน่วยงาน)", key="phone")
        purpose = st.text_area("จุดประสงค์", key="purpose")

    submitted = st.form_submit_button("สมัครใช้งาน")

# ======================
# Submit Logic
# ======================
if submitted:

    validations = [
        validate_email(email),
        validate_phone(mobile),
    ]
        
    if all(v[0] for v in validations):

        # เก็บข้อมูลไว้ก่อน
        st.session_state["pending_data"] = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "mobile": mobile,
            "occupation": occupation,
            "organization": organization,
            "location": location,
            "org_type": org_type,
            "phone": phone,
            "purpose": purpose,
            "created_at": datetime.now().isoformat(),
            'submitted': True
        }

        register_confirm()

    else : 
        st.error("กรุณากรอกข้อมูลให้ครบถ้วนและถูกต้อง")
        
# ======================
# Support Contact
# ======================
st.markdown("---")
st.markdown(
    """
📩 **ติดต่อฝ่ายสนับสนุน (Support Team)**  
หากพบปัญหาในการลงทะเบียนหรือต้องการสอบถามข้อมูลเพิ่มเติม  
กรุณาติดต่อ: **teera.phatrapornnant@nectec.or.th**
"""
)












