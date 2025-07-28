
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Apple Pay Insights", layout="wide")
st.title("🍎 Apple Pay Performance Dashboard")

# Load Apple Pay data
apple_df = pd.read_csv("apple_pay_only_dataset.csv")

# KPIs
st.subheader("Authorization KPIs")
txn_auth_rate = (apple_df['TRANSACTION_STATUS'] == 'success').mean()
invoice_auth_rate = apple_df.groupby('INVOICE_PUBLIC_ID')['TRANSACTION_STATUS'].apply(lambda x: 'success' in x.values).mean()
user_auth_rate = apple_df.groupby('USER_PUBLIC_ID')['TRANSACTION_STATUS'].apply(lambda x: 'success' in x.values).mean()

kpi_df = pd.DataFrame({
    "Metric": ["Transaction-Level", "Invoice-Level", "User-Level"],
    "Authorization Rate": [txn_auth_rate, invoice_auth_rate, user_auth_rate]
})
st.dataframe(kpi_df.set_index("Metric").style.format("{:.2%}"))

# Authorization Rate by Processor
st.subheader("Authorization Rate by Processor")
auth_by_processor = (
    apple_df.groupby("PROCESSOR")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(auth_by_processor)

# Authorization Rate by Card Brand
st.subheader("Authorization Rate by Card Brand")
auth_by_brand = (
    apple_df.groupby("CREDIT_CARD_BRAND")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(auth_by_brand)

# Authorization Rate by Attempt Number
st.subheader("Success Rate by Attempt Number")
funnel_data = (
    apple_df.groupby("ATTEMPT_NUMBER")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_index()
)
st.line_chart(funnel_data)

# Authorization Rate by Charge Category
st.subheader("Authorization Rate by Charge Category")
auth_by_category = (
    apple_df.groupby("CHARGE_CATEGORY")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(auth_by_category)

# Decline Reasons by Processor
st.subheader("Top Decline Reasons by Processor")
declined = apple_df[apple_df['TRANSACTION_STATUS'] == 'refused']
declines = declined.groupby(["PROCESSOR", "ERROR_MESSAGE"]).size().unstack(fill_value=0)
st.dataframe(declines)

st.caption("Built for Lemonade Case Study — Apple Pay Deep Dive")


# Success Rate by Subscription Interval
st.subheader("Authorization Rate by Subscription Interval")
auth_by_interval = (
    apple_df.groupby("SUBSCRIPTION_INTERVAL")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(auth_by_interval)

# Retry Success Rate by Processor
st.subheader("Retry Success Rate by Processor")
retry_success = (
    apple_df[apple_df["ATTEMPT_NUMBER"] > 1]
    .groupby("PROCESSOR")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(retry_success)

# Heatmap: Decline Reason × Attempt Number
import seaborn as sns
import matplotlib.pyplot as plt

st.subheader("Heatmap: Decline Reason by Attempt Number")
heatmap_data = (
    apple_df[apple_df["TRANSACTION_STATUS"] == "refused"]
    .groupby(["ERROR_MESSAGE", "ATTEMPT_NUMBER"]).size()
    .unstack(fill_value=0)
)

fig, ax = plt.subplots(figsize=(10, 12))
sns.heatmap(heatmap_data, cmap="Reds", linewidths=0.5, annot=False, ax=ax)
st.pyplot(fig)

# Root Cause: Decline Reasons by Charge Category
st.subheader("Decline Reasons by Charge Category")
declines_by_category = (
    apple_df[apple_df["TRANSACTION_STATUS"] == "refused"]
    .groupby(["CHARGE_CATEGORY", "ERROR_MESSAGE"]).size()
    .unstack(fill_value=0)
)
st.dataframe(declines_by_category)


# 📈 Apple Pay Daily Success Volume
st.subheader("Apple Pay Volume & Success Over Time")
apple_trend = pd.read_csv("apple_pay_daily_trend.csv", index_col=0)
st.line_chart(apple_trend)

# 📊 Apple Pay vs Card-on-File Success Rate by Card Brand
st.subheader("Apple Pay vs Card-on-File Success Rate by Brand")
brand_comp = pd.read_csv("apple_vs_card_success_by_brand.csv")
st.dataframe(brand_comp.style.format({"ApplePay_SuccessRate": "{:.2%}", "Card_SuccessRate": "{:.2%}"}))
