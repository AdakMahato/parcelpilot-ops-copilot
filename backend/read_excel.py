import pandas as pd
import json

excel_path = "../data/ParcelPilot_Assessment_Data.xlsx"
xls = pd.ExcelFile(excel_path)
print("Sheets:", xls.sheet_names)

for sheet in xls.sheet_names:
    print(f"\n--- {sheet} ---")
    df = pd.read_excel(excel_path, sheet_name=sheet)
    print(df.head(10).to_string())
