import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import re
import csv

chromedriver_autoinstaller.install()

service = Service()
driver = webdriver.Chrome(service=service)

def get_id_from_url(url):
    pattern = r"v=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def create_url_get_api(url):
    pre_url = "https://returnyoutubedislikeapi.com/votes?videoId="
    id_video = get_id_from_url(url)
    return pre_url + id_video if id_video else None


# Get comment
def get_information(driver):

    comments_array=[]

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-item-section-renderer#sections.style-scope.ytd-comments")
            )
        )
        for _ in range(10): 
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


def main_function(url):
    try:
        driver.get(url)

        comments_array=get_information(driver)

        # get other details
        url_api = create_url_get_api(url)
        if url_api:
            response = requests.get(url_api)
            if response.status_code == 200:
                data = response.json()
                # print(json.dumps(data, indent=4))  
                likes = data.get('likes', 'N/A')
                dislikes = data.get('dislikes', 'N/A')
                view_count = data.get('viewCount', 'N/A')
                print(f"Likes: {likes}, Unlikes: {dislikes}, Views: {view_count}")
            else:
                print(f"Can not get data from API. Error status: {response.status_code}")
        else:
            print("URL is not valid or can not extract video.")

        return likes,dislikes,view_count,comments_array
        
    except Exception as e:
        print(f"Error in main function for video URL {url}: {e}")
        return None, None, None, []

if __name__ == "__main__":
    urls=['https://www.youtube.com/watch?v=2Jo1So7NDXE',"https://www.youtube.com/watch?v=WfcnA46qkGc",]
    
    with open("../data/youtube_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Url","Likes", "Dislikes", "Views", "Comments"])  

        for url in urls:
            likes, dislikes, view_count, comments_array = main_function(url)
            writer.writerow([url,likes, dislikes, view_count, comments_array])  

    print("Data written to youtube_data.csv successfully.")

    driver.quit()
