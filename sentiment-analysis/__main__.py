import requests
import json


searchterm = "United Kingdom"
sortSetting = "latest"
language = "en"
blueskyURL = ("https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q="
              + searchterm + "?&sort=" + sortSetting + "?&language=" + language)
postData = requests.get(blueskyURL).json()

filtered_posts = [
    {
        "displayName": post["author"]["displayName"],
        "createdAt": post["record"]["createdAt"],
        "text": post["record"]["text"]
    }
    for post in postData["posts"]
]


print(json.dumps(filtered_posts, indent=1))
