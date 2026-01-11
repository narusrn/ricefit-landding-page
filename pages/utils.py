import streamlit as st
def sidebar_options():
  st.sidebar.page_link('pages/getting_started.py', label='Getting Started')
  st.sidebar.page_link('pages/register.py', label='Register')
  st.sidebar.page_link('pages/apidocs.py', label='API ที่ให้บริการ')
  st.sidebar.page_link(
      'pages/rice_phenotype_api_docs.py',
      label='API ลักษณะพันธุ์ข้าว (Rice Phenotype)'
  )
