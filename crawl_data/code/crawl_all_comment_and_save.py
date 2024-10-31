from crawl_each_channel import main_function as crawl_channel_function
from crawl_each_video import *
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield

app=FastAPI(lifespan=lifespan)

class InputUrl(BaseModel):
    url:str
    
@app.get("/")
async def home():
    return "This is tool crawl youtube."

@app.post("/crawl/video")
async def crawl_video_save(input_url:InputUrl):
    text=input_url.url
    
    
