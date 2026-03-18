# 台灣銀行即時匯率爬蟲

抓取台灣銀行當天匯率並儲存為 CSV，並透過 Streamlit 發布展示。

## 專案結構

```
├── scraper.py       # 爬蟲：抓取台銀匯率並存 CSV
├── app.py           # Streamlit 應用程式
├── requirements.txt # 套件依賴
└── rates.csv        # 輸出的匯率資料（執行後產生）
```

## 安裝與執行

```bash
pip install -r requirements.txt

# 只抓資料存 CSV
python scraper.py

# 啟動 Streamlit
streamlit run app.py
```

## 部署到 Streamlit Cloud

1. 將此專案推送到 GitHub
2. 前往 [streamlit.io/cloud](https://streamlit.io/cloud)
3. 連結 GitHub repo，選擇 `app.py` 作為入口
4. 點擊 Deploy

## 資料來源

- [台灣銀行牌告匯率](https://rate.bot.com.tw/xrt?Lang=zh-TW)
