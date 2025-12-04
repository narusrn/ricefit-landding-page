import streamlit as st
import streamlit.components.v1 as components

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')
st.sidebar.page_link('pages/register.py', label='Register')
st.sidebar.page_link('pages/apidocs.py', label='API ที่ให้บริการ')

st.markdown("""
<div style="text-align:center; margin-top: 120px;">
    <h2>API ที่ให้บริการ</h2>
    # <p style="font-size: 18px; color: gray;">⚙️ หน้านี้กำลังปรับปรุง...</p>
    # <p>โปรดกลับมาอีกครั้งเร็ว ๆ นี้</p>
    <a href="https://www.nectec.or.th/innovation/innovation-service/digital-agri-api/docs" target="_blank" rel="noopener noreferrer">เปิด RiceFit API Docs</a>
</div>

""", unsafe_allow_html=True)
