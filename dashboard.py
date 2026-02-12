import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Analytics Dashboard")

# -----------------------------
# LOAD DATA (CSV ONLY)
# -----------------------------
df = pd.read_csv("data/raw/Sales_data.csv", encoding="latin1")

df['invoice_date'] = pd.to_datetime(df['invoice_date'], dayfirst=True)
df['revenue'] = df['quantity'] * df['unit_price']

# -----------------------------
# KPIs CALCULATION
# -----------------------------
total_revenue = df['revenue'].sum()
total_orders = df['invoice_no'].nunique()
total_units = df['quantity'].sum()
avg_order_value = total_revenue / total_orders
revenue_per_customer = total_revenue / df['customer_id'].nunique()

# Repeat Customer Rate
repeat_customers = df.groupby('customer_id')['invoice_no'].nunique()
repeat_rate = (repeat_customers > 1).sum() / df['customer_id'].nunique() * 100

# -----------------------------
# KPI DISPLAY
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("📦 Units Sold", total_units)
col4.metric("💳 Avg Order Value", f"${avg_order_value:,.2f}")
col5.metric("🔁 Repeat Customer %", f"{repeat_rate:.2f}%")

st.divider()

# -----------------------------
# MONTHLY REVENUE TREND
# -----------------------------
monthly = (
    df.groupby(df['invoice_date'].dt.to_period('M'))['revenue']
    .sum()
    .reset_index()
)
monthly['invoice_date'] = monthly['invoice_date'].astype(str)

fig_monthly = px.line(
    monthly,
    x='invoice_date',
    y='revenue',
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------------
# TOP 5 PRODUCTS
# -----------------------------
top_products = (
    df.groupby('description')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x='revenue',
    y='description',
    orientation='h',
    title="Top 5 Products by Revenue"
)

st.plotly_chart(fig_products, use_container_width=True)

# -----------------------------
# REVENUE BY COUNTRY
# -----------------------------
country = df.groupby('country')['revenue'].sum().reset_index()

fig_country = px.bar(
    country,
    x='country',
    y='revenue',
    title="Revenue by Country"
)

st.plotly_chart(fig_country, use_container_width=True)

# -----------------------------
# TOP 5 CUSTOMERS
# -----------------------------
top_customers = (
    df.groupby('customer_id')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

st.subheader("🏆 Top 5 Customers")
st.dataframe(top_customers)