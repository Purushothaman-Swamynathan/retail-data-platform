from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def run_etl():
    os.system("python processing/spark_etl.py")

def load_db():
    os.system("python storage/load_to_db.py")

with DAG(
    dag_id="retail_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl
    )

    task2 = PythonOperator(
        task_id="load_db",
        python_callable=load_db
    )

    task1 >> task2