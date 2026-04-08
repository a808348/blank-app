import streamlit as st
import pandas as pd
from io import BytesIO

SAG_PERCENT = 30  # 固定 30%

# 計算理想 SAG
def calculate_sag(travel_mm):
    return travel_mm * SAG_PERCENT / 100

# 判斷狀態
def get_status(actual, target):
    if actual < target:
        return "偏硬 (SAG 太小) 🔴", "red"
    elif actual > target:
        return "偏軟 (SAG 太大) 🔵", "blue"
    else:
        return "正確 ✅", "green"



st.set_page_config(page_title="專業 SAG 工具", layout="wide")

st.title("🏍專業避震調校工具")
st.markdown("---")

# 客戶資料
st.subheader("📋 客戶資料")
customer_name = st.text_input("客戶名稱", key="customer_name")
bike_model = st.text_input("車種", key="bike_model")

# 騎士體重
weight = st.number_input("騎士體重(含裝備 kg)", min_value=0.0, max_value=150.0, value=0.0, step=1.0, key="weight")

st.markdown("## 前後避震設定")
col1, col2 = st.columns(2)

with col1:
    st.subheader("前避震")
    front_travel = st.number_input("行程 (mm)", min_value=0.0, max_value=300.0, value=0.0, key="front_travel")
    front_actual = st.number_input("實際下沉 (mm)", min_value=0.0, max_value=300.0, value=0.0, key="front_actual")
    front_compression = st.number_input("壓縮阻尼設定", min_value=0, max_value=100, value=0, key="front_compression")
    front_rebound = st.number_input("回彈阻尼設定", min_value=0, max_value=100, value=0, key="front_rebound")

with col2:
    st.subheader("後避震")
    rear_travel = st.number_input("行程 (mm)", min_value=0.0, max_value=300.0, value=0.0, key="rear_travel")
    rear_actual = st.number_input("實際下沉 (mm)", min_value=0.0, max_value=300.0, value=0.0, key="rear_actual")
    rear_compression = st.number_input("壓縮阻尼設定", min_value=0, max_value=100, value=0, key="rear_compression")
    rear_rebound = st.number_input("回彈阻尼設定", min_value=0, max_value=100, value=0, key="rear_rebound")

if st.button("計算 SAG", key="calculate_sag"):
    # 計算目標
    front_target = calculate_sag(front_travel)
    rear_target = calculate_sag(rear_travel)

    # 前後狀態
    front_status, front_color = get_status(front_actual, front_target)
    rear_status, rear_color = get_status(rear_actual, rear_target)

    # 體重建議
    if weight < 65:
        weight_hint = "體重偏輕：原廠通常偏硬，可能需更軟彈簧或降低 preload"
    elif weight > 85:
        weight_hint = "體重偏重：原廠可能偏軟，可能需增加 preload 或換硬彈簧"
    else:
        weight_hint = "體重正常範圍：原廠通常可調整到位"

    # 顯示結果
    st.markdown("---")
    st.subheader("📊 計算結果")
    st.markdown(f"**客戶：** {customer_name}  |  **車種：** {bike_model}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### 前避震")
        st.markdown(f"- 理想 SAG (30%): **{front_target:.1f} mm**")
        st.markdown(f"- 實際 SAG: **{front_actual:.1f} mm**")
        st.markdown(f"- 狀態: **{front_status}**")
        st.progress(min(front_actual / front_travel, 1.0))

    with col2:
        st.markdown(f"### 後避震")
        st.markdown(f"- 理想 SAG (30%): **{rear_target:.1f} mm**")
        st.markdown(f"- 實際 SAG: **{rear_actual:.1f} mm**")
        st.markdown(f"- 狀態: **{rear_status}**")
        st.progress(min(rear_actual / rear_travel, 1.0))

    st.markdown("---")
    st.subheader("⚙️ 體重建議")
    st.markdown(weight_hint)

    st.markdown("### 🔧 調整建議")
    st.markdown("1️⃣ 調整 preload 讓 SAG 接近理想值")
    st.markdown("2️⃣ 調整阻尼（回彈 / 壓縮）")
    st.markdown("3️⃣ 如果調不到 → 考慮更換彈簧")

    # 壓縮 / 回彈紀錄表
    st.subheader("📝 壓縮 / 回彈設定表")
    record_data = {
        "客戶名稱": [customer_name]*2,
        "車種": [bike_model]*2,
        "部位": ["前避震", "後避震"],
        "行程(mm)": [front_travel, rear_travel],
        "實際SAG(mm)": [front_actual, rear_actual],
        "理想SAG(mm)": [front_target, rear_target],
        "壓縮設定": [front_compression, rear_compression],
        "回彈設定": [front_rebound, rear_rebound],
        "狀態": [front_status, rear_status]
    }
    df = pd.DataFrame(record_data)
    st.dataframe(df)
