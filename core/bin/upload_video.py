import datetime
from core.bin.Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import json


#print(f"Upload_video.py: {os.getcwd()}")

def upload(media_file):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    with open("..\\content\\youtube_infos.json") as f:
        data = json.load(f)

    request_body = {
        'snippet': data,
        'status': {
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(media_file)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()


    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload("..\\content\\thumbnail.jpg")
    ).execute()
