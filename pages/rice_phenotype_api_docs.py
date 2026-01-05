import streamlit as st

st.set_page_config(
    page_title="RiceFit API – Phenotype",
    layout="wide"
)

st.title("🌾 RiceFit API – Phenotype")
st.markdown(
    """
    This page documents the **Rice Phenotype API**, which provides detailed
    information about rice varieties, including cultivation characteristics,
    stress tolerance, and disease resistance.
    """
)

# --------------------------------------------------
# API Overview
# --------------------------------------------------
st.header("📌 API Overview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Name**")
    st.code("Rice Variety Information")

    st.markdown("**Endpoint**")
    st.code("/rice/phenotype")

with col2:
    st.markdown("**Method**")
    st.code("GET")

    st.markdown("**Description**")
    st.write(
        "Retrieves rice variety information. "
        "If no rice variety is specified, the service returns all available varieties."
    )

# --------------------------------------------------
# Headers
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

st.table({
    "Parameter": ["rice_variety"],
    "Type": ["String (optional)"],
    "Description": [
        "Name of the rice variety (e.g. กข53). "
        "If omitted, all rice varieties will be returned."
    ]
})

# --------------------------------------------------
# Example Request
# --------------------------------------------------
st.header("📡 Example Request (curl)")

st.code(
    """curl -X 'GET' \\
  'http://10.228.8.25:5008/rice/phenotype?rice_variety=กข53' \\
  -H 'accept: application/json'""",
    language="bash"
)

# --------------------------------------------------
# Example Response
# --------------------------------------------------
st.header("📦 Example Response (200 OK)")

example_response = {
    "result": [
        {
            "rice_variety": "กข53",
            "category": "พันธุ์รับรอง กรมการข้าว",
            "rice_type": "ข้าวเจ้า",
            "cultivation": "นาสวน",
            "sensitivity": "ไม่ไวแสง",
            "aroma": "ไม่หอม",
            "planting_month": 1,
            "harvest_month": 12,
            "salinity_tolerance": 1,
            "flood_tolerance": 3,
            "high_temp_sensitivity_grain_loss": 4,
            "low_temp_sensitivity_grain_loss": 2,
            "acidity_tolerance": 5,
            "blast_resistance": 2,
            "bacterial_leaf_blight_resistance": 5,
            "seedling_stage_low_temp_tolerance": 4
        }
    ]
}

st.json(example_response)

# --------------------------------------------------
# Field Reference
# --------------------------------------------------
st.header("📚 Response Field Reference")

st.subheader("General Information")
st.markdown(
    """
    - **rice_variety**: Rice variety name  
    - **category**: Rice classification (พันธุ์รับรอง / พันธุ์พื้นเมือง / พันธุ์ปรับปรุง)  
    - **rice_type**: Rice type (ข้าวเจ้า / ข้าวเหนียว)  
    - **cultivation**: Cultivation ecosystem (นาสวน / ข้าวขึ้นน้ำ / ข้าวไร่ / น้ำลึก)  
    - **sensitivity**: Photoperiod sensitivity (ไวแสง / ไม่ไวแสง)  
    - **aroma**: Aroma characteristic (หอม / ไม่หอม)  
    """
)

st.subheader("Planting & Harvest")
st.markdown(
    """
    - **planting_month**: Planting month (1–12)  
    - **harvest_month**: Harvest month (1–12)  
    """
)

st.subheader("Tolerance & Resistance Scores")
st.markdown(
    """
    **Scale varies by factor:**

    - **salinity_tolerance**: 1 (Low) – 4 (High)  
    - **flood_tolerance**: 1 (Low) – 3 (High)  
    - **seedling_stage_low_temp_tolerance**: 1 (Low) – 4 (Very High)  

    **Disease & Stress Sensitivity (1–5):**  
    1 = Low | 2 = Slight | 3 = Moderate | 4 = High | 5 = Very High

    - **high_temp_sensitivity_grain_loss**  
    - **low_temp_sensitivity_grain_loss**  
    - **acidity_tolerance**  
    - **blast_resistance**  
    - **bacterial_leaf_blight_resistance**
    """
)

# --------------------------------------------------
# Notes
# --------------------------------------------------
st.header("📝 Notes")

st.markdown(
    """
    - The API supports querying a **single rice variety** or **all varieties**.
