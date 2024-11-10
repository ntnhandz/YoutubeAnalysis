
from utils import create_driver,get_header_from_channel,get_all_videos_in_videos_page


def main_function_scrape_channel(url):
    try:
        
        driver=create_driver()

        channel_name,channel_id,channel_num_subcribers,channel_videos,channel_image=get_header_from_channel(driver,url)
        print(channel_name,channel_id,channel_num_subcribers,channel_videos,channel_image)

        arr_hrefs = get_all_videos_in_videos_page(channel_id,driver)
        return arr_hrefs
        
    except Exception as e:
        print(f"Error main function: {e}")
    finally:
        driver.quit()
        

if __name__=="__main__":
    url = "https://www.youtube.com/@Web5Ngay"
    main_function_scrape_channel(url)