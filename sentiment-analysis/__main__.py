import requests

blueskyURL = "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=tesla?&sort=latest"
postData = requests.get(blueskyURL).json()
print(postData)