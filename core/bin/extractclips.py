from selenium import webdriver  
import time
import os
import re
import shutil
import logging

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Setting logger 
logger = logging.getLogger(__name__)

# gloabl dict
creator_names_dict = {}

oringal_window = ''

def getclips(url,num_clip):
    """Download the top clips on twitch and save it into Videos\\DownloadedVideos directory

    Args:
        url (String): The url of a given game clip
    """
    
    # print(f"getclips: {os.getcwd()}")
    logger.info(f"Calling getclips(): {os.getcwd()}")

    # Making sure the working director is core
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    video_download_directory = os.getcwd().replace('core\\bin', 'videos\\Downloaded')


    # Firefox
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", video_download_directory)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "binary/octet-stream")
    driver = webdriver.Firefox(executable_path='..\\dependencies\\geckodriver',firefox_profile=profile)

    driver.get(url)
    #oringal_window = driver.window_handles[0]
    logger.info(f"Opening starting url: {url}")

    try:
        time.sleep(1)
        clips_table = wait_for_element(driver, By.XPATH, "//div[@class='tw-flex-wrap tw-tower tw-tower--300 tw-tower--gutter-xs']")
        all_clips = driver.find_elements_by_xpath("//a[@class='tw-full-width tw-interactive tw-link tw-link--hover-underline-none tw-link--inherit']")
    except Exception as e:
        print(f"Could not find the clips table. Error: {e}")
        logger.error(f"Could not find the clips table. Error: {e}")
        return

    # TODO: Guard for 0 clips found
    print(f"Total clips found: {len(all_clips)}")
    logger.info(f"Total clips found: {len(all_clips)}")

    all_clips = get_all_hrefs(all_clips)
    video_url_lst = []

    # TODO: Remove before implementing the moviepy
    # clean_download_directory(video_download_directory)

    for clip_href in all_clips[0:num_clip]:
        print(f"Opening Clip: {clip_href}")
        logger.info(f"Opening Clip: {clip_href}")
        driver.get(clip_href)

        try:
            video_tag = wait_for_element(driver, By.XPATH, "//video")
            time.sleep(1)
            video_url = video_tag.get_attribute("src")
        except Exception as e:
            print(f"Could not find the video tag. Error: {e}")
            logger.error(f"Could not find the video tag. Error: {e}")
            return
        
        video_url_lst.append(clip_href)
        #creator_names_dict = {}
        download_file(driver,clip_href,video_url, video_download_directory)
        time.sleep(2)

    logger.info(f"{len(video_url_lst)} video urls: {video_url_lst}")

    # Clean out the empty files 
    clean_download_directory(video_download_directory,"empty")

    driver.quit()

# def rename_files(dir,url_lst):
#     # TODO: PermissionError: [WinError 32] The process cannot 
#     # access the file because it is being used by another process
    
#     # Change the directory to the Videos\\DownloadedVideos folder
#     os.chdir(dir)
#     files = os.listdir(".")
#     files.sort(key=os.path.getctime)
#     creator_names_dict = {}

#     for i in range(0,len(files)):
#         try: 
#             # Added the _ at the end of each clip for splitting later
#             creator_name = re.split('.tv/|/clip',url_lst[i])[1]
#             if creator_name not in creator_names_dict:
#                 creator_names_dict[creator_name] = 1
#                 os.rename(files[i],creator_name+"_.mp4")
#             else:
#                 # Make sure to increment the right repeting creator

#                 creator_names_dict[creator_name] = creator_names_dict[creator_name] + 1
#                 current_count = creator_names_dict[creator_name] 
#                 os.rename(files[i],creator_name+ "_" +str(current_count)+".mp4")
#         except IndexError as e:
#             print(f"Rename issue: {e}")
#             logger.error(f"Rename issue: {e}")
#             return

