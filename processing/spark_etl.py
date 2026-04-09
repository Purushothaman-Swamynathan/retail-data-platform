# ==============================
# RETAIL ETL PIPELINE (FIXED)
# ==============================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum as _sum

# ==============================
# STEP 1: START SPARK
# ==============================

spark = SparkSession.builder \
    .appName("Retail ETL Pipeline") \
    .getOrCreate()

print("✅ Spark Session Started")

# ==============================
# STEP 2: LOAD DATA
# ==============================

file_path = "data/raw/retail.csv"

df = spark.read.csv(file_path, header=True, inferSchema=True)

print("✅ Data Loaded")
df.show(5)

# ==============================
# STEP 3: CLEAN COLUMN NAMES
# ==============================

# Remove spaces from all column names
df = df.toDF(*[c.replace(" ", "") for c in df.columns])

# Now columns become:
# CustomerID instead of Customer ID

# ==============================
# STEP 4: DATA CLEANING
# ==============================

df = df.dropna(subset=["CustomerID", "Quantity", "Price"])

# Remove invalid values
df = df.filter((col("Quantity") > 0) & (col("Price") > 0))

print("✅ Data Cleaned")

# ==============================
# STEP 5: TRANSFORMATION
# ==============================

df = df.withColumn("amount", col("Quantity") * col("Price"))

# Rename columns
df = df.withColumnRenamed("CustomerID", "customer_id") \
       .withColumnRenamed("InvoiceDate", "timestamp")

print("✅ Transformation Done")

# ==============================
# STEP 6: FRAUD DETECTION
# ==============================

df = df.withColumn(
    "fraud_flag",
    when(col("amount") > 10000, 1).otherwise(0)
)

print("✅ Fraud Detection Applied")

# ==============================
# STEP 7: AGGREGATION
# ==============================

result = df.groupBy("customer_id") \
           .agg(_sum("amount").alias("total_spent"))

print("✅ Aggregation Done")
result.show(10)

# ==============================
# STEP 8: SAVE DATA (FIXED)
# ==============================

# ❌ OLD (causes error)
# df.write.mode("overwrite").csv(output_path, header=True)


# ✅ NEW (Windows-safe)
output_file = "data/processed/output.csv"
# ==============================
# SAVE TRANSACTIONS (IMPORTANT)
# ==============================

df.toPandas().to_csv("data/processed/transactions.csv", index=False)

print("✅ Transactions file saved")

# ==============================
# OPTIONAL: SAVE AGGREGATION
# ==============================

result.toPandas().to_csv("data/processed/output.csv", index=False)

print("✅ Aggregated file saved")

# ==============================
# END
# ==============================

spark.stop()

print("🔥 ETL PIPELINE COMPLETED SUCCESSFULLY")