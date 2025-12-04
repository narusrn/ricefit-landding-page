import streamlit as st

import os

creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
st.write(creds)

st.set_page_config(page_title="Ricefit API (Home)", layout="wide")

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')

st.sidebar.page_link('pages/register.py', label='Register')

st.title("เริ่มต้นการใช้งาน Ricefit API")


st.markdown("""
เพื่อใช้งาน API จำเป็นต้องสมัครสมาชิกผ่านเว็บไซต์ของเรา  

- สมัครสมาชิก: https://.../register  

หลังจากสมัครสมาชิกเรียบร้อยแล้ว ระบบจะส่ง **OAuth Access Token** ให้ทางอีเมลของคุณ  
โปรดตรวจสอบอีเมลและเก็บ Token ไว้ให้ดี เพราะเป็นรหัสสำหรับเข้าถึง API ของคุณ  

### ตัวอย่างการเรียก API
```bash
curl -X GET \
'https://www.nectec.or.th/innovation/innovation-service/digital-agri-api' \
-H 'accept: application/json' \
-H 'authorization: Bearer <ACCESS_TOKEN>'
```

""")


