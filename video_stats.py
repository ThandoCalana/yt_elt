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

        # print(channel_playlist_id)
        return channel_playlist_id

    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_ids(playlist_id): # extract a list of video IDs from the provided playlist

    video_ids = []
    page_token = None # Initialize to None since the first run will have no page token

    max_results = 50
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'


    try:
        while True: # Keep looping until there are no more page tokens

            url = base_url

            if page_token:
                url += f'&pageToken={page_token}' # concat page token to url once the page token var exists (2nd run onwards)

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            page_token = data.get('nextPageToken')

            if not page_token:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e

    
# Only true if the script is run directly instead of as a module
if __name__ == "__main__":
    playlist_id = get_playlist_id()
    print(get_video_ids(playlist_id))