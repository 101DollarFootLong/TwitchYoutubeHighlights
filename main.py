from core.bin.movie import render
from core.bin.extractclips import getclips,clean_download_directory
from core.bin.upload_api import upload_api
from core.bin.upload_selenium import upload_selenium
import os 
import logging
import time
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO, filename='MainLogFile.log', format='%(levelname)s: %(asctime)s : main.py : %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
logger = logging.getLogger(__name__)


dir = os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())
logger.info("="*65)
logger.info(os.getcwd())

url_dict = {"fall_guys" : "https://www.twitch.tv/directory/game/Fall%20guys/clips?range=7d",
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
            
game_text_position = {"fall_guys" : position["topcenter"],
            "league" : position["bottomright"],
            "valorant" : position["topright"]}

if __name__ == "__main__":
    start_time = time.time()

    # Edit contents
    game_type = "fall_guys"
    num_clips = 10
    url = url_dict[game_type]
    text_position = game_text_position[game_type]

    render_name = f"{game_type}_{str(num_clips)}clips_{str(datetime.now()).split()[0]}.mp4"

    # # Begin
    logger.info("Starting main.py script")
    # getclips(url, num_clips)
    # timer_dict = render(render_name,text_position)
    # clean_download_directory(os.getcwd())

    # Must follow the two naming convention:
    ## TitleDescription file: 'youtube_infos.json
    ## Thumbnail file: 'thumbnail.jpg'

    # Add the timers for the desciption
    #timer_dict_str = json.dumps(timer_dict)
    #print(timer_dict_str)
    render_name = "valorant_25clips_2020-08-26.mp4"
    upload_selenium(render_name) 

    print("--- %s seconds ---" % (time.time() - start_time))
    logger.info("--- %s seconds ---" % (time.time() - start_time))

    # TODO: Dynamic video description for youtube