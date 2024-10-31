import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import re
from bs4 import BeautifulSoup
import time

def extract_until_space(text):
    space_index = text.find(' ')
    if space_index == -1:
        return text
    return text[:space_index]

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

def scroll_down_page(driver, scroll_pause_time=2, max_scrolls=50):
    """Scroll down the page to load all the content."""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(scroll_pause_time) 
        
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_header_data(driver,url):
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
        print(len(all_div_a))
        for div_a in all_div_a:
            print(div_a.get_attribute("href"))
       


    except Exception as e:
        print(f"Error video page function: {e}")



def main_function(url):
    try:
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        # extension_path = 'return_dislike_youtube.crx'
        # options.add_extension(extension_path)
        # options.add_argument('--log-level=0')
        driver = uc.Chrome(options=options)

        channel_name,channel_id,channel_num_subcribers,channel_videos,channel_image=get_header_data(driver,url)
        print(channel_name,channel_id,channel_num_subcribers,channel_videos,channel_image)

        get_all_videos_in_videos_page(channel_id,driver)
        
        
    except Exception as e:
        print(f"Error main function: {e}")
    finally:
        driver.quit()

if __name__=="__main__":
    url = "https://www.youtube.com/@Web5Ngay"
    main_function(url)

