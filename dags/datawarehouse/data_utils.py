from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = "yt_api"

def create_conn():
    hook = PostgresHook(postgres_conn_id = "postgres_db_yt_elt", # Using the Airflow env var defined in docker compose {{ AIRFLOW_CONN_POSTGRES_DB_YT_ELT }} 
                        database = "elt_db") # ELT_DB defined in .env file
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor) # Return results as dict vs standard tuples

    return conn, cur

def close_conn(conn, cur):
    conn.close()
    cur.close()


def create_schema(schema):

    conn, cur = create_conn()

    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"

    cur.execute(schema_sql)

    conn.commit()

    close_conn(conn, cur)

def create_table(schema):

    conn, cur = create_conn()

    if schema.lower() == 'staging':
        table_sql = f"""
                    CREATE TABLE IF NOT EXISTS {schema}.{table} 
                    (
                        video_id VARCHAR(11) PRIMARY KEY NOT NULL,
                        video_title VARCHAR NOT NULL,
                        duration VARCHAR NOT NULL,
                        upload_date TIMESTAMP NOT NULL,
                        likes INT,
                        comments INT,
                        views INT 
                    );
                    """
    else:
        table_sql = f"""
                    CREATE TABLE IF NOT EXISTS {schema}.{table} 
                    (
                        video_id VARCHAR(11) PRIMARY KEY NOT NULL,
                        video_title VARCHAR NOT NULL,
                        duration TIME NOT NULL,
                        upload_date TIMESTAMP NOT NULL,
                        likes INT,
                        comments INT,
                        views INT 
                    );
                    """
        
    cur.execute(table_sql)

    conn.commit()

    close_conn(conn, cur)

    
def get_video_ids(cur, schema): # Retrieves all video ids in table

    video_sql = f" SELECT video_id FROM {schema}.{table}"
    cur.execute(video_sql)
    ids = cur.fetchall() 

    video_ids = [row['video_id'] for row in ids]

    return video_ids