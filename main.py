from core.movie import render
from core.extractclips import getclips,clean_download_directory
from core.upload_video import upload
import os 

dir = os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())

fall_guys_url = "https://www.twitch.tv/directory/game/Fall%20Guys/clips?range=7d"
league_url = "https://www.twitch.tv/directory/game/League%20of%20Legends/clips?range=7d"
valorant = "https://www.twitch.tv/directory/game/VALORANT/clips?range=7d"
num_clips = 3

# Ideal positions: Fall guy - topcenter | League - topleft
position = {"topleft":"x=10:y=10",
            "topcenter":"x=(w-text_w)/2:y=10",
            "topright":"x=w-tw-10:y=10",
            "center":"x=(w-text_w)/2:y=(h-text_h)/2",
            "bottomleft":"x=10:y=h-th-10",
            "bottomcenter":"x=(w-text_w)/2:y=h-th-10",
            "bottomright":"x=w-tw-10:y=h-th-10"}

if __name__ == "__main__":
    getclips(valorant, num_clips)
    text_position = position["topleft"]
    render(text_position)
    clean_download_directory(os.getcwd()+"\\DownloadedVideos")
    #upload(None,None,None)