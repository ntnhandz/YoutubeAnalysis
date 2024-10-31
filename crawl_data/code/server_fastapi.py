from crawl_each_channel import main_function as crawl_channel_function
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
        writer.writerow(["Url","Likes", "Dislikes", "Views", "Comments"])  

        likes, dislikes, view_count, comments_array = crawl_video_function(url)
        writer.writerow([url,likes, dislikes, view_count, comments_array])  

    print(f"Data written to {video_id} successfully.")
    
    
    
