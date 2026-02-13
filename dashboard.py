import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Analytics Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/raw/Sales_data.csv", encoding="latin1")

# Clean column names
df.columns = df.columns.str.strip()

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Revenue column
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# Remove negative or cancelled transactions (optional but professional)
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_units = df['Quantity'].sum()
total_customers = df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders

# Repeat Customer %
repeat_customers = df.groupby('CustomerID')['InvoiceNo'].nunique()
repeat_rate = (repeat_customers > 1).sum() / total_customers * 100

# -----------------------------
# KPI DISPLAY
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🧾 Total Orders", f"{total_orders:,}")
col3.metric("📦 Units Sold", f"{total_units:,}")
col4.metric("👥 Total Customers", f"{total_customers:,}")
col5.metric("🔁 Repeat Customer %", f"{repeat_rate:.2f}%")

st.divider()

# -----------------------------
# MONTHLY REVENUE TREND
# -----------------------------
monthly = (
    df.groupby(df['InvoiceDate'].dt.to_period('M'))['Revenue']
    .sum()
    .reset_index()
)

monthly['InvoiceDate'] = monthly['InvoiceDate'].astype(str)

fig_monthly = px.line(
    monthly,
    x='InvoiceDate',
    y='Revenue',
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------------
# TOP 5 PRODUCTS
# -----------------------------
top_products = (
    df.groupby('Description')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x='Revenue',
    y='Description',
    orientation='h',
    title="Top 5 Products by Revenue"
)

st.plotly_chart(fig_products, use_container_width=True)

# -----------------------------
# REVENUE BY COUNTRY
# -----------------------------
country = (
    df.groupby('Country')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_country = px.bar(
    country,
    x='Country',
    y='Revenue',
    title="Revenue by Country"
)

st.plotly_chart(fig_country, use_container_width=True)

# -----------------------------
# TOP 5 CUSTOMERS
# -----------------------------
top_customers = (
    df.groupby('CustomerID')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

st.subheader("🏆 Top 5 Customers")
st.dataframe(top_customers)