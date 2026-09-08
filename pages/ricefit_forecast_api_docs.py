import streamlit as st
import pandas as pd
import json
from utils import sidebar_options

st.set_page_config(
    page_title="RiceFit API – Forecast",
    layout="wide"
)

sidebar_options()

st.header("RiceFit API – พยากรณ์อากาศและความเสี่ยงข้าวรายวัน")
st.markdown(
    """
    ดึงข้อมูลสภาพอากาศย้อนหลัง (historic) และพยากรณ์ล่วงหน้า (forecast) จาก Open-Meteo ตามพิกัดที่ระบุ
    นำมารวมเป็นข้อมูลรายวัน แล้วคำนวณตัวนับความเสี่ยงของโรคข้าว (โรคไหม้ / โรคขอบใบแห้ง)
    และความเสี่ยงจากอุณหภูมิสูง–ต่ำในแต่ละระยะการเจริญเติบโตของข้าว
    เพื่อใช้เป็นข้อมูลสนับสนุนการแจ้งเตือนและพยากรณ์ความเสี่ยงข้าว (RiceFit)
    """
)

# --------------------------------------------------
# API Overview
# --------------------------------------------------
st.subheader("API Overview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Name**")
    st.code("Weather Forecast & Rice Risk")

    st.markdown("**Endpoint**")
    st.code("/ricefit_forecast")

with col2:
    st.markdown("**Method**")
    st.code("GET")

    st.markdown("**คำอธิบาย**")
    st.write(
        "พยากรณ์สภาพอากาศและความเสี่ยงโรค/อุณหภูมิสำหรับข้าวรายวัน"
    )

st.markdown("---")

# --------------------------------------------------
# Request
# --------------------------------------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Request Headers")

    df_headers = pd.DataFrame({
        "Header": ["accept", "apikey"],
        "Value": ["application/json", "{API Key}"],
        "Description": [
            "Response format",
            "API key for authentication"
        ]
    })

    st.dataframe(df_headers, hide_index=True, use_container_width=True)

    st.subheader("Query Parameters")

    df_params = pd.DataFrame({
        "Parameter": [
            "lat",
            "lon",
            "historic_days",
            "forecast_days"
        ],
        "Type": [
            "Float",
            "Float",
            "Int (optional, default=21)",
            "Int (optional, default=7)"
        ],
        "Description": [
            "ละติจูดของตำแหน่งที่ต้องการพยากรณ์อากาศ",
            "ลองจิจูดของตำแหน่งที่ต้องการพยากรณ์อากาศ",
            "จำนวนวันย้อนหลังจากวันนี้ที่ต้องการดึงข้อมูลสภาพอากาศจริง (1–60 วัน)",
            "จำนวนวันล่วงหน้าที่ต้องการพยากรณ์อากาศ (1–180 วัน)"
        ]
    })

    st.dataframe(df_params, hide_index=True, use_container_width=True)

    st.caption("ข้อมูลสภาพอากาศดึงจาก Open-Meteo (archive + forecast API) แล้วรวมเป็นรายวันฝั่งเซิร์ฟเวอร์")

    st.subheader("Response Codes")

    df_errors = pd.DataFrame({
        "Code": [400, 401, 404, 500],
        "Description": [
            "Bad Request – The server could not understand the request due to invalid syntax.",
            "Unauthorized – API key ไม่ถูกต้องหรือไม่ได้แนบมา",
            "Not Found – The server cannot find the requested resource.",
            "Internal Server Error – เกิดข้อผิดพลาดระหว่างประมวลผล เช่น ไม่สามารถดึงข้อมูลอากาศหรือคำนวณข้อมูลรายวันไม่สำเร็จ"
        ]
    })

    st.dataframe(df_errors, hide_index=True, use_container_width=True)

with col2:
    st.subheader("Example Request")

    st.code(
        """curl -X 'GET' \\
'http://10.228.8.25:5008/ricefit_forecast?lat=13.7563&lon=100.5018&historic_days=21&forecast_days=7' \\
-H 'accept: application/json'""",
        language="bash"
    )

    example_response = {
        "latitude": 13.7563,
        "longitude": 100.5018,
        "historic_days": 21,
        "records": [
            {
                "date": "2025-06-01",
                "temperature_2m_max": 34.2,
                "temperature_2m_min": 25.1,
                "precipitation": 12.4,
                "relativehumidity_2m": 82.0,
                "temperature_2m_avg": 29.65,
                "monthly_precipitation": 148.6,
                "cnt_blast_disease": 3,
                "cnt_blb_disease": 0,
                "cnt_lt_risk": 0,
                "cnt_ht_risk": 0,
                "cnt_sd_risk": 0,
                "cnt_gw1_risk": 0,
                "cnt_gw2_risk": 0,
                "cnt_flw_risk": 0,
                "cnt_hvs_risk": 0
            }
        ]
    }

    st.subheader("Example JSON Response")
    st.code(json.dumps(example_response, ensure_ascii=False, indent=2), language="json")

