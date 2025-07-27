import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="💹 توصيات فوركس يومية", layout="wide")

# قائمة الأزواج
forex_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X",
               "USDCHF=X", "NZDUSD=X", "EURJPY=X", "GBPJPY=X", "EURGBP=X"]

# توليد التوصيات
def generate_signal(df):
    rsi = df.ta.rsi(length=14).iloc[-1]
    macd_hist = df.ta.macd().iloc[-1]['MACDh_12_26_9']
    ema20 = df.ta.ema(length=20).iloc[-1]
    ema50 = df.ta.ema(length=50).iloc[-1]
    price = df["Close"].iloc[-1]

    signal = "HOLD"
    reason = []
    if rsi < 30:
        signal = "BUY"
        reason.append("RSI Oversold")
    elif rsi > 70:
        signal = "SELL"
        reason.append("RSI Overbought")

    if ema20 > ema50:
        reason.append("EMA20 > EMA50 (Uptrend)")
    else:
        reason.append("EMA20 < EMA50 (Downtrend)")

    if macd_hist > 0:
        reason.append("MACD Histogram Positive")
    else:
        reason.append("MACD Histogram Negative")

    return signal, round(price, 5), ", ".join(reason)

# تحليل كل الأزواج
def create_recommendations():
    results = []
    for symbol in forex_pairs:
        df = yf.download(tickers=symbol, period="5d", interval="1h")
        if df.empty or len(df) < 50:
            continue
        signal, price, reason = generate_signal(df)
        results.append({
            "Pair": symbol.replace("=X", ""),
            "Signal": signal,
            "Price": price,
            "Reason": reason
        })
    return pd.DataFrame(results)

# واجهة Streamlit
st.title("📊 توصيات فوركس لحظية")
st.markdown("آخر تحديث: **" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "**")

if st.button("🔄 تحديث التوصيات"):
    df = create_recommendations()
    st.success("✅ تم تحديث التوصيات.")
    st.dataframe(df, use_container_width=True)
else:
    st.info("اضغط الزر بالأعلى لتوليد توصيات جديدة.")
  add forex agent script
