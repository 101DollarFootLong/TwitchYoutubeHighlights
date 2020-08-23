# pip install --upgrade youtube-uploader-selenium
# pip install selenium-firefox
from core.bin.youtube_uploader import YouTubeUploader
import os 

def upload_selenium(media_file):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    video_path = f"..\\..\\videos\\Rendered\\{media_file}"
    metadata_path = "..\\content\\youtube_infos.json"

    uploader = YouTubeUploader(video_path, metadata_path)
    was_video_uploaded, video_id = uploader.upload()
    print("asserting")
    assert was_video_uploaded