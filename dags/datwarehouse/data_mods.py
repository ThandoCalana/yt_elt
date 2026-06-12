import logging

logger = logging.getLogger(__name__)
table = "yt_api"


def insert_rows(cur, conn, schema, row):

    try:

        if schema.lower() == 'staging':
            video_id = 'video_id'

            cur.execute(f""""
                        
                        INSERT INTO {schema}.{table} (video_id, video_title, duration, upload_date, like, comments, views)
                        VALUES ((%video_id)s, (%video_title)s, (%duration)s, (%upload_date)s, (%like)s, (%comments)s, (%views)s);
                        """, row) # %(x)s notation allows us to look at that specific key within a dictionary
            
            conn.commit()
            logger.info(f"All data loaded for ID: {row[video_id]}")

        else:
            video_id = 'video_id'

            cur.execute(f""""
                        
                        INSERT INTO {schema}.{table} (video_id, video_title, duration, upload_date, like, comments, views)
                        VALUES ((%video_id)s, (%video_title)s, (%duration)s, (%upload_date)s, (%like)s, (%comments)s, (%views)s);
                        """, row)
            
            conn.commit()
            logger.info(f"All data loaded for ID: {row[video_id]}")

    except:
        logger.info(f"Error inserting ID: {row['video_id']}")
        raise


def update_row(cur, conn, schema, row):

    video_id = row['video_id']
    duration = row['duration']
    update_date = row['published_at']
    video_title = row['title']
    likes = row['likes']
    