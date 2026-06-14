from airflow import DAG
import pendulum 
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_details, save_file
from datawarehouse.dwh import load_staging, load_core

local_tz = pendulum.timezone("Africa/Johannesburg")

default_args = { # Airflow-provided
    'owner': 'thandocalana',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1, tzinfo=local_tz),
    'email': ['tcalana2013@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=10),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

with DAG(
    dag_id = "produce_json",
    start_date = datetime(2026,6,1),
    default_args = default_args,
    description = "DAG to produce JSON file",
    schedule = "0 8 * * */2", # At 08:00 on every 2nd day-of-week.
    catchup = False
) as dag:
    
    # Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extract_video_details(video_ids)
    save_to_json = save_file(extracted_data)

    # Define dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json


with DAG(
    dag_id = "update_db",
    start_date = datetime(2026,6,1),
    default_args = default_args,
    description = "DAG to load data into staging and core layers",
    schedule = "0 9 * * */2", # At 08:00 on every 2nd day-of-week.
    catchup = False
) as dag:
    
    # Define tasks
    staging_load = load_staging()
    core_load = load_core()

    # Define dependencies
    staging_load >> core_load