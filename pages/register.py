import os
import re
import sys
import time
import hashlib
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
load_dotenv()

st.set_page_config(page_title="Ricefit API (Register)", layout="wide")

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')

st.sidebar.page_link('pages/register.py', label='Register')

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
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scope)
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
        first_name = st.text_input("ชื่อ")
        last_name = st.text_input("นามสกุล")

        email = st.text_input("อีเมล")
        if email:
            is_valid, message = validate_email(email)
            if not is_valid:
                st.error(message)

        mobile = st.text_input("หมายเลขโทรศัพท์มือถือ")
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
        )
        organization = st.text_input("หน่วยงาน")
        location = st.text_input("สถานที่ตั้ง")
        org_type = st.selectbox(
            "ประเภทหน่วยงาน",
            [
                "ในนามบุคคล",
                "สถานศึกษา",
                "องค์กร/บริษัทเอกชน",
                "หน่วยงานราชการ/หน่วยงานในกำกับของรัฐ",
                "หน่วยงานความร่วมมือระหว่างประเทศ",
            ],
        )
        phone = st.text_input("เบอร์โทรศัพท์ (หน่วยงาน)")
        purpose = st.text_area("จุดประสงค์")

    submitted = st.form_submit_button("สมัครใช้งาน")

# ======================
# Submit Logic
# ======================
if submitted:
    # Validate all fields
    validations = [
        validate_email(email),
        validate_phone(mobile),
    ]

    # Check if all validations pass
    if all(v[0] for v in validations):
        st.success("Form submitted successfully!")
        # Update session state
        recording_submition({
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
        })
        
        st.toast("🎉 ลงทะเบียนสำเร็จ!", icon="🎉")
        time.sleep(1.2)      # ให้ popup แสดงก่อน
        st.rerun()


