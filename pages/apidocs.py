import streamlit as st

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')
st.sidebar.page_link('pages/register.py', label='Register')
st.sidebar.page_link('pages/apidocs.py', label='API ที่ให้บริการ')

st.title("API ที่ให้บริการ")
st.info("⚙️ หน้านี้กำลังปรับปรุง...")
st.write("โปรดกลับมาอีกครั้งเร็ว ๆ นี้")
