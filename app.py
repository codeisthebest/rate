import requests
import pandas as pd
from io import StringIO
from datetime import datetime
import streamlit as st


def fetch_bot_rates():
    url = "https://rate.bot.com.tw/xrt/flcsv/0/day"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers, timeout=15)
    response.encoding = "utf-8-sig"  # 去除 BOM

    df = pd.read_csv(StringIO(response.text), header=0, index_col=0)
    # 欄位結構：現金買入=col2, 即期買入=col3, 現金賣出=col12, 即期賣出=col13

    result = pd.DataFrame({
        "幣別代碼": df.index,
        "現金買入": df.iloc[:, 1].values,
        "即期買入": df.iloc[:, 2].values,
        "現金賣出": df.iloc[:, 11].values,
        "即期賣出": df.iloc[:, 12].values,
    })
    result = result[result["幣別代碼"].notna()].reset_index(drop=True)
    return result


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
        st.exception(e)
        st.stop()

# ── 搜尋過濾 ──────────────────────────────────────────────
keyword = st.text_input("搜尋幣別代碼", placeholder="例如：USD、JPY、EUR")
if keyword:
    df = df[df["幣別代碼"].str.contains(keyword.upper(), na=False)]

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
