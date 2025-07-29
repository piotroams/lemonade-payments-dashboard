
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Apple Pay Dashboard", layout="wide")
st.title("🍎 Apple Pay Performance Dashboard")

apple_df = pd.read_csv("apple_pay_only_dataset.csv")

# KPIs
st.subheader("Authorization Rates (Apple Pay)")
txn_auth = (apple_df['TRANSACTION_STATUS'] == 'success').mean()
invoice_auth = apple_df.groupby('INVOICE_PUBLIC_ID')['TRANSACTION_STATUS'].apply(lambda x: 'success' in x.values).mean()
user_auth = apple_df.groupby('USER_PUBLIC_ID')['TRANSACTION_STATUS'].apply(lambda x: 'success' in x.values).mean()
kpi_df = pd.DataFrame({
    "Level": ["Transaction", "Invoice", "User"],
    "Authorization Rate": [txn_auth, invoice_auth, user_auth]
})
st.dataframe(kpi_df.set_index("Level").style.format("{:.2%}"))

# Daily trend
st.subheader("Daily Transaction Status Trend")
daily_trend = pd.read_csv("apple_pay_daily_trend.csv", index_col=0)
daily_trend = daily_trend[["success", "refused", "error"]] if "error" in daily_trend.columns else daily_trend
st.line_chart(daily_trend)

# Auth rate by brand
st.subheader("Authorization Rate by Card Brand")
brand = (
    apple_df.groupby("CREDIT_CARD_BRAND")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(brand)

# Auth rate by subscription interval
st.subheader("Authorization Rate by Subscription Interval")
interval = (
    apple_df.groupby("SUBSCRIPTION_INTERVAL")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(interval)

# Retry success rate
st.subheader("Retry Success Rate by Processor")
retry = (
    apple_df[apple_df["ATTEMPT_NUMBER"] > 1]
    .groupby("PROCESSOR")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(retry)

# Split heatmaps
st.subheader("🔹 Top Decline Reasons – First Attempt")
top_first = (
    apple_df[(apple_df["TRANSACTION_STATUS"] == "refused") & (apple_df["ATTEMPT_NUMBER"] == 1)]
    .groupby("ERROR_MESSAGE").size().sort_values(ascending=False).head(15).index
)
heatmap_first = (
    apple_df[
        (apple_df["TRANSACTION_STATUS"] == "refused") &
        (apple_df["ATTEMPT_NUMBER"] == 1) &
        (apple_df["ERROR_MESSAGE"].isin(top_first))
    ]
    .groupby(["ERROR_MESSAGE", "ATTEMPT_NUMBER"]).size()
    .unstack(fill_value=0)
)
fig1, ax1 = plt.subplots(figsize=(10, 8))
sns.heatmap(heatmap_first, cmap="Reds", linewidths=0.5, annot=True, fmt='d', ax=ax1)
st.pyplot(fig1)

st.subheader("🔸 Top Decline Reasons – Retry Attempts")
top_retry = (
    apple_df[(apple_df["TRANSACTION_STATUS"] == "refused") & (apple_df["ATTEMPT_NUMBER"] > 1)]
    .groupby("ERROR_MESSAGE").size().sort_values(ascending=False).head(15).index
)
heatmap_retry = (
    apple_df[
        (apple_df["TRANSACTION_STATUS"] == "refused") &
        (apple_df["ATTEMPT_NUMBER"] > 1) &
        (apple_df["ERROR_MESSAGE"].isin(top_retry))
    ]
    .groupby(["ERROR_MESSAGE", "ATTEMPT_NUMBER"]).size()
    .unstack(fill_value=0)
)
fig2, ax2 = plt.subplots(figsize=(10, 8))
sns.heatmap(heatmap_retry, cmap="Oranges", linewidths=0.5, annot=True, fmt='d', ax=ax2)
st.pyplot(fig2)

# Authorization rate by processor
st.subheader("Authorization Rate by Processor (All Levels)")
txn = pd.read_csv("apple_txn_success_by_processor.csv", index_col=0)
invoice = pd.read_csv("apple_invoice_success_by_processor.csv", index_col=0)
user = pd.read_csv("apple_user_success_by_processor.csv", index_col=0)
st.write("Transaction-Level:")
st.bar_chart(txn.sort_values(ascending=False))
st.write("Invoice-Level:")
st.bar_chart(invoice.squeeze().sort_values(ascending=False))
st.write("User-Level:")
st.bar_chart(user.sort_values(ascending=False))

# Declines recurring
st.subheader("Top Decline Reasons for Recurring Payments")
rec = pd.read_csv("apple_recurring_top_declines.csv", index_col=0)
st.bar_chart(rec)

# Apple vs card success rate by brand
st.subheader("Apple Pay vs Card-on-File by Brand")
brand_comp = pd.read_csv("apple_vs_card_success_by_brand.csv")
st.dataframe(brand_comp)

# Apple vs card success by brand per processor
st.subheader("Apple Pay vs Card-on-File by Brand and Processor")
brand_proc = pd.read_csv("apple_vs_card_brand_by_processor.csv")
st.dataframe(brand_proc)

st.caption("Dashboard: Apple Pay Performance | Built for Lemonade Interview")
