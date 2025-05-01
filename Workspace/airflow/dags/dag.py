from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

def fetch_weather_data():
    subprocess.run(["python", "data.py"])

def preprocess_data():
    subprocess.run(["python", "preprocess.py"])

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 25),
    'retries': 1,
}

dag = DAG(
    'weather_data_pipeline',
    default_args=default_args,
    schedule_interval='0 21 * * 1',  # Or set a cron expression
)

task_fetch_data = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag,
)

task_preprocess_data = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

task_fetch_data >> task_preprocess_data
