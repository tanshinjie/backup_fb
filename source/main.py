from datetime import datetime
from upload import initialize_drive_service, upload_file
from download import extract_filename_from_text, download_facebook_video, get_video_id_from_url
from utils import resolve_path_to_file
import json
import os
import logging
from dotenv import load_dotenv, dotenv_values 

if __name__ == "__main__":
    file_path = f'../output/extracted_links_{datetime.now().strftime("%Y-%m-%d")}.json'
    input_file_path = resolve_path_to_file(file_path)

    log_file_path = resolve_path_to_file(f'../output/app.log')

    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    # Input data
    videos = []

    with open(input_file_path) as f:
        videos = json.load(f)
    
    for video in videos:
        url = video["Link"]
        text = video["Text"]
        video_id = get_video_id_from_url(url)
        
        # Extract filename from text or use video ID as default
        output_filename = "videos/" + extract_filename_from_text(text, video_id)
        
        print("Step 1: Download", video_id)
        # Download the video
        download_facebook_video(url, output_filename + ".mp4")

        if (os.path.exists(output_filename + ".mp4")):
            output_filename = output_filename + ".mp4"

            print("Step 2: Upload to Google Drive")
            # Upload to gdrive
            service = initialize_drive_service()
            response = upload_file(service, output_filename)
            print(response)

            print("Step 3: Cleanup local copy")
            # Delete the file
            os.remove(output_filename)

        else:
            print(f"No mp4 found for: {output_filename}. Need to manual upload.")
