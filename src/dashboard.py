# dashboard.py — run with: streamlit run src/dashboard.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "activity_logs.csv")

st.set_page_config(page_title="FocusFlow Dashboard", layout="wide")

st.title("FocusFlow AI — Dashboard")

if os.path.exists(LOG_PATH):
    df = pd.read_csv(LOG_PATH)
    st.subheader("Recent activity (last 200 rows)")
    st.dataframe(df.tail(200))
    # compute simple metrics
    st.subheader("Metrics")
    if not df.empty:
        # approximate "focused" rows where active_app in focus apps
        focus_apps = ["VSCode", "PyCharm", "LibreOffice"]
        df['is_focus'] = df['active_app'].apply(lambda x: 1 if any(f in str(x) for f in focus_apps) else 0)
        focus_pct = df['is_focus'].mean() * 100
        st.metric("Focus % (logged)", f"{focus_pct:.1f}%")
        st.line_chart(df['is_focus'].rolling(20).mean())
else:
    st.info("No logs yet. Run the activity monitor to create data.")
