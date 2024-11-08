# ETL_apacheairflow
# Web Log Processing Pipeline with Apache Airflow

## Project Overview
This project implements an ETL (Extract, Transform, Load) pipeline using Apache Airflow to process web server log files. The pipeline extracts specific fields from log files, performs transformations, and archives the results.

## Prerequisites
- Python 3.x
- Apache Airflow
- Access to a Linux/Unix environment

## Project Structure
```bash
/home/project/airflow/dags/
├── process_web_log.py    # Main DAG file
├── capstone/             
    ├── accesslog.txt     # Input log file
    ├── extracted_data.txt    
    ├── transformed_data.txt  
    └── weblog.tar       # Output file
```

## Installation
1. Create directories:
```bash
mkdir -p /home/project/airflow/dags/capstone
```

2. Download the dataset:
```bash
curl -o /home/project/airflow/dags/capstone/accesslog.txt https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/ETL/accesslog.txt
```

## DAG Implementation
The pipeline consists of three tasks:

1. **Extract**: Get IP and status code from logs
2. **Transform**: Filter out IP "198.46.149.143"
3. **Load**: Create archive file

## Running Pipeline
1. Start Airflow:
```bash
airflow webserver -D
airflow scheduler -D
```

2. Submit DAG:
```bash
python3 process_web_log.py
```

3. Unpause DAG:
```bash
airflow dags unpause process_web_log
```

4. Monitor:
```bash
airflow dags list-runs -d process_web_log
```

## Author
Phan Van Tien
