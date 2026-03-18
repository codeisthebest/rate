import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


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
        currency = cols[0].get_text(strip=True)
        cash_buy = cols[2].get_text(strip=True)
        cash_sell = cols[3].get_text(strip=True)
        spot_buy = cols[4].get_text(strip=True)
        spot_sell = cols[5].get_text(strip=True)
        rows.append({
            "幣別": currency,
            "現金買入": cash_buy,
            "現金賣出": cash_sell,
            "即期買入": spot_buy,
            "即期賣出": spot_sell,
        })

    df = pd.DataFrame(rows)
    return df


def main():
    print(f"台灣銀行匯率查詢 － {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    df = fetch_bot_rates()
    print(df.to_string(index=False))

    # 儲存為 CSV
    filename = f"bot_rates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\n已儲存至 {filename}")


if __name__ == "__main__":
    main()
