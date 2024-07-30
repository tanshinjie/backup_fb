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
        filename = match.group(0).strip().replace('/', '-').replace(' ', '_') + "_" + default
    else:
        filename = default
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

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        filename=f'output/app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # Input data
    videos = [
        {
            "Link": "https://www.facebook.com/100063765656088/videos/478139855159372",
            "Text": "你知道不对的姿势会影响你的健康吗？\n# 低头看手机 长时间的办公桌工作 #电脑前的不对姿势\n这些都会让上班族的您照成隐患\n🇦🇺🇨🇦🇺🇸🇸🇬🇮🇩🇮🇳🇹🇼🇭🇰\n27/7/2024 LIVE P154 ( 268 )\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n进入直播 👇了解更多\n健康直播学习平台🏊‍♂️\n让你过着有品质的生活💯🈵️🔥❤️\n想要了解更多\n记得关注我们的页面，会随时更新的哦~\n\n#走路久了不舒服 #站久不舒服 #睡觉起来不舒服 #坐久不舒服 #站久不舒服 #久驾不适 #怎么锻炼 #怎样保养 #健康养生 #不适原因 #马来西亚 #槟城 #malaysia #penang #autoworld #MasterJack #wellness"
        },
        # Add more video data here...
    ]
    
    for video in videos:
        url = video["Link"]
        text = video["Text"]
        video_id = get_video_id_from_url(url)
        
        # Extract filename from text or use video ID as default
        output_filename = extract_filename_from_text(text, video_id) + ".%(ext)s"
        
        # Download the video
        download_facebook_video(url, output_filename)