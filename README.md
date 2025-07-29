# Crash Predictor Pro (Live Solana Version)

This app fetches live crash multipliers from the Solana blockchain using the crash game program `DEALERKFspSo5RoXNnKAhRPhTcvJeqeEgAgZsNSjCx5E`. It runs a predictor using trend, streak, and volatility logic.

## 🛠 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Optionally, edit RPCs in `solana_client.py` to use a private endpoint.

## 🔄 Features
- Live Solana RPC fetch
- Confidence calculation (Above/Under 2x)
- Manual fallback entry

---
Created with ❤️ by ChatGPT