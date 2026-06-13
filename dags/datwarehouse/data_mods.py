import logging

logger = logging.getLogger(__name__)
table = "yt_api"


def insert_rows(cur, conn, schema, row):

    try:

        if schema.lower() == 'staging':
            video_id = 'video_id'

            cur.execute(f""""
                        
                        INSERT INTO {schema}.{table} (video_id, video_title, duration, upload_date, like, comments, views)
                        VALUES (%(video_id)s, %(video_title)s, %(duration)s, %(upload_date)s, %(like)s, %(comments)s, %(views)s);
                        """, row) # %(x)s notation allows us to look at that specific key within a dictionary

        else:
            video_id = 'video_id'

            cur.execute(f""""
                        
                        INSERT INTO {schema}.{table} (video_id, video_title, duration, upload_date, likes, comments, views)
                        VALUES (%(video_id)s, %(video_title)s, %(duration)s, %(upload_date)s, %(like)s, %(comments)s, %(views)s);
                        """, row)
            
        conn.commit()
        logger.info(f"All data loaded for ID: {row[video_id]}")

    except Exception as e:
        logger.info(f"Error inserting ID: {row['video_id']}")
        raise e


def update_row(cur, conn, schema, row):
    
    try:
        cur.execute(f"""
                    UPDATE {schema}.{table}
                    SET
                        video_title = %(video_title)s,
                        likes = %(likes)s,
                        comments = %(comments)s,
                        views = %(views)s
                    WHERE 
                        video_id = %(video_id)s
                    AND upload_date = %(upload_date)s;
                    """, row)
        conn.commit()
        logger.info(f"Update completed for ID: {row['video_id']}")

    except Exception as e:
        logger.info(f"Error updating row with ID: {row['video_id']}")
        raise e


def delete_row(cur, conn, schema, ids_to_delete:list):

    ids = ','.join(id for id in ids_to_delete)

    try:
        cur.execute(f"""
                    DELETE FROM {schema}.{table}
                    WHERE 
                        video_id IN {ids}
                    """)
        conn.commit()
        logger.info(f"All data deleted for IDs: {ids_to_delete}")

    except Exception as e:
        logger.info(f"Error deleting row for ID: {ids_to_delete}")
        raise e