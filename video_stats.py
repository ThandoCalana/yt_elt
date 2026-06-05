import requests
import os
from dotenv import load_dotenv
import json
from datetime import date

load_dotenv(dotenv_path="./.env")

# Store sensitive data in a .env file
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
MAX_RESULTS = 50

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

    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}&playlistId={playlist_id}&key={API_KEY}'


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


def extract_video_details(video_ids):
    
    extracted_details = []

    def batch_videos(video_id_list:list, batch_size:int):
        for video_id in range(0, len(video_id_list), batch_size): # start, end, step
            # Use yield to still return the result but don't stop the looping process
            yield video_id_list[video_id: video_id + batch_size] # extracting a slice of the video IDs

    try:
        for batch in batch_videos(video_ids, MAX_RESULTS):
            video_ids_str = ",".join(batch) # API URL takes a comma-separated list of video ids 
            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                content_details = item['contentDetails']
                video_statistics = item['statistics']
                video_snippet = item['snippet']

                extracted_data = {
                    'video_id': video_id,
                    'duration': content_details['duration'],
                    'published_at': video_snippet['publishedAt'],
                    'title': video_snippet['title'],
                    'likes': video_statistics.get('likeCount', None), # Some videos may not have likes -> default to None
                    'comments': video_statistics.get('commentCount', None),
                    'views': video_statistics.get('viewCount', None)
                    }
                
                extracted_details.append(extracted_data)

    except requests.exceptions.RequestException as e:
        raise e

    return extracted_details
            
def save_file(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=4) # json.dump writes to a file, ensure ascii=false to ensure utf-8 encoding (allows for special chars)

# Only true if the script is run directly instead of as a module
if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extract_video_details(video_ids)
    save_file(extracted_data)