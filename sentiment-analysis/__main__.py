import requests
import json
import csv
from datetime import datetime

def GetPostsFromSearch(searchterm, sortSetting, language):
    # Fix the URL construction - using proper query parameter format
    blueskyURL = "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"
    params = {
        "q": searchterm,
        "sort": sortSetting,
        "language": language,
        "limit": "100"
    }
    # Make the request with separate params dictionary
    response = requests.get(blueskyURL, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        postData = response.json()

        filtered_posts = [
            {
                "displayName": post["author"]["displayName"],
                "createdAt": post["record"]["createdAt"],
                "text": post["record"]["text"]
            }
            for post in postData["posts"]
        ]

        print(json.dumps(filtered_posts, indent=1))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


    for post in filtered_posts:
        # Parse the ISO format date
        dt = datetime.fromisoformat(post["createdAt"].replace("Z", "+00:00"))
        # Format as YYYY-MM-DD HH:MM:SS
        post["createdAt"] = dt.strftime("%d-%m-%Y %H:%M:%S")
    with open('data/postData.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['displayName', 'createdAt', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for post in filtered_posts:
            writer.writerow(post)
    print("CSV file 'postData.csv' has been created successfully.")


def GetPostsFromHandle():
    blueskyURL = "https://api.bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
    params = {
        "actor": "linusmediagroup.com",
        "limit": "100"
    }
    response = requests.get(blueskyURL, params=params)

    if response.status_code == 200:
        postData = response.json()
        print(json.dumps(postData, indent=1))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    GetPostsFromSearch("Cambridge", "top", "en")
    #GetPostsFromHandle()

if __name__ == '__main__':
    main()

