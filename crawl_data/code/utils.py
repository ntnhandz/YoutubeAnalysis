import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import csv


def create_driver():
    chromedriver_autoinstaller.install()
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    # options.add_argument('--no-sandbox') 
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('user-agent=Mozilla/5.0 (Win
    driver = webdriver.Chrome(service=service, options=options)
    return driver
    

def get_id_from_url(url):
    pattern = r"v=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# create url api video
def create_url_api_video(url):
    pre_url = "https://returnyoutubedislikeapi.com/votes?videoId="
    id_video = get_id_from_url(url)
    return pre_url + id_video if id_video else None

# get comment
def get_comments_from_video(driver):
    comments_array = []
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-item-section-renderer#sections.style-scope.ytd-comments")
            )
        )
        for _ in range(20): 
            driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")  
            time.sleep(0.6) 

        main_div = driver.find_element(
            By.CSS_SELECTOR, "ytd-item-section-renderer#sections.style-scope.ytd-comments"
        )
        div_comments = main_div.find_elements(By.CSS_SELECTOR, "yt-attributed-string#content-text > span.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap")
        print(f"Number of comments: {len(div_comments)}")
        for div_comment in div_comments:
            print(div_comment.text)
            comments_array.append(div_comment.text)

    except Exception as e:
        print(f"Error during getting comments: {e}")
        
    return comments_array

# get details from video
def get_details_from_video(url_api):
    date_created = likes = dislikes = view_count = rating = deleted = "N/A"
    if url_api:
        response = requests.get(url_api)
        if response.status_code == 200:
            data = response.json()
            date_created = data.get("dateCreated", "N/A")
            likes = data.get('likes', 'N/A')
            dislikes = data.get('dislikes', 'N/A')
            view_count = data.get('viewCount', 'N/A')
            rating = data.get("rating", "N/A")
            deleted = data.get("deleted", "N/A")  
            print(f"Date created: {date_created}, Likes: {likes}, Unlikes: {dislikes}, Views: {view_count}, Rating: {rating}, Deleted: {deleted}")
        else:
            print(f"Can not get data from API. Error status: {response.status_code}")
    else:
        print("URL is not valid or can not extract video.")
    
    return date_created, likes, dislikes, view_count, rating, deleted



# find space
def extract_until_space(text):
    space_index = text.find(' ')
    if space_index == -1:
        return text
    return text[:space_index]

# extract channel name
def extract_channelname(url):
    if "@" in url:
        return url.split("@")[1].split("/")[0]
    return None

# custom like
def convert_string_to_number(text):
    text = text.replace(',', '.')
    if 'K' in text:
        number = float(text.replace('K', ''))
        return int(number * 1000)
    elif 'M' in text:
        number = float(text.replace('M', ''))
        return int(number * 1000000)
    elif 'T' in text:
        number = float(text.replace('M', ''))
        return int(number * 1000000000)
    else:
        return int(float(text))
    

# scroll page
def scroll_down_page(driver, scroll_pause_time=2, max_scrolls=100):
    """Scroll down the page to load all the content."""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(scroll_pause_time) 
        
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_header_from_channel(driver,url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".page-header-view-model-wiz__page-header-headline-info"))
        )
        main_div = driver.find_element(By.CSS_SELECTOR, ".page-header-view-model-wiz__page-header-headline-info")
        channel_name=main_div.find_element(By.CSS_SELECTOR,".dynamic-text-view-model-wiz__h1").text
        channel_image=driver.find_element(By.CSS_SELECTOR,"img.yt-core-image.yt-spec-avatar-shape__image.yt-core-image--fill-parent-height.yt-core-image--fill-parent-width.yt-core-image--content-mode-scale-to-fill.yt-core-image--loaded").get_attribute("src")
        # print(channel_image)

        core_information_div=main_div.find_element(By.CSS_SELECTOR,".page-header-view-model-wiz__page-header-content-metadata.yt-content-metadata-view-model-wiz.yt-content-metadata-view-model-wiz--inline")
        # print(core_information_div.text)
        lines=core_information_div.text.split('\n')
        info = [line.strip('•') for line in lines if line.strip() and line != '•']
        channel_id= info[0]

        channel_num_subcribers=info[1]
        channel_num_subcribers=extract_until_space(channel_num_subcribers)
        channel_num_subcribers=convert_string_to_number(channel_num_subcribers)

        channel_videos=info[2]
        channel_videos=extract_until_space(channel_videos)
        channel_videos=convert_string_to_number(channel_videos)

        # channel_introduction=main_div.find_element(By.CSS_SELECTOR,"span.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap").text
        # print(channel_introduction)
        return channel_name,channel_id,channel_num_subcribers,channel_videos,channel_image
    except Exception as e:
        print(f"Error get header data: {e}")

# get all href a in channel
def get_all_videos_in_videos_page(channel_id,driver):
    try:
        url_video=f"https://www.youtube.com/{channel_id}/videos?app=desktop"
        driver.get(url_video)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#contents.style-scope.ytd-rich-grid-renderer"))
        )
        
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        main_div=driver.find_element(By.CSS_SELECTOR,"#contents.style-scope.ytd-rich-grid-renderer")
        
        all_div_a=main_div.find_elements(By.CSS_SELECTOR,"a#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail")
        
        hrefs_arr=[]
        #print(len(all_div_a))
        for div_a in all_div_a:
            #print(div_a.get_attribute("href"))
            hrefs_arr.append(div_a.get_attribute("href"))
       
        return hrefs_arr

    except Exception as e:
        print(f"Error video page function: {e}")
        return None