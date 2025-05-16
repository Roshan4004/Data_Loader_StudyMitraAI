from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os, io
from googleapiclient.http import MediaIoBaseDownload

#ESSENTIALS FOR GOOGLE CREDENTIALS
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

#Build credentials using service_account
def get_drive_service():
    creds = Credentials.from_service_account_file(os.path.join(os.path.dirname(__file__),'main-service.json'), scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def just_creds():
    return Credentials.from_service_account_file(os.path.join(os.path.dirname(__file__),'main-service.json'), scopes=SCOPES)

def loader_func(file_id):
    drive_service = get_drive_service()
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh