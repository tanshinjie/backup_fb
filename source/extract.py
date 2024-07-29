import re
import json
from bs4 import BeautifulSoup
from utils import resolve_path_to_file
from datetime import datetime

# The regex pattern to match the specific Facebook URLs
pattern = r"/100063765656088/videos/.*"

# Function to extract URLs and their sibling aria-labels from HTML content
def extract_links_and_labels(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []

    links = soup.find_all('a', href=True)

    # Find all anchor tags with href attributes
    for link in links:
        url = link['href']
        if re.match(pattern, url):
            aria_label = link.get('aria-label', '')
            if aria_label:
                data.append({ 'Link': "https://www.facebook.com" + url, 'Text': aria_label})

    return data

if __name__ == "__main__":
    # File path to the local HTML file
    file_path = resolve_path_to_file("../output/facebook_page.html")  # Replace with the actual file path


    # Read the HTML content from the local file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Extract the matching links and their aria-labels
    matching_data = extract_links_and_labels(html_content)

    # File path to save the extracted data as a JSON file
    json_file_path = resolve_path_to_file(f"../output/extracted_link_{datetime.now().strftime("%Y-%m-%d")}.json")  # You can change the file name if needed


    # Save the data to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(matching_data, jsonfile, ensure_ascii=False, indent=4)

    print(f"Extracted data has been saved to {json_file_path}")
