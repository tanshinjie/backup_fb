import requests
import json
import os
from dotenv import load_dotenv

def fetch_videos(access_token, page_url=None, all_videos=None):
    if all_videos is None:
        all_videos = []

    if page_url is None:
        base_url = "https://graph.facebook.com/v20.0/JSPWellnessBoneAlignme/live_videos?fields=creation_time,description,permalink_url"
        params = {
            'access_token': access_token,
            'debug': 'all',
            'format': 'json',
            'method': 'get',
            'origin_graph_explorer': '1',
            'pretty': '0',
            'suppress_http_code': '1',
            'transport': 'cors'
        }
    else:
        base_url = page_url
        params = None

    response = requests.get(base_url, params=params)
    data = response.json()

    # Append the fetched data to the list
    all_videos.extend(data.get('data', []))

    # Check if there are more pages to fetch
    paging = data.get('paging', {})
    next_page_url = paging.get('next')
    if next_page_url:
        fetch_videos(access_token, next_page_url, all_videos)
    
    return all_videos

def save_to_file(data, filename='videos.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    load_dotenv()
    
    FB_ACCESS_TOKEN = os.environ["FB_ACCESS_TOKEN"]
    
    # Fetch all videos and save to a JSON file
    all_videos_data = fetch_videos(FB_ACCESS_TOKEN)
    save_to_file(all_videos_data)
    print(f"Data has been saved to 'videos.json'")