def rename_files(dir,file,clip_href,url_lst):
    # TODO: PermissionError: [WinError 32] The process cannot 
    # access the file because it is being used by another process
    os.chdir(dir)
    try: 
        # Added the _ at the end of each clip for splitting later
        creator_name = re.split('.tv/|/clip',clip_href)[1]
        if creator_name not in creator_names_dict:
            creator_names_dict[creator_name] = 1
            os.rename(file,creator_name+"_.mp4")
        else:
            # Make sure to increment the right repeting creator

            creator_names_dict[creator_name] = creator_names_dict[creator_name] + 1
            current_count = creator_names_dict[creator_name] 
            os.rename(file,creator_name+ "_" +str(current_count)+".mp4")
        
    except IndexError as e:
        print(f"Rename issue: {e}")
        logger.error(f"Rename issue: {e}")
        return
        
def download_file(driver, clip_href,video_url, dir):
    """
    Waits for Chrome to finish downloading the file  
    Chrome first downloads the file with an extension of .crdownloaded which is renamed on completion
    Args:
        driver (chromedriver object): The current chrome driver
        video_url (String): A .mp4 video url
        dir (String): The directory for the downloaded videos
    """
    previous_dir = os.listdir(dir)
    # Fix the failed to download file by switching to firefox browser
    # Add a new window when try to download the mp4 file.

    # list_of_windows = driver.window_handles
    # if len(list_of_windows) > 1:
    #     for handle in list_of_windows:
    #         if handle != oringal_window:
    #             driver.switch_to.window(window_name=driver.window_handles[handle])
    #             driver.close()
    #     driver.switch_to.window(window_name=oringal_window)

    logger.info("Attempting to download the file")
    # driver.execute_script(f"window.open('{video_url}')")
    driver.execute_script(f"window.open('{video_url}')")
    # driver.execute_script("window.open()")
    # driver.switch_to.window(driver.window_handles[-1])
    # print(video_url)
    # driver.get(video_url)
    # driver.close()
    # driver.switch_to.window(driver.window_handles[-1])

    time.sleep(2)
    time_out = time.time() + 60
    
    finished = False

    while not finished and time.time() < time_out:
        finished = True
        files = os.listdir(dir)
        for file in files:
            if re.search(r'.part', file):
                finished = False

    after_dir = os.listdir(dir)
    diff_lst = list(set(after_dir) - set(previous_dir))
    if finished and len(diff_lst) == 1:
        print(diff_lst[0])
        rename_files(dir,str(diff_lst[0]),clip_href,video_url)
    else:
        print(f"Error: Download didn't finish after 60 seconds. URL: {video_url}")
        logger.error(f"Download didn't finish after 60 seconds. URL: {video_url}")
        return

def clean_download_directory(dir, deletetype="mp4"):
    """
    Given a directory path remove all mp4 files
    Args:
        dir (String): The directory for the downloaded videos
    """
    if deletetype == "mp4":
        print("Cleaning out all .mp4 files!!")
        logger.info("Cleaning your directory!!")
        filelist = [ f for f in os.listdir(dir) if f.endswith(".mp4") ]
        for f in filelist:
            os.remove(os.path.join(dir, f))

    # clean out empty files
    if deletetype == "empty":
        print("Cleaning empty files")
        logger.info("Cleaning your directory!!")
        filelist = [f for f in os.listdir(dir) if os.stat(f).st_size == 0]
        for f in filelist:
            os.remove(os.path.join(dir, f))

def get_all_hrefs(clip_list):
    """
    Given a list of a-tags return a list of hrefs
    Args:
        clip_list (List): A list of chromedriver objects
    """  
    href_lst = []
    for clip in clip_list:
        href_lst.append(clip.get_attribute("href"))
    return href_lst

def wait_for_element(driver,
                        by_type,
                        element,
                        timeout=10,
                        condition=EC.presence_of_element_located):
      """
      Wait for the presence of an element to appear on the page
      The element can be referenced by any type supported by the 'By' class
      :param driver:
      :param by_type:
      :param element:
      :param timeout:
      :param condition:
      :return:
      """
      try:
        element = WebDriverWait(driver, timeout).until(
          condition((by_type, element))
        )
        return element
      except TimeoutException:
        return None




    