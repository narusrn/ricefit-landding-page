import streamlit as st

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
