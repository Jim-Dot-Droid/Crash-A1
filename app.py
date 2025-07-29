import streamlit as st
import pandas as pd
import numpy as np
from solana_client import fetch_latest_multipliers

st.set_page_config(page_title="Crash Predictor Pro", layout="centered")

st.title("Crash Game Predictor Pro – Live from Solana")
st.write("Live predictions using on-chain rounds from program DEALERKF...")

# Load live data
with st.spinner("Fetching live data from Solana..."):
    multipliers = fetch_latest_multipliers()

if multipliers:
    st.success(f"Fetched {len(multipliers)} live rounds.")
else:
    st.warning("No live data available. Try manual input below.")

# Predictor logic
def compute_confidence(data, threshold=2.0, trend_window=10):
    if not data:
        return 0.5, 0.5

    data = np.array(data)
    n = len(data)
    weights = np.linspace(0.3, 1.0, n)
    base_score = np.average((data > threshold).astype(int), weights=weights)

    recent = data[-trend_window:] if n >= trend_window else data
    trend_score = np.mean(recent > threshold)

    streak = 1
    for i in range(n - 2, -1, -1):
        if (data[i] > threshold) == (data[i + 1] > threshold):
            streak += 1
        else:
            break
    streak_impact = min(streak * 0.01, 0.1)
    streak_score = streak_impact if data[-1] <= threshold else -streak_impact

    combined = (0.6 * base_score) + (0.3 * trend_score) + (0.1 * (0.5 + streak_score))
    volatility = np.std(data)
    if volatility > 2:
        combined *= 0.9
    if n < 20:
        combined = 0.5 + (combined - 0.5) * 0.7

    combined = max(0, min(combined, 1))
    return combined, 1 - combined

# Prediction
if multipliers:
    above_conf, under_conf = compute_confidence(multipliers)
    st.subheader("Prediction")
    if above_conf > under_conf:
        st.success(f"Prediction: Above 200% ({above_conf:.1%} confidence)")
    else:
        st.error(f"Prediction: Under 200% ({under_conf:.1%} confidence)")

# Manual fallback
st.subheader("Manual Input")
manual_vals = st.text_area("Enter comma-separated multipliers (e.g., 1.8, 2.1, 1.3):")
if st.button("Use Manual Data"):
    try:
        data = list(map(float, manual_vals.split(',')))
        above_conf, under_conf = compute_confidence(data)
        st.info(f"Manual Prediction: {'Above' if above_conf > under_conf else 'Under'} 200%")
    except:
        st.error("Invalid input.")