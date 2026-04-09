import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Number of records
NUM_RECORDS = 200

data = []

start_time = datetime.now()

for i in range(NUM_RECORDS):
    record = {
        "Customer ID": random.randint(1, 20),
        "Quantity * Price": round(random.uniform(50, 1500), 2),
        "InvoiceDate": start_time + timedelta(seconds=i)
    }
    data.append(record)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
file_path = "data/data.csv"
df.to_csv(file_path, index=False)

print(f"✅ Data generated successfully: {file_path}")
print(df.head())