import requests
import json
import re

def get_id_from_url(url):
    pattern = r"v=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def create_url_get_api(url):
    pre_url = "https://returnyoutubedislikeapi.com/votes?videoId="
    id_video = get_id_from_url(url)
    return pre_url + id_video if id_video else None


url_api = create_url_get_api("https://www.youtube.com/watch?v=h6RONxjPBf4")
if url_api:
    response = requests.get(url_api)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4)) 
