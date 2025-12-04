import streamlit as st

st.set_page_config(page_title="Ricefit API (Home)", layout="wide")

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')
st.sidebar.markdown("""
<style>
/* base style */
.sidebar-subitem {
    margin-left: 30px;
    font-size: 14px;
    display: block;
    
    padding: 4px 0;
    text-decoration: none !important;
}

/* hover = ฟ้า */
.sidebar-subitem:hover {
    color: #1a73e8 ;
    text-decoration: none !important;
}

/* active (คลิกขณะกด) */
.sidebar-subitem:active {
    color: #1a73e8 ;
}

}
</style>

<a class="sidebar-subitem" href="#การสมัครการใช้งาน">การสมัครการใช้งาน</a>
<a class="sidebar-subitem" href="#การยืนยันสิทธิ์การใช้งาน">การยืนยันสิทธิ์การใช้งาน</a>
""", unsafe_allow_html=True)

st.sidebar.page_link('pages/register.py', label='Register')
st.sidebar.page_link('pages/apidocs.py', label='API ที่ให้บริการ')

# st.sidebar.title("เริ่มต้นการใช้งาน Ricefit API")

# st.sidebar.markdown("""
# - [การสมัครการใช้งาน](#การสมัครการใช้งาน)
# - [การยืนยันสิทธิ์การใช้งาน](#การยืนยันสิทธิ์การใช้งาน)
# """)


st.header("เริ่มต้นการใช้งาน Ricefit API")

st.markdown("""
ในการใช้งานข้อมูล Ricefit ผ่านระบบ API จะต้องทำการสมัครใช้งานก่อน และส่งข้อมูลยืนยันตัวตนทุกครั้งที่เรียกการใช้งาน API

ระบบยืนยันตัวตนของ API ใช้ตามมาตรฐาน OAuth 2.0 โดยรองรับวิธีการขอ Access Token ผ่านทางเว็บไซต์บริการข้อมูล RiceFit API เท่านั้น ซึ่งนักพัฒนาต้องทำตามขั้นตอนการสมัครและใช้งาน ดังนี้
""")

st.header("การสมัครการใช้งาน", anchor="การสมัครการใช้งาน")

st.markdown("""

ผู้ใช้งานทั่วไปและนักพัฒนาสามารถสมัครใช้บริการข้อมูล Ricefit API ได้ที่เว็บไซต์ https://ricefit-landding-page-wcbsvzpxrxwy5atzdeuxdf.streamlit.app/register

เมื่อเข้าสู่เว็บไซต์แล้ว กรอกข้อมูลส่วนตัวเพื่อใช้ในการยืนยันตัวตน และวัตถุประสงค์ในสมัครเข้าใช้งาน

""")

st.image("assets/register-from.png")

st.markdown("""

หลังจากสมัครสมาชิกเรียบร้อยแล้ว ระบบจะส่ง **OAuth Access Token** ให้ทางอีเมลของคุณ  
โปรดตรวจสอบอีเมลและเก็บ Token ไว้ให้ดี เพราะเป็นรหัสสำหรับเข้าถึง API ของคุณ  

""")

st.header("การยืนยันสิทธิ์การใช้งาน", anchor="การยืนยันสิทธิ์การใช้งาน")

col1, col2 = st.columns([1, 1])   # ซ้ายกว้างกว่าขวาเล็กน้อย

with col1:
    st.markdown("""
    ในการเรียกใช้ API ที่เปิดให้บริการทุกครั้ง ผู้ใช้จะต้องมีการยืนยันสิทธิ์ (Authentication) ด้วย OAuth Access Token ของผู้ใช้ที่ได้สร้างขึ้นไว้บนเว็บไซต์ แนบเข้ามากับ Header ของ HTTP Request บน parameter "authorization" ก่อนส่งเข้ามายัง URL ของ API นั้น

    ---
                
    ✅  หากยืนยันตัวตนสำเร็จและสามารถเรียกข้อมูลได้สำเร็จ API จะส่งกลับข้อมูลพร้อมด้วย HTTP status code 200 (OK)
                
    ---
    
    ❌  หากไม่มีการส่ง OAuth access token หรือยืนยันตัวตนไม่สำเร็จ API จะส่งกลับ Error message พร้อมด้วย HTTP status code 401 (Unauthorized)
    
    """)

with col2:
    st.code("""
    curl -I -X GET \\
    'https://www.nectec.or.th/innovation/innovation-service/digital-agri-api/ricefit' \\
    -H 'accept: application/json' \\
    -H 'authorization: Bearer bIBlfvqQqS2lLPWZ... <- access token'
    """, language="bash")

    st.code("""
    HTTP/1.1 200 OK
    Server: nginx/1.10.2
    Content-Type: application/json
    Transfer-Encoding: chunked
    Connection: keep-alive
    X-Powered-By: PHP/7.1.8
    Cache-Control: no-cache, private
    Date: Sun, 27 Aug 2017 12:06:57 GMT
    X-RateLimit-Limit: 60
    X-RateLimit-Remaining: 59
    X-Datapoint-Limit: 100000
    X-Datapoint-Remaining: 997562
    """, language="bash")

# ### ตัวอย่างการเรียก API
# ```bash
# curl -X GET \
# 'https://www.nectec.or.th/innovation/innovation-service/digital-agri-api' \
# -H 'accept: application/json' \
# -H 'authorization: Bearer <ACCESS_TOKEN>'
# ```






