st.markdown("---")

# --------------------------------------------------
# Response Reference
# --------------------------------------------------
st.subheader("Response Reference")

df_response = pd.DataFrame({
    "ชื่อฟิลด์": [
        "latitude",
        "longitude",
        "historic_days",
        "records[].date",
        "records[].temperature_2m_max",
        "records[].temperature_2m_min",
        "records[].precipitation",
        "records[].relativehumidity_2m",
        "records[].temperature_2m_avg",
        "records[].monthly_precipitation",
        "records[].cnt_blast_disease",
        "records[].cnt_blb_disease",
        "records[].cnt_lt_risk",
        "records[].cnt_ht_risk",
        "records[].cnt_sd_risk",
        "records[].cnt_gw1_risk",
        "records[].cnt_gw2_risk",
        "records[].cnt_flw_risk",
        "records[].cnt_hvs_risk"
    ],
    "ชนิดข้อมูล": [
        "Float", "Float", "Int",
        "String (YYYY-MM-DD)", "Float", "Float", "Float", "Float", "Float", "Float",
        "Int", "Int", "Int",
        "Int (0 หรือ 1)", "Int (0 หรือ 1)", "Int (0 หรือ 1)", "Int (0 หรือ 1)", "Int (0 หรือ 1)", "Int (0 หรือ 1)"
    ],
    "คำอธิบาย": [
        "ละติจูดที่ร้องขอ",
        "ลองจิจูดที่ร้องขอ",
        "จำนวนวันย้อนหลังที่ใช้",
        "วันที่ของข้อมูล",
        "อุณหภูมิสูงสุดของวัน (°C)",
        "อุณหภูมิต่ำสุดของวัน (°C)",
        "ปริมาณฝนรวมของวัน (มม.)",
        "ความชื้นสัมพัทธ์เฉลี่ยของวัน (%)",
        "อุณหภูมิเฉลี่ยของวัน (°C) = (max+min)/2",
        "ปริมาณฝนรวมของทั้งเดือนที่วันนั้นสังกัดอยู่ (มม.)",
        "ตัวนับวันต่อเนื่องที่เข้าเงื่อนไขเสี่ยงโรคไหม้ (RH ≥ 85% และอุณหภูมิ > 25°C) — ดู หมายเหตุ ด้านล่าง",
        "ตัวนับวันต่อเนื่องที่เข้าเงื่อนไขเสี่ยงโรคขอบใบแห้ง (RH ≥ 80%, อุณหภูมิ > 25°C, ฝนรายเดือน ≥ 70มม.) — ดู หมายเหตุ ด้านล่าง",
        "ตัวนับวันต่อเนื่องที่อุณหภูมิต่ำสุด < 15°C (เสี่ยงข้าวเป็นหมันจากอากาศเย็น) — ดู หมายเหตุ ด้านล่าง",
        "เข้าเงื่อนไขอุณหภูมิสูง (max > 40°C) ในวันนั้นหรือไม่",
        "เสี่ยงต่อระยะกล้า (seedling): min < 16°C หรือ max > 40°C",
        "เสี่ยงต่อระยะเจริญเติบโตช่วงที่ 1: min < 9°C หรือ max > 35°C",
        "เสี่ยงต่อระยะเจริญเติบโตช่วงที่ 2: min < 12°C หรือ max > 35°C",
        "เสี่ยงต่อระยะออกดอก: min < 15°C หรือ max > 35°C",
        "เสี่ยงต่อระยะเก็บเกี่ยว: min < 12°C หรือ max > 30°C"
    ]
})

st.dataframe(
    df_response,
    hide_index=True,
    use_container_width=True,
    height=700
)

st.markdown(
    """
> **หมายเหตุ — พฤติกรรมตัวนับ (`cnt_blast_disease`, `cnt_blb_disease`, `cnt_lt_risk`)**
> ค่าเหล่านี้เป็น **ตัวนับสะสมข้ามวัน** ไม่ใช่ค่าอิสระต่อวัน (running counter):
> วันใดไม่เข้าเงื่อนไข ตัวนับจะ**รีเซ็ตเป็น 0 ทันที** และตัวนับจะ**รีเซ็ตเองเป็น 0** เมื่อนับครบ 7 วันติดต่อกัน
> (หรือ 6 วันสำหรับ `cnt_lt_risk`) ก่อนเริ่มนับใหม่ในรอบถัดไป แม้เงื่อนไขจะยังคงเป็นจริงต่อเนื่องก็ตาม
"""
)
