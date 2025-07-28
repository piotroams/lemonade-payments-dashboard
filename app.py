
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lemonade Payments Dashboard", layout="wide")

st.title("🍋 Lemonade - Apple Pay Authorization Dashboard")

# Load Apple Pay data files
apple_summary = pd.read_csv("apple_pay_summary.csv", index_col=0)
decline_reasons = pd.read_csv("apple_pay_top_decline_reasons.csv", index_col=0)
declines_by_processor = pd.read_csv("apple_pay_declines_by_processor.csv")
declines_by_attempt = pd.read_csv("apple_pay_declines_by_attempt.csv")

# Show summary rates
st.subheader("Authorization Rates")
st.dataframe(apple_summary.style.format({"Rate": "{:.2%}"}))

# Charts
st.subheader("Top 10 Decline Reasons")
st.bar_chart(decline_reasons)

st.subheader("Declines by Processor")
st.bar_chart(declines_by_processor.set_index('Processor'))

st.subheader("Declines by Attempt Number")
st.bar_chart(declines_by_attempt.set_index('Attempt Number'))

st.caption("Built for Lemonade case study | Powered by Streamlit")
