import subprocess
import logging
from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs
import json

def extract_filename_from_text(text, default):
    # Regex to extract date and any following info up to the first parenthesis
    match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})[^()]*', text)
    if match:
        filename = match.group(0).strip().replace('/', '-').replace(' ', '_').replace("\n", '').replace("\"", "").replace("\'", "") + "_" + default
    else:
        filename = text.split('\n')[0].replace("\"", "").replace("\'", "")  + "_" + default
    return filename

def download_facebook_video(video_url, output_filename):
    # Define the yt-dlp command with output template
    command = f'yt-dlp -o "{output_filename}" "{video_url}"'
    
    try:
        # Run the yt-dlp command
        result = subprocess.run(command, shell=True)
        
        # Log the output
        if result.returncode == 0:
            logging.info(f"Successfully downloaded video: {video_url}")
            print(f"Successfully downloaded: {video_url}")
        else:
            logging.error(f"Failed to download video: {video_url}\n{result.stderr}")
            print(f"Failed to download: {video_url}")
    except Exception as e:
        logging.error(f"Error downloading video: {video_url}\n{str(e)}")
        print(f"Error downloading: {video_url}")

def get_video_id_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.path.split('/')[-1]