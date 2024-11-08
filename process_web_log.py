# Import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
import requests

input_file = '/home/project/airflow/dags/capstone/accesslog.txt'
extracted_file = '/home/project/airflow/dags/capstone/extracted_data.txt'
transformed_file = '/home/project/airflow/dags/capstone/transformed_data.txt'
output_file = '/home/project/airflow/dags/capstone/weblog.tar'


def extract_data():
    print("Inside Extract")
    with open(input_file, 'r') as infile, \
         open(extracted_file, 'w') as outfile:
        for line in infile:
            try:
                ip = line.split(' ')[0]
                status_code = line.split('"')[2].strip().split(' ')[0]
                outfile.write(f"{ip}#{status_code}\n")              
            except IndexError:
                # Skip malformed lines
                continue    
    print("Extract completed")

def transform_data():
    print("Inside Transform")   
    with open(extracted_file, 'r') as infile, \
         open(transformed_file, 'w') as outfile:
        for line in infile:
            if "198.46.149.143" not in line:
                outfile.write(line)   
    print("Transform completed")

def load_data():
    global transformed_file, output_file
    print("Inside Load")
    
    # Save the array to a CSV file
    with open(transformed_file, 'r') as infile, \
         open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line + '\n')
    
    print("Load completed")

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Phan Van Tien',
    'start_date': days_ago(0),
    'email': ['tienphantps@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='process_web_log',
    schedule_interval=timedelta(days=1),
)

# Task 1
execute_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

# Task 2
execute_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

# Task 3
execute_load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

# Set up task pipeline
execute_extract >> execute_transform >> execute_load
