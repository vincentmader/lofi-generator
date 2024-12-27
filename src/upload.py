#!../.venv/bin/python3

import os
import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Paths
CREDENTIALS_FILE = "../tmp/credentials.json"  # Replace with the path to your credentials file
TOKEN_FILE = "../tmp/token.pickle"  # OAuth token will be saved here
SONGS_DIR = "../tmp/generated_songs"

# OAuth Scopes for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

#def authenticate_youtube():
#    """Authenticate to YouTube API."""
#    creds = None
#    if os.path.exists(TOKEN_FILE):
#        with open(TOKEN_FILE, "rb") as token:
#            creds = pickle.load(token)
#    if not creds or not creds.valid:
#        if creds and creds.expired and creds.refresh_token:
#            creds.refresh(Request())
#        else:
#            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#            creds = flow.run_console()
#        with open(TOKEN_FILE, "wb") as token:
#            pickle.dump(creds, token)
#    return build("youtube", "v3", credentials=creds)

from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_youtube():
    # Scopes for the YouTube Data API
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    
    # Create the flow using the client secrets file
    flow = InstalledAppFlow.from_client_secrets_file(
        # "client_secrets.json", SCOPES
        CREDENTIALS_FILE , SCOPES
    )
    
    # This will run a local server for authentication
    creds = flow.run_local_server(port=8080)  # port=0 will automatically pick an available port
    
    return creds

def upload_to_youtube(youtube, video_file, title, description, tags, category="10", privacy_status="public"):
    """
    Upload a video to YouTube.
    :param youtube: Authenticated YouTube service
    :param video_file: Path to video file
    :param title: Video title
    :param description: Video description
    :param tags: List of tags
    :param category: YouTube category (default is 10: Music)
    :param privacy_status: Privacy status (public, private, unlisted)
    """
    try:
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            },
            "status": {
                "privacyStatus": privacy_status,
            },
        }

        media_file = open(video_file, "rb")
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=video_file,
        )
        response = request.execute()
        print(f"Uploaded: {title}")
        return response
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Authenticate to YouTube
    youtube = authenticate_youtube()

    # Loop through songs and upload them
    #for i, song in enumerate(os.listdir(SONGS_DIR), start=1):
    #    if not song.endswith(".wav"):
    #        continue
    #    song_path = os.path.join(SONGS_DIR, song)

    #    # Random title, description, and tags
    #    title = f"Lo-Fi Chill Track #{i}"
    #    description = "Relax and enjoy this unique Lo-Fi track. Perfect for study and focus. 🎵"
    #    tags = ["Lo-Fi", "Chill", "Relaxing Music", "Study Music"]

    #    # Upload song to YouTube
    #    upload_to_youtube(
    #        youtube,
    #        video_file=song_path,
    #        title=title,
    #        description=description,
    #        tags=tags,
    #    )

if __name__ == "__main__":
    main()
