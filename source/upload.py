from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import io
from google.cloud import storage
from dotenv import load_dotenv

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

# Initialize the storage client
def initialize_storage_client():
    client = storage.Client()
    return client

def upload_file_to_bucket(bucket_name, file_path, destination_blob_name):
    # Initialize the storage client
    client = initialize_storage_client()
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Create a new blob in the bucket
    blob = bucket.blob(destination_blob_name)
    
    # Upload the file
    blob.upload_from_filename(file_path)
    
    print(f"File {file_path} uploaded to {destination_blob_name}.")

def upload_large_file_to_bucket(bucket_name, file_path, destination_blob_name, chunk_size=256*1024):
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    # Set chunk size
    blob.chunk_size = chunk_size  # Set to a multiple of 256 KB
    
    # Upload the file in chunks
    blob.upload_from_filename(file_path)
    print(f"Large file {file_path} uploaded to {destination_blob_name}.")

if __name__ == "__main__":
    load_dotenv()

    # Upload to Google Drive
    # # Path to the service account key file
    # SERVICE_ACCOUNT_FILE = os.environ['GDRIVE_CREDENDIALS_FILE']
    # SCOPES = ['https://www.googleapis.com/auth/drive.file']
    # PARENT_FOLDER_ID=os.environ['PARENT_FOLDER_ID']
    # service = initialize_drive_service()
    # response = upload_file(service, 'videos/27-7-2024_LIVE_P154_478139855159372.mp4')
    # print(response)

    # Upload to Google Bucket
    # Set the environment variable for the service account key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ['SA_CREDENTIALS_FILE']
    bucket_name = os.environ['GCP_BUCKET_NAME']
    file_path = ""
    destination_blob_name = ""

    upload_file_to_bucket(bucket_name, file_path, destination_blob_name)