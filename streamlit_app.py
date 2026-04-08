import streamlit as st
import pandas as pd

SAG_PERCENT = 30

# ===== 車種資料庫 =====
bike_data = {
    "Honda": {
        "X-ADV 750": {"front": 150, "rear": 150},
        "CBR1000RR": {"front": 120, "rear": 138},
    },
    "Yamaha": {
        "MT-09": {"front": 137, "rear": 130},
    }
}

def calc_sag(travel):
    return travel * SAG_PERCENT / 100

st.set_page_config(layout="wide")
st.title("🏍 SAG 專業調校工具")

# ===== 客戶資料 =====
st.subheader("📋 客戶資料")
name = st.text_input("客戶名稱", key="name")

# ===== 車種選單 =====
brand = st.selectbox("品牌", list(bike_data.keys()), key="brand")

model = st.selectbox(
    "車種",
    list(bike_data[brand].keys()),
    key="model"
)

# 自動帶入行程
front_travel = bike_data[brand][model]["front"]
rear_travel = bike_data[brand][model]["rear"]

st.markdown("---")

# ===== 顯示車輛數據（像圖片那樣）=====
col1, col2 = st.columns(2)

with col1:
    st.subheader("前叉 (FRONT)")
    st.metric("行程", f"{front_travel} mm")
    front_target = calc_sag(front_travel)
    st.metric("SAG 30%", f"{front_target:.0f} mm")

    front_actual = st.number_input("實際 SAG", key="f_actual")
    front_comp = st.number_input("壓縮", key="f_comp")
    front_reb = st.number_input("回彈", key="f_reb")

with col2:
    st.subheader("後避震 (REAR)")
    st.metric("行程", f"{rear_travel} mm")
    rear_target = calc_sag(rear_travel)
    st.metric("SAG 30%", f"{rear_target:.0f} mm")

    rear_actual = st.number_input("實際 SAG", key="r_actual")
    rear_comp = st.number_input("壓縮", key="r_comp")
    rear_reb = st.number_input("回彈", key="r_reb")

# ===== 分析 =====
if st.button("分析設定"):

    def check(actual, target):
        if actual < target:
            return "偏硬 🔴"
        elif actual > target:
            return "偏軟 🔵"
        else:
            return "OK ✅"

    st.markdown("---")
    st.subheader("📊 分析結果")

    st.write(f"客戶：{name} | 車種：{brand} {model}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("前避震")
        st.write(f"SAG: {front_actual} / {front_target:.0f} mm")
        st.write(check(front_actual, front_target))

    with col2:
        st.write("後避震")
        st.write(f"SAG: {rear_actual} / {rear_target:.0f} mm")
        st.write(check(rear_actual, rear_target))

    # ===== 記錄表 =====
    df = pd.DataFrame({
        "客戶": [name, name],
        "車種": [model, model],
        "部位": ["前", "後"],
        "行程": [front_travel, rear_travel],
        "目標SAG": [front_target, rear_target],
        "實際SAG": [front_actual, rear_actual],
        "壓縮": [front_comp, rear_comp],
        "回彈": [front_reb, rear_reb]
    })

    st.dataframe(df)
