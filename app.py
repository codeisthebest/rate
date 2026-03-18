import requests
import pandas as pd
from datetime import datetime
from io import StringIO
import streamlit as st


def fetch_bot_rates():
    # 台銀官方 CSV API（比 HTML 解析穩定）
    url = "https://rate.bot.com.tw/xrt/flcsv/0/day"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.encoding = "utf-8"

    df = pd.read_csv(StringIO(response.text), header=1)

    # 只保留需要的欄位
    df = df.iloc[:, :6]
    df.columns = ["幣別", "幣別代碼", "現金買入", "現金賣出", "即期買入", "即期賣出"]
    df = df.dropna(subset=["幣別"]).reset_index(drop=True)

    return df


# ── 頁面設定 ──────────────────────────────────────────────
st.set_page_config(page_title="台銀匯率", page_icon="💱", layout="wide")
st.title("💱 台灣銀行牌告匯率")
st.caption(f"資料來源：台灣銀行｜更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ── 載入資料 ──────────────────────────────────────────────
with st.spinner("抓取匯率中..."):
    try:
        df = fetch_bot_rates()
    except Exception as e:
        st.error(f"資料抓取失敗：{e}")
        st.stop()

# ── 搜尋過濾 ──────────────────────────────────────────────
keyword = st.text_input("搜尋幣別", placeholder="例如：美金、日圓、USD")
if keyword:
    mask = (
        df["幣別"].str.contains(keyword, case=False, na=False) |
        df["幣別代碼"].str.contains(keyword, case=False, na=False)
    )
    df = df[mask]

# ── 顯示表格 ──────────────────────────────────────────────
st.dataframe(df, use_container_width=True, hide_index=True)

# ── 下載按鈕 ──────────────────────────────────────────────
csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
st.download_button(
    label="⬇ 下載 CSV",
    data=csv,
    file_name=f"bot_rates_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)

if st.button("🔄 重新整理"):
    st.rerun()
