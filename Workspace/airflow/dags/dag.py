from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def fetch_weather_data():
    subprocess.run(["python", "/opt/airflow/data.py"], check=True)

def preprocess_data():
    subprocess.run(["python", "/opt/airflow/preprocess.py"], check=True)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 25),
    'retries': 1,
}

with DAG(
    dag_id='weather_data_pipeline',
    default_args=default_args,
    schedule='0 21 * * 1',  # ✅ New syntax: `schedule` not `schedule_interval`
    catchup=False,
    tags=['example'],
) as dag:

    task_fetch_data = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather_data,
    )

    task_preprocess_data = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )

    task_fetch_data >> task_preprocess_data
