import requests
import html
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
load_dotenv(".env")


def get_comments(video_url):

    video_id = parse_qs(urlparse(video_url).query)["v"][0]


    api_key=os.getenv("YOUTUBE_API_KEY")
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    
    all_comments = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "pageToken": next_page_token,
            "key": api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        for item in data.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comment_data = {
                "text": html.unescape(snippet["textDisplay"]),
            }

            all_comments.append(comment_data)

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break


    return all_comments