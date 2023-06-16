from apify import Actor
from instagrapi import Client
import json
import httpx
from urllib.parse import quote
client = httpx.Client(
    headers={
        # this is internal ID of an instegram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

async def scrape_user(username: str):
    """Scrape Instagram user's data"""
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    print("result: " + str(result))
    data = json.loads(result.content)
    timeline = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]
    video = timeline["is_video"]
    caption = timeline["edge_media_to_caption"]["edges"][0]["node"]["text"]
    thumbnail = timeline["thumbnail_src"]
    url = ""
    if(video==True):
        url = timeline["video_url"]
    else:
        url = timeline["display_url"]
    result = dict()
    result["video"] = video
    result["caption"] = caption
    result["thumbnail"] = thumbnail
    result["url"] = url
    return result

print(scrape_user("bmwdesigned"))


async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        usernames = actor_input.get("usernames")
        for username in usernames:
            data = await scrape_user(username)      
            await Actor.push_data({
                        'username': username,
                        'video': data["video"],
                        'caption': data["caption"],
                        'thumbnail': data["thumbnail"],
                        'url': data["url"]
                        })
                    


