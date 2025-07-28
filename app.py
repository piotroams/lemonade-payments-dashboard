
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
