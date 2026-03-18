import streamlit as st
import pandas as pd
from scraper import fetch_bot_rates, save_to_csv
from datetime import datetime
import os

st.set_page_config(page_title="台灣銀行即時匯率", page_icon="💱", layout="wide")

st.title("💱 台灣銀行即時匯率")
st.caption("資料來源：台灣銀行 rate.bot.com.tw")

# 重新整理按鈕
if st.button("🔄 重新抓取最新匯率"):
    st.cache_data.clear()

@st.cache_data(ttl=600)
def load_data():
    df = fetch_bot_rates()
    save_to_csv(df)
    return df

with st.spinner("抓取匯率中..."):
    df = load_data()

if df.empty:
    st.error("無法取得匯率資料，請稍後再試。")
else:
    update_time = df["更新時間"].iloc[0]
    st.success(f"資料更新時間：{update_time}")

    # 搜尋欄位
    search = st.text_input("搜尋幣別（例如：美金、日圓）", "")
    if search:
        df_show = df[df["幣別"].str.contains(search, na=False)]
    else:
        df_show = df

    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # 下載 CSV
    csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="⬇️ 下載 CSV",
        data=csv_bytes,
        file_name=f"bot_rates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )
