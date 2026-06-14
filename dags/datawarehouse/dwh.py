from datawarehouse.data_load import load_data
from datawarehouse.data_utils import create_conn, close_conn, create_schema, create_table, get_video_ids
from datawarehouse.data_mods import insert_rows, update_row, delete_rows
from datawarehouse.data_transformation import transform_data

from airflow.decorators import task
import logging

logger = logging.getLogger(__name__)
table = "yt_api"

@task
def load_staging():

    schema = 'staging'
    conn, curr = None, None

    try:
        conn, cur = create_conn()
        create_schema(schema)
        create_table(schema)

        data = load_data()

        video_ids = get_video_ids(cur, schema)

        existing_ids = set()

    
        for row in data:
            if len(video_ids) == 0:
                insert_rows(cur, conn, schema, row)
            else:
                if row['video_id'] in video_ids:
                    update_row(cur, conn, schema, row)
                else:
                    insert_rows(cur, conn, schema, row)

            existing_ids.add(row['video_id'])

        ids_to_delete = set(video_ids) - existing_ids

        if ids_to_delete:
            delete_rows(cur, conn, schema, ids_to_delete)

        logger.info(f"{schema} table update complete")

    except Exception as e:
        logger.info(f"Error loading staging data")
        raise e
    
    finally:
        if conn and cur:
            close_conn(conn,cur)

@task
def load_core():

    schema = 'core'
    conn, curr = None, None
    
    try:

        conn, cur = create_conn()
        create_schema(schema)
        create_table(schema)

        # Get all data from STAGING layer that will be processed
        # Can process in batches if data is to large
        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall()

        video_ids = get_video_ids( cur, schema) 

        existing_ids = set()

        for row in rows:
            transformed_row = transform_data(row)

            if len(video_ids) == 0:
                insert_rows(cur, conn, schema, transformed_row)
            else:
                if transformed_row['video_id'] in video_ids:
                    update_row(cur, conn, schema, transformed_row)
                else:
                    insert_rows(cur, conn, schema, transformed_row)

            existing_ids.add(transformed_row['video_id'])

        ids_to_delete = set(video_ids) - existing_ids

        if ids_to_delete:
            delete_rows(cur, conn, schema, ids_to_delete)

        logger.info(f"{schema} table update complete")
            
    except Exception as e:
        logger.info(f"Error loading core data")
        raise e
    
    finally:
        if conn and cur:
            close_conn(conn,cur)
