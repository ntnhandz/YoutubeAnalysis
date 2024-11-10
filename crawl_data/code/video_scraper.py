
from utils import create_driver,create_url_api_video,get_comments_from_video,get_details_from_video
import csv

def main_function_scrape_video(url):
    try:
        driver=create_driver()
        driver.get(url)
        url_api_video = create_url_api_video(url)

        comments_array=get_comments_from_video(driver)
        date_created,likes,dislikes,view_count,rating,deleted = get_details_from_video(url_api_video)

        return date_created,likes,dislikes,view_count,rating,deleted,comments_array
        
    except Exception as e:
        print(f"Error in main function for video URL {url}: {e}")
        return None,None,None,None, None, None, []
    
    finally:
        driver.quit()
        

if __name__ == "__main__":
    urls=['https://www.youtube.com/watch?v=2Jo1So7NDXE',"https://www.youtube.com/watch?v=WfcnA46qkGc","https://www.youtube.com/watch?v=YexFEXRzsbM"]
    
    with open("../data/youtube_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Url","Date created","Likes", "Dislikes", "Views", "Rating","Deleted","Comments"])  

        for url in urls:
            date_created,likes, dislikes, view_count, rating, deleted, comments_array = main_function_scrape_video(url)
            writer.writerow([url,date_created,likes, dislikes, view_count,rating,deleted, comments_array])  

    print("Data written to youtube_data.csv successfully.")