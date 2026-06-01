import requests
import os
from dotenv import load_dotenv
# import json

load_dotenv(dotenv_path="./.env")

# Store sensitive data in a .env file
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = 'MrBeast'

# Enclose code you want to repeat in a function - Software dev best practices
def get_playlist_id():

    # Use try-except block to ensure proper error handling - software dev best practice
    try:
        # Create API URL using paramaterized API_KEY and CHANNEL_HANDLE
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()
        # print(data)
        # Another way to convert python data to json
        # print(json.dumps(data, indent=4))


        # Used json crack extension to get path to uploads
        # We want the uploads value to get the Playlist ID
        channel_items = data["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlist_id)
        return channel_playlist_id

    except requests.exceptions.RequestException as e:
        raise e
    
# Only true if the script is run directly instead of as a module
if __name__ == "__main__":
    get_playlist_id()