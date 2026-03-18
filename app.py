import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import streamlit as st


def fetch_bot_rates():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"title": "牌告匯率"})

    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cols = tr.find_all("td")
        if len(cols) < 7:
            continue
        rows.append({
            "幣別": cols[0].get_text(strip=True),
            "現金買入": cols[2].get_text(strip=True),
            "現金賣出": cols[3].get_text(strip=True),
            "即期買入": cols[4].get_text(strip=True),
            "即期賣出": cols[5].get_text(strip=True),
        })

    return pd.DataFrame(rows)


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
keyword = st.text_input("搜尋幣別", placeholder="例如：美金、日圓、EUR")
if keyword:
    df = df[df["幣別"].str.contains(keyword, case=False, na=False)]

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
