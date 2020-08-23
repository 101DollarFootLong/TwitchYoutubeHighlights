import datetime
from core.bin.Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
import httplib2
import json
import random
import time

def upload_api(media_file):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    CLIENT_SECRET_FILE = f'..\\dependencies\\client_secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    #upload_date_time = datetime.datetime(2020, 8, 23, 11, 20, 0).isoformat() + '.000Z'

    with open("..\\content\\youtube_infos.json") as f:
        data = json.load(f)

    request_body = {
        'snippet': data,
        'status': {
            'selfDeclaredMadeForKids': False, 
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': True
    }

    mediaFile = MediaFileUpload(f"..\\..\\videos\\Rendered\\{media_file}", chunksize=1024*1024, resumable=True)

    print("Uploading the video...")
    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()


    print("Setting the thumbnail")
    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload("..\\content\\thumbnail.jpg")
    ).execute()


