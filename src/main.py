from apify import Actor
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
from selenium_stealth import stealth
import json
import requests
from urllib.parse import quote
async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        proxy_settings = actor_input.get('proxySettings')
        proxy_configuration = await Actor.create_proxy_configuration(actor_proxy_input=proxy_settings)
        proxy_url = await proxy_configuration.new_url()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--proxy-server={proxy_url}')
        driver = webdriver.Chrome(options= chrome_options)
        stealth(driver,
                user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
                languages= ["en-US", "en"],
                vendor=  "Google Inc.",
                platform=  "Win32",
                webgl_vendor=  "Intel Inc.",
                renderer=  "Intel Iris OpenGL Engine",
                fix_hairline= False,
                run_on_insecure_origins= False,
                )
        usernames = actor_input.get("usernames")
        for username in usernames:
            print(username)
            url = f'https://instagram.com/{username}/?__a=1&__d=dis'
            driver.get(url)
            print(f"Attempting: {driver.current_url}")
            if "login" in driver.current_url:
                print("Failed/ redir to login")
                driver.quit()
            else:
                print ("Success")
                resp_body = driver.find_element(By.TAG_NAME, "body").text
                data_json = json.loads(resp_body)
                data = data_json['graphql']['user']
                timeline = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]
                video = timeline["is_video"]
                caption = timeline["edge_media_to_caption"]["edges"][0]["node"]["text"]
                thumbnail = timeline["thumbnail_src"]
                url_ig = ""
                if(video==True):
                    url_ig = timeline["video_url"]
                else:
                    url_ig = timeline["display_url"]
            await Actor.push_data({
                        'username': username,
                        'video': video,
                        'caption': caption,
                        'thumbnail': thumbnail,
                        'url': url_ig
                        })
                    


