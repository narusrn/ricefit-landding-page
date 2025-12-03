import streamlit as st
st.set_page_config(page_title="Ricefit API", layout="wide")

# st.sidebar.page_link('app.py', label='Home')
st.sidebar.page_link('pages/getting_started.py', label='Getting Started')

st.sidebar.page_link('pages/register.py', label='Register')

# Redirect to Getting Start page
st.switch_page("pages/getting_started.py")
