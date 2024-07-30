from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import io

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'secrets/sa_credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
PARENT_FOLDER_ID="1EW0JQCf9poHdjMk0dK8gyU2lTY7fhcTP"

def initialize_drive_service():
    # creds = None
    # if os.path.exists(TOKEN_PATH):
        # creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive'])
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create your own flow and save the token
            pass

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(service, file_path, chunk_size=256 * 1024):
    file_metadata = {'name': os.path.basename(file_path), 'parents':[PARENT_FOLDER_ID]}
    
    # Initialize media upload with resumable upload type
    media = MediaFileUpload(file_path, resumable=True)
    
    request = service.files().create(body=file_metadata, media_body=media)
    
    # Upload the file in chunks
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("Upload complete")
    return response

if __name__ == "__main__":
    service = initialize_drive_service()
    response = upload_file(service, 'videos/27-7-2024_LIVE_P154_478139855159372.mp4')
    print(response)
