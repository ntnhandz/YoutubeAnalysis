from crawl_each_channel import main_function as crawl_channel_function,extract_channelname
from crawl_each_video import main_function as crawl_video_function
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
import csv
import re

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield

app=FastAPI(lifespan=lifespan)

class InputUrl(BaseModel):
    url:str
    
@app.get("/")
async def home():
    return "This is tool crawl youtube."

def get_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    if match:
        return match.group(1)
    return None


@app.post("/crawl/video")
async def crawl_video_save(input_url:InputUrl):
    
    url=input_url.url
    video_id=get_video_id(url)
    
    with open(f"../data/data_crawl/{video_id}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Url","Date created","Likes", "Dislikes", "Views", "Rating","Deleted","Comments"])   

        date_created,likes, dislikes, view_count, rating, deleted, comments_array = crawl_video_function(url)
        writer.writerow([url,date_created,likes, dislikes, view_count,rating,deleted, comments_array])   

    print(f"Data written to {video_id} successfully.")
    
    
    
@app.post("/crawl/channel/")
async def crawl_each_channel(input_url:InputUrl):
    
    arr_hrefs=crawl_channel_function(input_url.url)
    filename=extract_channelname(input_url.url)
    with open (f"../data/data_crawl/channel/{filename}.csv",mode="w",newline="",encoding="utf-8") as file:
        
        writer = csv.writer(file)
        writer.writerow(["Url","Date created","Likes", "Dislikes", "Views", "Rating","Deleted","Comments"])   
        
        for href in arr_hrefs:
            video_id=get_video_id(href)
            date_created,likes, dislikes, view_count, rating, deleted, comments_array = crawl_video_function(href)
            writer.writerow([video_id,date_created,likes, dislikes, view_count,rating,deleted, comments_array])   
            
    print(f"Crawl channel {filename} successful!")