from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'secrets/sa_credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
PARENT_FOLDER_ID="1EW0JQCf9poHdjMk0dK8gyU2lTY7fhcTP"

def upload_file_service_account(file_path):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path), 'parents':[PARENT_FOLDER_ID]}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")
