from selenium import webdriver  
import time
import os
import re
import shutil

fall_guys_url = "https://www.twitch.tv/directory/game/Fall%20Guys/clips?range=7d"

def getclips(url):
    """Download the top clips on twitch and save it into DownloadedVideos directory

    Args:
        url (String): The url of a given game clip
    """
    # Making sure the working director is core
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    chromeOptions = webdriver.ChromeOptions()
    video_download_directory = os.getcwd().replace('core', 'DownloadedVideos')

    prefs = {
    "download.default_directory": video_download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }

    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path='..\\chromedriver', chrome_options=chromeOptions)

    driver.get(url)
    time.sleep(1)
    all_clips = driver.find_elements_by_xpath("//a[@class='tw-full-width tw-interactive tw-link tw-link--hover-underline-none tw-link--inherit']")
    print(f"Total clips found: {len(all_clips)}")
    all_clips = get_all_hrefs(all_clips)

    video_url_lst = []

    # TODO: Remove before implementing the moviepy
    clean_download_directory(video_download_directory)

    for clip_href in all_clips[0:4]:
        print(f"Opening Clip: {clip_href}")
        driver.get(clip_href)
        time.sleep(1)
        video_url = driver.find_element_by_xpath("//video").get_attribute("src")
        video_url_lst.append(clip_href)
        download_file(driver,video_url, video_download_directory)
        time.sleep(2)

    rename_files(video_download_directory, video_url_lst)

def rename_files(dir,url_lst):
    os.chdir(dir)
    files = os.listdir(".")
    files.sort(key=os.path.getctime)
    creator_names_lst = []
    count = 0
    for i in range(0,len(files)):
        creator_name = re.split('tv/|/clip',url_lst[i])[1]
        if creator_name not in creator_names_lst:
            creator_names_lst.append(creator_name)
            os.rename(files[i],creator_name+"_.mp4")
        else:
            count += 1
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
    # TODO: Rename file, strip the url to get the content creator name
    driver.get(video_url)
    start = time.time()
    
    finished = False
    file_name = ""

    while not finished and time.time() < start + 60:
        finished = True
        files = os.listdir(dir)
        for file in files:
            if re.search(r'crdownload', file):
                file_name = file.split(".crdownload")[0]
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
    getclips(fall_guys_url)


    