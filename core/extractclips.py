from selenium import webdriver  
import time
import os
import re
import shutil
from selenium.webdriver.common.keys import Keys

fall_guys_url = "https://www.twitch.tv/directory/game/Fall%20Guys/clips?range=7d"
league_url = "https://www.twitch.tv/directory/game/League%20of%20Legends/clips?range=7d"
valorant = "https://www.twitch.tv/directory/game/VALORANT/clips?range=7d"

def getclips(url):
    """Download the top clips on twitch and save it into DownloadedVideos directory

    Args:
        url (String): The url of a given game clip
    """
    # Making sure the working director is core
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    video_download_directory = os.getcwd().replace('core', 'DownloadedVideos')
    
    # Chrome
    # chromeOptions = webdriver.ChromeOptions()
    # prefs = {
    # "download.default_directory": video_download_directory,
    # "download.prompt_for_download": False,
    # "download.directory_upgrade": True
    # }
    # chromeOptions.add_experimental_option("prefs",prefs)
    # driver = webdriver.Chrome(executable_path='..\\Dependencies\\chromedriver', chrome_options=chromeOptions)

    # Firefox
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", video_download_directory)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "binary/octet-stream")
    driver = webdriver.Firefox(executable_path='..\\Dependencies\\geckodriver',firefox_profile=profile)

    driver.get(url)
    time.sleep(2)
    # TODO: Find all the English title clips
    all_clips = driver.find_elements_by_xpath("//a[@class='tw-full-width tw-interactive tw-link tw-link--hover-underline-none tw-link--inherit']")
    print(f"Total clips found: {len(all_clips)}")
    all_clips = get_all_hrefs(all_clips)

    video_url_lst = []

    # TODO: Remove before implementing the moviepy
    clean_download_directory(video_download_directory)

    for clip_href in all_clips[2:4]:
        print(f"Opening Clip: {clip_href}")
        driver.get(clip_href)
        time.sleep(1)
        video_url = driver.find_element_by_xpath("//video").get_attribute("src")
        video_url_lst.append(clip_href)
        download_file(driver,video_url, video_download_directory)
        time.sleep(2)

    rename_files(video_download_directory, video_url_lst)

def rename_files(dir,url_lst):
    # TODO: PermissionError: [WinError 32] The process cannot 
    # access the file because it is being used by another process
    
    # Change the directory to the downloadedvideos folder
    os.chdir(dir)
    files = os.listdir(".")
    files.sort(key=os.path.getctime)
    creator_names_lst = []
    prev_creator = ""
    count = 0

    for i in range(0,len(files)):
        # Added the _ at the end of each clip for splitting later
        creator_name = re.split('.tv/|/clip',url_lst[i])[1]
        if creator_name not in creator_names_lst:
            creator_names_lst.append(creator_name)
            os.rename(files[i],creator_name+"_.mp4")
        else:
            # Make sure to increment the right repeting creator
            if prev_creator == creator_name:
                count += 1
            else:
                count = 1

            prev_creator = creator_name
            os.rename(files[i],creator_name+ "_" +str(count)+".mp4")
        

def download_file(driver, video_url, dir):
    """
    Waits for Chrome to finish downloading the file  
    Chrome first downloads the file with an extension of .crdownloaded which is renamed on completion
    Args:
        driver (chromedriver object): The current chrome driver
        video_url (String): A .mp4 video url
        dir (String): The directory for the downloaded videos
    """
    # Fix the failed to download file by switching to firefox browser
    # Add a new window when try to download the mp4 file. 
    driver.execute_script(f"window.open('{video_url}','_blank')")
    time.sleep(2)
    start = time.time()
    
    finished = False
    file_name = ""

    while not finished and time.time() < start + 60:
        finished = True
        files = os.listdir(dir)
        for file in files:
            if re.search(r'.part', file):
                #file_name = file.split(".crdownload")[0]
                file_name = file.split(".part")[0]
                finished = False

def clean_download_directory(dir):
    """
    Given a directory path remove all mp4 files
    Args:
        dir (String): The directory for the downloaded videos
    """
    
    print("Cleaning your directory!!")
    filelist = [ f for f in os.listdir(dir) if f.endswith(".mp4") ]
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
    
if __name__ == "__main__":
    getclips(valorant)


    