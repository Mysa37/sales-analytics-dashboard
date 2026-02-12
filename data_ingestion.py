import pandas as pd
from sqlalchemy import create_engine

# === 1. Read CSV ===
df = pd.read_csv("data/raw/sales_data.csv", encoding="latin1")

print("Initial Shape:", df.shape)
print("Original Columns:", df.columns)

# === 2. Rename Columns EXACTLY ===
df.rename(columns={
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country"
}, inplace=True)

print("Renamed Columns:", df.columns)

# === 3. Cleaning ===
df = df.dropna(subset=["customer_id"])
df = df[df["quantity"] > 0]
df = df[df["unit_price"] > 0]

df["invoice_date"] = pd.to_datetime(
    df["invoice_date"],
    format="%d-%m-%Y %H:%M"
)
df["customer_id"] = df["customer_id"].astype(int)

print("Cleaned Shape:", df.shape)

# === 4. Connect to MySQL ===
engine = create_engine(
    "mysql+pymysql://analytics_user:Pass123!@localhost:3306/sales_db"
)

# === 5. Insert into MySQL ===
df.to_sql("sales", engine, if_exists="append", index=False)

print("✅ Data successfully loaded into MySQL")