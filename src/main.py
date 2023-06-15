from apify import Actor
from instagrapi import Client

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        sessionid = actor_input.get('sessionid')
        usernames = actor_input.get('usernames')
        cl = Client()
        cl.login_by_sessionid(sessionid)
        for username in usernames:
            video = False
            user_id = cl.user_id_from_username(username)
            medias = cl.user_medias(user_id, 2)
            captiontext = medias[0].caption_text
            mediatype = medias[0].media_type
            producttype = medias[0].product_type
            url = ""
            print(captiontext)
            
            if mediatype==2 and (producttype=="feed" or producttype=="clips"):
                video = True
                url = medias[0].video_url
                print(url)
                
            if mediatype==1:
                url = medias[0].thumbnail_url
                print(url)
                
            await Actor.push_data({
                        'username': username,
                        'caption': captiontext,
                        'url': url,
                        })
                    
