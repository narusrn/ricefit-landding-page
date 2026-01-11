import streamlit as st
import streamlit.components.v1 as components
from utils import sidebar_options 
# st.sidebar.page_link('app.py', label='Home')
sidebar_options()

st.markdown("""
<div style="text-align:center; margin-top: 120px;">
    <h2>API ที่ให้บริการ</h2>
    <a href="https://www.nectec.or.th/innovation/innovation-service/digital-agri-api/docs" target="_blank" rel="noopener noreferrer">ไปที่ RiceFit API Docs</a>
</div>

""", unsafe_allow_html=True)
