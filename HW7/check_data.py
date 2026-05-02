"""
HW7 - Check Data Structure
Run this first to understand your data
"""

import pandas as pd

# Load the CSV file (FIXED: changed to read_csv)
df = pd.read_csv("processed_data.csv")

print("="*50)
print("DATA INFORMATION")
print("="*50)

print("\n[1] COLUMN NAMES:")
print(df.columns.tolist())

print("\n[2] FIRST 3 ROWS:")
print(df.head(3))

print("\n[3] LABEL VALUES:")
print(df['label'].unique())

print("\n[4] FILE SHAPE:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n[5] MISSING VALUES:")
print(df.isnull().sum())

print("\n[6] SAMPLE EMAIL:")
print("Subject:", str(df['subject'].iloc[0])[:100])
print("Message:", str(df['message'].iloc[0])[:200])