from core.bin.movie import render
from core.bin.extractclips import getclips,clean_download_directory
from core.bin.upload_video import upload
import os 
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename='MainLogFile.log', format='%(levelname)s: %(asctime)s : main.py : %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
logger = logging.getLogger(__name__)


dir = os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())
logger.info("="*65)
logger.info(os.getcwd())

url_dict = {"fall_guys" : " ",
            "league" : "https://www.twitch.tv/directory/game/League%20of%20Legends/clips?range=7d",
            "valorant" : "https://www.twitch.tv/directory/game/VALORANT/clips?range=7d"}


# Ideal positions: Fall guy - topcenter | League - topleft
position = {"topleft":"x=10:y=10",
            "topcenter":"x=(w-text_w)/2:y=10",
            "topright":"x=w-tw-10:y=10",
            "center":"x=(w-text_w)/2:y=(h-text_h)/2",
            "bottomleft":"x=10:y=h-th-10",
            "bottomcenter":"x=(w-text_w)/2:y=h-th-10",
            "bottomright":"x=w-tw-10:y=h-th-10"}

if __name__ == "__main__":
    start_time = time.time()

    # Edit
    game_type = "valorant"
    url = url_dict[game_type]
    num_clips = 10
    text_position = position["topleft"]

    render_name = f"{game_type}_{str(num_clips)}clips_{str(datetime.now()).split()[0]}.mp4"

    # Begin
    logger.info("Starting main.py script")
    getclips(url, num_clips)
    render(render_name,text_position)
    clean_download_directory(os.getcwd())

    # Must follow the two naming convention:
    ## TitleDescription file: 'youtube_infos.json
    ## Thumbnail file: 'thumbnail.jpg'
    #upload(f"Rendered\\{render_name}") 

    print("--- %s seconds ---" % (time.time() - start_time))
    logger.info("--- %s seconds ---" % (time.time() - start_time))