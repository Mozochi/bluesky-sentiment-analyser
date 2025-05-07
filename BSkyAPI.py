import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd


def get_posts_from_search(search_term, sort_setting, language):
    """
    Function fetches posts from the Bluesky Endpoint based on a search term.

    Parameters:
    search_term (str): Search term to look for in posts.
    Sort_setting (str): Options: "top" or "latest". Default is "latest"
    language (str): # Uses IETF language subtags. Default is "en" (English).

    Returns:
    None.

    """

    language, search_term, sort_setting = validate_search_parameters(language, search_term, sort_setting)

    bluesky_post_search_url = "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"
    params = {
        "q": search_term,
        "sort": sort_setting,
        "language": language,
        "limit": "100" # The Number of posts to return, between 1 and 100. Default value is 25.
    }

    # Make the GET request to the Bluesky API
    try:
        response = requests.get(bluesky_post_search_url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return pd.DataFrame() # Return an empty dataframe on error
    
    post_data = response.json()
    filtered_posts = []

    if "posts" in post_data and isinstance(post_data["posts"], list):
        for post_item in post_data["posts"]:
            # Checking if post_item is a dictionary
            if not isinstance(post_item, dict):
                continue
            author_info = post_item.get("author")
            record_info = post_item.get("record")

            # Checking author_info and record_info are dictionaries before trying to get sup-keys
            if not isinstance(author_info, dict) or not isinstance(record_info, dict):
                continue
        
            display_name = author_info.get("displayName", "Unknown User")

            created_at_val = record_info.get("createdAt")
            text_val = record_info.get("text")

            if created_at_val is not None and text_val is not None:
                filtered_posts.append({
                    "display_name": display_name,
                    "created_at": created_at_val,
                    "text": text_val
                })
    else:
        print("Warning: 'posts' key not found in API response or is not a list.")

    return pd.DataFrame(filtered_posts)


def validate_search_parameters(language, search_term, sort_setting):
    """
    Function validates the input parameters for the search function.

    Parameters:
    search_term (str): Search term to look for in posts.
    Sort_setting (str): Options: "top" or "latest". Default is "latest"
    language (str): # Uses IETF language subtags. Default is "en" (English).

    Returns:
    search_term (str): Validated search term.
    Sort_setting (str): Validated sort setting.
    language (str): Validated language code.
    """

     # Remove trailing whitespace from the input parameters
    search_term = search_term.strip()
    sort_setting = sort_setting.strip().lower() # Convert to lower once
    language = language.strip().lower() # Convert to lower once
    

    # Validate the sort_setting parameters
    if sort_setting not in ["top", "latest"]:
        # In a GUI context, you'd return an error or use a default
        print("Invalid sort setting. Using default 'latest'.")
        sort_setting = "latest" 

    # Validate the language parameters
    if language not in ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko"]:

        print("Invalid language. Using default 'en'.")
        language = "en"

    # Validate the search_term parameters
    if not search_term: # Check if search term is empty

        print("Warning: Search term is empty.")
    
    print("Input validation (non-interactive for GUI) complete.")
    return language, search_term, sort_setting



def create_csv(filtered_posts):
    """
    Procedure creates a CSV file from the filtered posts.

    Parameters:
    filtered_posts (dict): Contains the filtered posts from the Bluesky API.

    Returns:
    None.

    """

    # Converts createdAt field is in ISO time format
    for post in filtered_posts:
        # Parse the ISO format date
        dt = datetime.fromisoformat(post["created_at"].replace("Z", "+00:00"))
        # Format as YYYY-MM-DD HH:MM:SS
        post["created_at"] = dt.strftime("%d-%m-%Y %H:%M:%S")

    # Create a CSV file and write the filtered posts to it
    with open("post_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        field_names = ["display_name", "created_at", "text"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        for post in filtered_posts:
            writer.writerow(post)

    print("CSV file 'post_data.csv' has been created successfully.")

    # Remove rows with blank text fields and save to a new CSV file "post_data_filtered.csv"
    df = pd.read_csv('post_data.csv')
    df_filtered = df[df["text"].notna() & (df["text"].str.strip() != "")]
    print(f"Removed {df.shape[0] - df_filtered.shape[0]} rows with blank text fields")
    df_filtered.to_csv("post_data_filtered.csv", index=False)

    try:
        os.remove("post_data.csv")
    except FileNotFoundError:
        print("Original file not found, no need to remove.")
    except PermissionError:
        print("Permission denied when trying to remove file.")

def get_posts_from_handle(actor):
    """
    Function fetches posts from the Bluesky Endpoint based on a user handle

    Parameters:
    actor (dict): Handle of the user whose feed you want to fetch

    Returns:
    None.
   """

    #Load authentication variables from .env file
    load_dotenv()
    identifier = os.getenv("IDENTIFIER")
    password = os.getenv("PASSWORD")

    at_proto_auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"

    payload = {
        "identifier": identifier, # Handle/PID of client user
        "password": password # App Password from Bluesky
    }

    # Make the POST request to the authentication endpoint
    try:
        response = requests.post(at_proto_auth_url, json=payload,)
    except requests.exceptions.RequestException as e:
        print("Authentication failed:", response.status_code)
        print(response.text)
    else:
        data = response.json()
        token = data["accessJwt"]

    # Make the GET request to the Bluesky API
    bluesky_url = "https://api.bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
    params = {
        "actor": actor,
        "limit": "100" # The Number of posts to return, between 1 and 100. Default value is 25.
    }
    response = requests.get(bluesky_url, params=params, headers={"authorization": f"Bearer {token}"})

    # Check if the request was successful
    if response.status_code == 200:
        postData = response.json()

        # Filter the posts to only include the createdAt and text fields
        filtered_posts = []
        for item in postData["feed"]:
            if "post" in item and "record" in item["post"]:
                filtered_posts.append({
                    "created_at": item["post"]["record"]["createdAt"],
                    "text": item["post"]["record"]["text"]
                })

        return pd.DataFrame(filtered_posts)

    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def handle_validation(actor):
    """
        Function checks if the handle exists in the Bluesky API.

        Parameters:
        actor (str): Handle of the user whose feed you want to fetch

        Returns:
        actor (str): Validated handle of the user
       """

    actor = actor.strip()
    handle_lookup_url = "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=" + actor

    # Check identity endpoint to ensure that the handle exists
    response = requests.get(handle_lookup_url)

    if response.status_code == 200:
        return True
    else:
        return False

def main():
    get_posts_from_search("Cambridge", "latest", "en")
    #get_posts_from_handle("linusmediagroup.com")

if __name__ == "__main__":
    main()