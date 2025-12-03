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
        credentials = ServiceAccountCredentials.from_json_keyfile_dict({
          "type": "service_account",
          "project_id": "agritronicssitelists",
          "private_key_id": "949a5883f59ceb2e22c8a1d81d9666f8a6067549",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9BQrPbJXwQqBA\n1hAkssQZLdLEmp7F45x1GWRWNEcwwYv16MvfubUQX4sFBGFkmc898efsbQ43oKvl\nk5qWr4aX+d7I4ABOu4lXVgBXiQwScYnFjmvg0VsdE/lVgjLPwj5LwGlc6B/eZAEu\njxEaR5NaoiWXjJzlod+Kn6UQZlRdJngOb70aNTyvHgNGlj5dajJKBIsxI+zV2SuA\nHUKeRqu5MOlmPrxJIY2iwZ7egBu9GK0zA2UZV8KHbxJq1+y4ODi+5kHsKlle2kg1\n86NCiJtUXZ87pgsm9a+9OMuuB3Gq4RpncW6m21O6+IEAxLGGo+l8r01eh6lOHqq3\nyrUxuXvDAgMBAAECggEAA5l0+z42HL0oEBQDeq9szI3y1YucOmh7Mj+piXq1YFhP\nMf+c4kXHDOjE3POYZzIGoEdbA0WQX77Phy+oYfY1ue8oLusVFmq70s3wc7pIYJGI\n7hooM7/I3GTk+pvgG9S3GvovB3XkJXgCDcDrsnRqee9ch+ZFlpneh+VCX22TbbKl\nZ8oiP6bxZU3CF3mGmUuhM7LaBnFXsCo9iwRSkN5tKlHsQhqfch7Zc1/IYu9Jf4r5\nGsTAo8O+ryXpR5DVp5BdSPjJ1vvAfNDPSmAoFQ2xoNtOCqJ4vbbhLWOekt7owozi\nXdLU63Q4viszqk0SFf6tbbmGfqEN8bfbONYqDx88AQKBgQD2qxvXD2GyH4Gih/Pm\nk4y/uIL3sJeMsUuK0t/UJKQ/uI1uzPF4azsluIIEDh2GiH/CXwppu5ZLI9d80IEG\njvPQ3zD/AhRoYUADOg6/UJDDGT4ffOqB7cuZE0ncPVZh3ImvokAOcJ2RjPxOrAkp\nY7jjBAWn+53JFVCsTjAMHhBZEQKBgQDEK6Cb1G2VLVKn4FqIcMriS8Bm7c5mZcx0\n7n+Rg0btfYsnuLX5DDLNM9dy3zil2xCUUSFO89SoBsCFtc2fg+4T6E7w6PBOaaTq\nEvtcT/Z5WUpkRTD/VsfathPdstlXtjWWhcSBYlCXBcqW8h68BTkXnp7vM2qUKnyR\n9nKujnjnkwKBgQCxVtFcK53UXtxnipCqjBgb2j6mbtp19x1VgEgVkAZaHYfpSgSs\ny4Mpml43JiLKDyazCntFCu2BthH9lTW+DlZyK5RhMhCT/p7z8vCZUQXSjjpgjwFW\nSi0fL4PhiGOrVc/TarXc69AMzayzrvGjRSOuarzaSYbmA6INTuUyQQcF0QKBgG0D\nHX5bHwZOKGeX+ldl7qiwldvc/NzUZzj3rDZtsEWbhW/uallamQSFcY2pVC5+vQje\nyNa6EwvIrMXhEMI7K1sutmeT2q6IcJePMtXKrdojb36nIKJUVD1K/2Es2TCv1bmu\n3lNUEhrKohkdtUygzmg8wm+EsA5kSdNHE9XC4Jc3AoGAdNP78a0K0H28AUf5jC+Y\nCrVaNWPFkCL5o+bwG0xSCjUoVcvQI3+WGgal5iOvvo2E+nHHB9W6v1b8LIfLfRvR\nL8rLyiQldJVFm6pRN8TB6yhM+/6510LVGgbiVe00PRPLCN9QHPjXHV8+cXgyDhei\nPq4K/uEmtw/uGibMAZ0g6TQ=\n-----END PRIVATE KEY-----\n",
          "client_email": "agritronicssitelists@agritronicssitelists.iam.gserviceaccount.com",
          "client_id": "117687940972076786827",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/agritronicssitelists%40agritronicssitelists.iam.gserviceaccount.com"
        }
        , scope)
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




