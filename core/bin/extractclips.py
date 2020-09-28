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
from selenium.webdriver.firefox.options import Options

# Setting logger 
logger = logging.getLogger(__name__)

# global dict
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

    ## Headless start option
    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(executable_path='..\\dependencies\\geckodriver',firefox_profile=profile, options=options)
    driver.get(url)
    time.sleep(1)

    # Scroll down until we found n number of clips
    wait_for_element(driver, By.XPATH, '//body')
    target =  driver.find_element_by_xpath(f"/html/body/div[1]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div[2]/div[4]/div[1]/div/div/div/div[{num_clip}]")
    driver.execute_script('arguments[0].scrollIntoView(true);', target)

    logger.info(f"Opening starting url: {url}")

    try:
        time.sleep(1)
        wait_for_element(driver, By.XPATH, "//div[@class='tw-flex-wrap tw-tower tw-tower--300 tw-tower--gutter-xs']")
        all_clips = driver.find_elements_by_xpath("//a[@class='tw-full-width tw-interactive tw-link tw-link--hover-underline-none tw-link--inherit']")
    except Exception as e:
        print(f"Could not find the clips table. Error: {e}")
        logger.error(f"Could not find the clips table. Error: {e}")
        return

    # Check for 0 clips found
    if len(all_clips) == 0:
        print(f"Total number of clips found was 0, ending run.")
        return

    print(f"Total clips found: {len(all_clips)}")
    logger.info(f"Total clips found: {len(all_clips)}")

    # Get all the href links
    all_clips = get_all_hrefs(all_clips)
    print(f"List of clips: {all_clips}")
    video_download_urls = []

    # TODO: Remove before implementing the moviepy

    # Clean the directory before trying to download new clips
    clean_download_directory(video_download_directory)

    # Loop through all the video clips found
    for video_url in all_clips[0:num_clip]:
        print(f"Opening Clip: {video_url}")
        logger.info(f"Opening Clip: {video_url}")
        driver.get(video_url)
        time.sleep(2)

        try:
            video_tag = wait_for_element(driver, By.XPATH, "//video")
            download_url = video_tag.get_attribute("src")
        except Exception as e:
            print(f"Could not find the video tag. Error: {e}")
            logger.error(f"Could not find the video tag. Error: {e}")
            continue

        # Sometimes the download_url is an empty string
        if download_url[-4:] != '.mp4':
            print(f"The Download URL was not found, skipping to the next clip.")
            continue
        
        video_download_urls.append(download_url)
        #creator_names_dict = {}           
        download_sucessful = download_file(driver,download_url,video_url, video_download_directory)

        if download_sucessful:
            print(f"Download successful.")      
        else:
            print(f"Download failed. Skipping to next clip.")


    # logger.info(f"{len(video_url_lst)} video urls: {video_url_lst}")

    # Clean out the empty files 
    clean_download_directory(video_download_directory,"empty")

    downloaded_files_num = len(os.listdir(video_download_directory))
    print(f"Total number of file downloaded: {str(downloaded_files_num)}")
    logger.info(f"Total number of file downloaded: {str(downloaded_files_num)}")

    driver.quit()

def rename_files(dir,file,clip_href,url_lst):
    # TODO: PermissionError: [WinError 32] The process cannot 
    # access the file because it is being used by another process
    os.chdir(dir)
    output_name = ""
    try: 
        # Added the _ at the end of each clip for splitting later
        creator_name = re.split('.tv/|/clip',clip_href)[1]
        if creator_name not in creator_names_dict:
            creator_names_dict[creator_name] = 1
            output_name = creator_name+"_.mp4"
            os.rename(file,output_name)
            print(f"Renaming {file} -> {output_name}")
            logger.info(f"Renaming {file} -> {output_name}")
        else:
            # Make sure to increment the right repeting creator

            creator_names_dict[creator_name] = creator_names_dict[creator_name] + 1
            current_count = creator_names_dict[creator_name] 
            output_name = creator_name+ "_" +str(current_count)+".mp4"
            os.rename(file,output_name)

            print(f"Renaming {file} -> {output_name}")
            logger.info(f"Renaming {file} -> {output_name}")
    except IndexError as e:
        print(f"Rename issue: {e}")
        logger.error(f"Rename issue: {e}")
        return
        
def download_file(driver, download_url,video_url, dir):

    """
    Waits for Firefox to finish downloading the file  
    Firefox first downloads the file with an extension of .part which is renamed on completion
    Args:
        driver: The current Firefox driver
        download_url (String): A .mp4 url
        video_url: The URL to the clip we are trying to to download
        dir (String): The directory for the downloaded videos
    """

    # Get list of files before trying to download
    previous_dir = os.listdir(dir)

    # Open the .mp4 URL to start the download
    logger.info(f"Attempting to download the file for clip: {video_url}")
    driver.execute_script(f"window.open('{download_url}')")
    time.sleep(2)

    time_out = time.time() + 60
    
    finished = False

    # Loop until the download is finished or timesout 
    while not finished and time.time() < time_out:
        finished = True
        files = os.listdir(dir)
        for file in files:
            if re.search(r'.part', file):
                finished = False

    # Get list of files after downloading the file
    after_dir = os.listdir(dir)

    # Get the difference betwen before and after lists
    diff_lst = list(set(after_dir) - set(previous_dir))

    # If the difference is 1 then the download was compelted
    if finished and len(diff_lst) == 1:
        rename_files(dir,str(diff_lst[0]),video_url,download_url)
        return True
    else:
        print(f"Error: Download didn't finish after 60 seconds. URL: {video_url}")
        logger.error(f"Download didn't finish after 60 seconds. URL: {video_url}")
        return False


def clean_download_directory(dir, deletetype="mp4"):
    """
    Given a directory path remove all mp4 files
    Args:
        dir (String): The directory for the downloaded videos
    """
    if deletetype == "mp4":
        print(f"dir {dir}")
        print("Cleaning out all .mp4 files!!")
        logger.info("Cleaning your directory!!")
        filelist = [ f for f in os.listdir(dir) if f.endswith(".mp4") ]
        for f in filelist:
            # PermissionError: [WinError 32] The process cannot access the file because it is being used by another process:
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
        try:
            href_lst.append(clip.get_attribute("href"))
        except Exception as e:
            continue
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

    


    