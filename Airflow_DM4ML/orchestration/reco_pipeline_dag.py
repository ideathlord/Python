from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "recomart",
    "start_date": datetime(2026, 1, 1),
    "retries": 1
}

with DAG(
    dag_id="recomart_recommendation_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    generate_data = BashOperator(
        task_id="generate_csv_data",
        bash_command="python ingestion/generate_csv_data.py"
    )

    ingest_api = BashOperator(
        task_id="ingest_api_data",
        bash_command="python ingestion/ingest_api_data.py"
    )

    validate = BashOperator(
        task_id="validate_data",
        bash_command="python validation/validate_data.py"
    )

    clean = BashOperator(
        task_id="clean_data",
        bash_command="python preprocessing/clean_and_eda.py"
    )

    build_features = BashOperator(
        task_id="build_features",
        bash_command="python features/build_features.py"
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="python model/train_model.py"
    )

    generate_data >> ingest_api >> validate >> clean >> build_features >> train_model