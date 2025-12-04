import streamlit as st

st.set_page_config(page_title="Ricefit API (Home)", layout="wide")

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')

st.sidebar.page_link('pages/register.py', label='Register')

st.title("เริ่มต้นการใช้งาน Ricefit API")

st.markdown("""
ในการใช้งานข้อมูล ... ผ่านระบบ API จะต้องทำการสมัครใช้งานก่อน และส่งข้อมูลยืนยันตัวตนทุกครั้งที่เรียกการใช้งาน API

ระบบยืนยันตัวตนของ API ใช้ตามมาตรฐาน OAuth 2.0 โดยรองรับวิธีการขอ Access Token ผ่านทางเว็บไซต์บริการข้อมูล RiceFit API เท่านั้น ซึ่งนักพัฒนาต้องทำตามขั้นตอนการสมัครและใช้งาน ดังนี้
""")

st.title("การสมัครการใช้งาน")

st.markdown("""

ผู้ใช้งานทั่วไปและนักพัฒนาสามารถสมัครใช้บริการข้อมูล Ricefit API ได้ที่เว็บไซต์ https://ricefit-landding-page-wcbsvzpxrxwy5atzdeuxdf.streamlit.app/register

เมื่อเข้าสู่เว็บไซต์แล้ว กรอกข้อมูลส่วนตัวเพื่อใช้ในการยืนยันตัวตน และวัตถุประสงค์ในสมัครเข้าใช้งาน

""")

st.image("assets/register.png", use_column_width=True)

st.markdown("""

หลังจากสมัครสมาชิกเรียบร้อยแล้ว ระบบจะส่ง **OAuth Access Token** ให้ทางอีเมลของคุณ  
โปรดตรวจสอบอีเมลและเก็บ Token ไว้ให้ดี เพราะเป็นรหัสสำหรับเข้าถึง API ของคุณ  


""")

# ### ตัวอย่างการเรียก API
# ```bash
# curl -X GET \
# 'https://www.nectec.or.th/innovation/innovation-service/digital-agri-api' \
# -H 'accept: application/json' \
# -H 'authorization: Bearer <ACCESS_TOKEN>'
# ```










