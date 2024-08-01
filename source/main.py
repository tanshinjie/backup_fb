from datetime import datetime
from upload import initialize_drive_service, upload_large_file_to_bucket
from download import extract_filename_from_text, download_facebook_video, get_video_id_from_url
from utils import resolve_path_to_file
import json
import os
import logging
from dotenv import load_dotenv

def validate_fields(data):
    required_fields = ["creation_time", "description", "permalink_url", "id"]
    for index, item in enumerate(data):
        for field in required_fields:
            if field not in item:
                print(f"Missing required field '{field}' in item {index}")
                return False
    return True


if __name__ == "__main__":
    load_dotenv()

    file_path = "../videos.json"
    input_file_path = resolve_path_to_file(file_path)

    log_file_path = resolve_path_to_file(f'../output/app.log')

    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # Set the environment variable for the service account key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["SA_CREDENTIALS_FILE"]
    bucket_name = os.environ["GCP_BUCKET_NAME"]

    # Input data
    videos = []

    with open(input_file_path) as f:
        videos = json.load(f)
    
    for video in videos:
        url = "https://www.facebook.com" + video["permalink_url"]
        text = video["description"]
        video_id = get_video_id_from_url(url)
        
        # Extract filename from text or use video ID as default
        output_filename = extract_filename_from_text(text, video_id) + ".mp4"
        output_file_path = "videos/" + output_filename

        print("Step 1: Download", video_id)
        # Download the video
        download_facebook_video(url, output_file_path)

        if (os.path.exists(output_file_path)):

            print("Step 2: Upload to GCP Bucket")
            # Upload to bucket
            upload_large_file_to_bucket(bucket_name, output_file_path, output_filename)

            print("Step 3: Cleanup local copy")
            # Delete the file
            os.remove(output_file_path)

        else:
            print(f"No mp4 found for: {output_filename}. Need to manual upload.")
