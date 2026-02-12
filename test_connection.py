from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://analytics_user:Pass123!@localhost:3306/sales_db"
)

try:
    connection = engine.connect()
    print("Connection Successful 🚀")
    connection.close()
except Exception as e:
    print("Connection Failed:", e)