import json
from datetime import date
import logging

logger = logging.getLogger(__name__)

def load_data():

    file_path = f"./data/YT_data_{date.today()}.json"

    try:
        with open(file_path, 'r', encoding="utf-8") as raw_data: # Open file in 'read-mode'
            data = json.load(raw_data) # Deserializes the file into a Python object

            return data
        
    except FileNotFoundError:
        logger.info(f"File Not Found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.info(f"JSON error on file: {file_path}")
        raise