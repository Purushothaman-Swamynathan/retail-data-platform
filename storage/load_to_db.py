# ==============================
# LOAD DATA TO POSTGRESQL (FINAL FIX)
# ==============================

import pandas as pd
import glob
from storage.db import get_connection
from dashboard.ml_model import predict_fraud

#fraud_flag = predict_fraud(amount)

# ==============================
# STEP 1: READ FILE
# ==============================

files = glob.glob("data/processed/transactions.csv")

if not files:
    print("❌ No processed files found!")
    exit()

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

print("✅ Data Loaded from processed folder")

# ==============================
# STEP 2: CONNECT DB
# ==============================

conn = get_connection()
cursor = conn.cursor()

print("Database connected successfully")

# ==============================
# STEP 3: INSERT CUSTOMERS FIRST
# ==============================

unique_customers = df["customer_id"].dropna().unique()

for cust_id in unique_customers:
    cursor.execute("""
        INSERT INTO customers (customer_id)
        VALUES (%s)
        ON CONFLICT (customer_id) DO NOTHING
    """, (int(cust_id),))
conn.commit()   # 🔥 VERY IMPORTANT

print("✅ Customers inserted")

# ==============================
# STEP 4: INSERT TRANSACTIONS
# ==============================

for _, row in df.iterrows():
    cursor.execute("""
     INSERT INTO transactions (customer_id, amount, timestamp, fraud_flag)
        VALUES (%s, %s, %s, %s)
    """, (
        int(row["customer_id"]),
        float(row["amount"]),
        str(row["timestamp"]),
        bool(row["fraud_flag"])
    ))

conn.commit()

print("✅ Transactions inserted")

# ==============================
# STEP 5: CLOSE
# ==============================

cursor.close()
conn.close()

print("🔥 DATA LOADED SUCCESSFULLY")