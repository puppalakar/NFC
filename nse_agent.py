import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep
from typing import List, Dict

BASE = "https://www.nseindia.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nseindia.com/"
}

session = requests.Session()
session.headers.update(HEADERS)


def fetch_json(path: str) -> Dict:
    """Fetch NSE API JSON with cookie warmup."""
    session.get(BASE, timeout=10)
    response = session.get(BASE + path, timeout=10)
    response.raise_for_status()
    return response.json()


def get_nifty50() -> List[str]:
    j = fetch_json("/api/equity-stockIndices?index=NIFTY%2050")
    return [item["symbol"] for item in j.get("data", [])]


def get_quote(symbol: str) -> Dict:
    return fetch_json(f"/api/quote-equity?symbol={symbol}")


def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["RSI"] = compute_rsi(df["close"])
    df["MA20"] = df["close"].rolling(window=20).mean()
    df["MA50"] = df["close"].rolling(window=50).mean()
    return df


def signal_from_ohlc(df: pd.DataFrame) -> str:
    if len(df) < 2:
        return "hold"

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    buy_condition = prev["EMA20"] < prev["EMA50"] and latest["EMA20"] > latest["EMA50"] and latest["RSI"] < 70
    sell_condition = prev["EMA20"] > prev["EMA50"] and latest["EMA20"] < latest["EMA50"] and latest["RSI"] > 30

    if buy_condition:
        return "buy"
    if sell_condition:
        return "sell"
    return "hold"


def load_historical(symbol: str, start_days: int = 365) -> pd.DataFrame:
    days = start_days
    end = datetime.today()
    start = end - timedelta(days=days)
    endpoint = "/api/option-chain-indices?symbol=NIFTY" if symbol == "NIFTY" else f"/api/historical/cm/equity?symbol={symbol}&series=[\"EQ\"]&from={start.strftime('%d-%m-%Y')}&to={end.strftime('%d-%m-%Y')}"

    # fallback: NSE chain data endpoint may not be documented; user can adapt to valid endpoint
    r = session.get(BASE + endpoint, timeout=10)
    r.raise_for_status()

    # data parsing is endpoint-specific; this is a convenience stub for extension.
    return pd.DataFrame()


def analyze_symbols(symbols: List[str]) -> pd.DataFrame:
    results = []
    for sym in symbols:
        try:
            quote = get_quote(sym)
            info = quote.get("priceInfo", {})
            latest_price = info.get("lastPrice", None)
            results.append({"symbol": sym, "price": latest_price, "signal": "single-quote"})
            sleep(0.4)
        except Exception as ex:
            results.append({"symbol": sym, "price": None, "signal": f"error: {ex}"})
    return pd.DataFrame(results)


if __name__ == "__main__":
    symbols = get_nifty50()[:20]
    analysis = analyze_symbols(symbols)

    print("NSE stock scan (top 20 NIFTY50):")
    print(analysis.to_string(index=False))
    print("\nNote: this script is a baseline opportunity; integrate historical OHLC and compute full signals before live use.")
