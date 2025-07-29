
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Apple Pay Insights", layout="wide")
st.title("🍎 Apple Pay Performance Dashboard")

# Load Data
apple_df = pd.read_csv("apple_pay_only_dataset.csv")

# 📊 KPIs
st.subheader("Authorization KPIs")
txn_auth_rate = (apple_df['TRANSACTION_STATUS'] == 'success').mean()
invoice_auth_rate = apple_df.groupby('INVOICE_PUBLIC_ID')['TRANSACTION_STATUS'].apply(lambda x: 'success' in x.values).mean()
user_auth_rate = apple_df.groupby('USER_PUBLIC_ID')['TRANSACTION_STATUS'].apply(lambda x: 'success' in x.values).mean()
kpi_df = pd.DataFrame({
    "Metric": ["Transaction-Level", "Invoice-Level", "User-Level"],
    "Authorization Rate": [txn_auth_rate, invoice_auth_rate, user_auth_rate]
})
st.dataframe(kpi_df.set_index("Metric").style.format("{:.2%}"))

# 📈 Daily Apple Pay Success Trend
st.subheader("Apple Pay Volume & Success Over Time")
apple_trend = pd.read_csv("apple_pay_daily_trend.csv", index_col=0)
valid_statuses = ['success', 'refused', 'error']
apple_trend = apple_trend[[c for c in apple_trend.columns if c in valid_statuses]]
st.line_chart(apple_trend)

# 📊 Auth Rate by Card Brand
st.subheader("Authorization Rate by Card Brand")
auth_by_brand = (
    apple_df.groupby("CREDIT_CARD_BRAND")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(auth_by_brand)

# 📊 Success Rate by Attempt Number
st.subheader("Success Rate by Attempt Number")
funnel_data = (
    apple_df.groupby("ATTEMPT_NUMBER")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_index()
)
st.line_chart(funnel_data)

# 📊 Success Rate by Subscription Interval
st.subheader("Authorization Rate by Subscription Interval")
auth_by_interval = (
    apple_df.groupby("SUBSCRIPTION_INTERVAL")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(auth_by_interval)

# 📊 Retry Success Rate by Processor
st.subheader("Retry Success Rate by Processor")
retry_success = (
    apple_df[apple_df["ATTEMPT_NUMBER"] > 1]
    .groupby("PROCESSOR")["TRANSACTION_STATUS"]
    .value_counts(normalize=True).unstack().fillna(0)["success"]
    .sort_values(ascending=False)
)
st.bar_chart(retry_success)

# 🔥 Heatmap: Decline Reason × Attempt Number
st.subheader("Heatmap: Decline Reason by Attempt Number")
heatmap_data = (
    apple_df[apple_df["TRANSACTION_STATUS"] == "refused"]
    .groupby(["ERROR_MESSAGE", "ATTEMPT_NUMBER"]).size()
    .unstack(fill_value=0)
)
fig, ax = plt.subplots(figsize=(10, 12))
sns.heatmap(heatmap_data, cmap="Reds", linewidths=0.5, annot=False, ax=ax)
st.pyplot(fig)

# 📋 Decline Reasons by Charge Category
st.subheader("Decline Reasons by Charge Category")
declines_by_category = (
    apple_df[apple_df["TRANSACTION_STATUS"] == "refused"]
    .groupby(["CHARGE_CATEGORY", "ERROR_MESSAGE"]).size()
    .unstack(fill_value=0)
)
st.dataframe(declines_by_category)

# 📊 Apple Pay vs Card-on-File Success Rate by Brand
st.subheader("Apple Pay vs Card-on-File Success Rate by Brand")
brand_comp = pd.read_csv("apple_vs_card_success_by_brand.csv")
st.dataframe(brand_comp.style.format({"ApplePay_SuccessRate": "{:.2%}", "Card_SuccessRate": "{:.2%}"}))

# 📊 Authorization Rate by Processor (3 levels)
st.subheader("Transaction-Level Auth Rate by Processor")
txn = pd.read_csv("apple_txn_success_by_processor.csv", index_col=0)
st.bar_chart(txn.sort_values(by='success', ascending=False))

st.subheader("Invoice-Level Auth Rate by Processor")
invoice = pd.read_csv("apple_invoice_success_by_processor.csv", index_col=0)
st.bar_chart(invoice.sort_values(ascending=False))

st.subheader("User-Level Auth Rate by Processor")
user = pd.read_csv("apple_user_success_by_processor.csv", index_col=0)
st.bar_chart(user.sort_values(ascending=False))

# 📋 Top Declines for Recurring Apple Pay Transactions
st.subheader("Top Decline Reasons – Recurring Apple Pay Transactions")
recur = pd.read_csv("apple_recurring_top_declines.csv", index_col=0)
st.bar_chart(recur)

# 🆚 Apple Pay vs Card Success by Brand per Processor
st.subheader("Apple Pay vs Card-on-File Success Rate by Brand & Processor")
brand_proc = pd.read_csv("apple_vs_card_brand_by_processor.csv")
st.dataframe(brand_proc.style.format({
    "ApplePay_SuccessRate": "{:.2%}",
    "Card_SuccessRate": "{:.2%}"
}))

st.caption("Built for Lemonade Case Study — Apple Pay Deep Dive")
