import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def fetch_bot_rates():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table tbody tr")
    data = []
    for row in rows:
        cols = row.select("td")
        if len(cols) < 5:
            continue
        # col[0] 幣別文字因 RWD 設計重複，取前半段即可
        raw = cols[0].get_text(strip=True)
        currency = raw[: len(raw) // 2] if len(raw) % 2 == 0 and raw[: len(raw) // 2] == raw[len(raw) // 2 :] else raw
        buy_cash = cols[1].get_text(strip=True)
        sell_cash = cols[2].get_text(strip=True)
        buy_spot = cols[3].get_text(strip=True)
        sell_spot = cols[4].get_text(strip=True)
        data.append({
            "幣別": currency,
            "現金買入": buy_cash,
            "現金賣出": sell_cash,
            "即期買入": buy_spot,
            "即期賣出": sell_spot,
            "更新時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    return pd.DataFrame(data)


def save_to_csv(df, path="rates.csv"):
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"已儲存 {len(df)} 筆匯率資料至 {path}")


if __name__ == "__main__":
    df = fetch_bot_rates()
    save_to_csv(df)
    print(df.head())
