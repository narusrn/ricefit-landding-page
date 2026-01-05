import streamlit as st
import json

st.set_page_config(
    page_title="RiceFit API – Prediction",
    layout="wide"
)

st.title("🌾 RiceFit API – Prediction")
st.markdown(
    """
    This page provides detailed documentation for the **RiceFit Prediction API**,  
    which analyzes environmental and phenotypic data to assess rice cultivation risks
    and recommends suitable rice varieties for a given location.
    """
)

# --------------------------------------------------
# Basic API Info
# --------------------------------------------------
st.header("📌 API Overview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Name**")
    st.code("Prediction Ricefit")

    st.markdown("**Endpoint**")
    st.code("/ricefit")

with col2:
    st.markdown("**Method**")
    st.code("GET")

    st.markdown("**Description**")
    st.write(
        "Analyzes environmental and phenotypic data of rice to assess area-specific risks "
        "and recommends suitable rice varieties."
    )

# --------------------------------------------------
# Header
# --------------------------------------------------
st.header("🔐 Request Headers")

st.table({
    "Header": ["accept", "apikey"],
    "Value": ["application/json", "{API Key}"],
    "Description": [
        "Response format",
        "API key for authentication"
    ]
})

# --------------------------------------------------
# Query Parameters
# --------------------------------------------------
st.header("🧾 Query Parameters")

st.markdown(
    """
    Parameters are passed via **query string**.
    Some parameters (e.g. `factors`) can be repeated.
    """
)

st.table({
    "Parameter": [
        "factors", "lat", "lon", "rice_variety",
        "sensitivity", "month", "start_date"
    ],
    "Type": [
        "String (multiple)", "Float", "Float", "String",
        "String", "Integer", "Date"
    ],
    "Description": [
        "Environmental or stress factors (Thai), e.g. ดินเค็ม, น้ำท่วมฉับพลัน",
        "Latitude of location (e.g. 13.7563)",
        "Longitude of location (e.g. 100.5018)",
        "Rice variety name (e.g. กข53)",
        "Photoperiod sensitivity: ไวแสง / ไม่ไวแสง",
        "Target month (1–12)",
        "Planting start date (YYYY-MM-DD)"
    ]
})

# --------------------------------------------------
# Example Request
# --------------------------------------------------
st.header("📡 Example Request (curl)")

st.code(
    """curl -X 'GET' \\
  'http://10.228.8.25:5008/ricefit?factors=ดินเค็ม&factors=น้ำท่วมฉับพลัน&lat=13.7563&lon=100.5018&rice_variety=กข53&sensitivity=ไวแสง&month=7&start_date=2025-06-01' \\
  -H 'accept: application/json'""",
    language="bash"
)

# --------------------------------------------------
# Example Response
# --------------------------------------------------
st.header("📦 Example Response (200 OK)")

example_response = {
    "ข้อมูลดิน": [
        {
            "คำอธิบายเนื้อดิน": "-",
            "อินทรียวัตถุ": "ต่ำมาก",
            "ปฏิกิริยาดิน": "เป็นกรดรุนแรงมากที่สุด",
            "ปริมาณฟอสฟอรัส": "ต่ำมาก",
            "ปริมาณโพแทสเซียม": "ต่ำมาก",
            "ความจุแคตไอออน ": "ต่ำมาก",
            "ค่าการนำไฟฟ้าของดิน": "ไม่เค็ม"
        }
    ],
    "ระดับความเสี่ยง": [
        {
            "ดินเปรี้ยว": 1,
            "โรคขอบใบแห้ง": 1,
            "โรคใบไหม้": 1,
            "แล้ง": 3.09,
            "อุณหภูมิสูง": 1,
            "อุณหภูมิต่ำ": 1,
            "อุณหภูมิระยะเมล็ด": 1,
            "ดินเค็ม": 1,
            "ระยะข้าว": 4
        }
    ],
    "พันธุ์ข้าวแนะนํา": [
        {
            "rice_variety": "หอมชลสิทธิ์",
            "cultivation": "นาสวน",
            "sensitivity": "ไม่ไวแสง",
            "aroma": "หอม"
        }
    ]
}

st.json(example_response)

# --------------------------------------------------
# Response Field Reference
# --------------------------------------------------
st.header("📚 Response Field Reference")

st.subheader("Soil Information")
st.markdown(
    """
    - **คำอธิบายเนื้อดิน**: Soil texture description  
    - **ปฏิกิริยาดิน**: Soil pH / chemical reaction  
    - **ปริมาณฟอสฟอรัส**: Phosphorus level  
    - **ปริมาณโพแทสเซียม**: Potassium level  
    - **ความจุแคตไอออน**: CEC (Cation Exchange Capacity)  
    - **ค่าการนำไฟฟ้าของดิน**: Electrical conductivity (salinity)
    """
)

st.subheader("Risk Levels")
st.markdown(
    """
    All risk levels use the same scale:

    **1 = Low | 2 = Slight | 3 = Moderate | 4 = High | 5 = Very High**
    """
)

st.subheader("Rice Variety Recommendation")
st.markdown(
    """
    - **rice_variety**: Rice variety name  
    - **cultivation**: Ecosystem (นาสวน / ข้าวขึ้นน้ำ / ข้าวไร่ / น้ำลึก)  
    - **sensitivity**: Photoperiod sensitivity  
    - **aroma**: Aroma characteristic
    """
)

# --------------------------------------------------
# Error Codes
# --------------------------------------------------
st.header("⚠️ Error Codes")

st.table({
    "HTTP Code": ["400", "401", "404", "500"],
    "Description": [
        "Bad Request – Invalid request syntax",
        "Unauthorized – Authentication required",
        "Not Found – Resource not found",
        "Internal Server Error – Server-side failure"
    ]
})

st.divider()
st.caption("RiceFit API Documentation | Streamlit Viewer")
