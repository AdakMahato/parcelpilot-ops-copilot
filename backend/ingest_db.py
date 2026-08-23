import pandas as pd
from app.database import engine
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

excel_path = "../data/ParcelPilot_Assessment_Data.xlsx"

accounts_df = pd.read_excel(excel_path, sheet_name="accounts")
orders_df = pd.read_excel(excel_path, sheet_name="orders")
tickets_df = pd.read_excel(excel_path, sheet_name="tickets")

# Convert booleans where needed (pandas reads them as bool already if they are True/False)
accounts_df.to_sql("accounts", con=engine, if_exists="replace", index=False)
orders_df.to_sql("orders", con=engine, if_exists="replace", index=False)
tickets_df.to_sql("tickets", con=engine, if_exists="replace", index=False)

print("Ingested Excel data into parcelpilot.db")
