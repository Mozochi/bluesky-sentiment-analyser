import requests
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd

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

    createCSV(filtered_posts)


def createCSV(filtered_posts):
    for post in filtered_posts:
        # Parse the ISO format date
        dt = datetime.fromisoformat(post["createdAt"].replace("Z", "+00:00"))
        # Format as YYYY-MM-DD HH:MM:SS
        post["createdAt"] = dt.strftime("%d-%m-%Y %H:%M:%S")
    with open('postData.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['displayName', 'createdAt', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for post in filtered_posts:
            writer.writerow(post)
    print("CSV file 'postData.csv' has been created successfully.")

    df = pd.read_csv('postData.csv')
    df_filtered = df[df['text'].notna() & (df['text'].str.strip() != '')]
    print(f"Removed {df.shape[0] - df_filtered.shape[0]} rows with blank text fields")
    df_filtered.to_csv('postData-filtered.csv', index=False)
    os.remove('postData.csv')


def GetPostsFromHandle(actor):
    load_dotenv()
    identifier = os.getenv("IDENTIFIER")
    password = os.getenv("PASSWORD")

    print("Identifier:", identifier)
    print("Password:", password)

    AtProtoAuthURL = "https://bsky.social/xrpc/com.atproto.server.createSession"

    payload = {
        "identifier": identifier,
        "password": password
    }

    response = requests.post(AtProtoAuthURL, json=payload,)

    if response.status_code == 200:
        data = response.json()
        print("Access token:", data["accessJwt"])
        token = data["accessJwt"]
    else:
        print("Authentication failed:", response.status_code)
        print(response.text)

    blueskyURL = "https://api.bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
    params = {
        "actor": actor,
        "limit": "100"
    }
    response = requests.get(blueskyURL, params=params, headers={'authorization': f'Bearer {token}'})

    if response.status_code == 200:
        postData = response.json()

        filtered_posts = []
        for item in postData['feed']:
            if 'post' in item and 'record' in item['post']:
                filtered_posts.append({
                    'createdAt': item['post']['record']['createdAt'],
                    'text': item['post']['record']['text']
                })

        createCSV(filtered_posts)

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    #GetPostsFromSearch("Cambridge", "top", "en")
    GetPostsFromHandle("linusmediagroup.com")

if __name__ == '__main__':
    main()

