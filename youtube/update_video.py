import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def update_video(youtube, **args):
    videos_list_response = youtube.videos().list(
        id=args.video_id,
        part='snipped'
    ).execute()

    if not videos_list_response['items']:
        print(f"Video {args.video_id} not found")

    videos_list_snippet = videos_list_response['items'][0]['snippet']

    if args.title:
        videos_list_snippet['title'] = args.title
    if args.description:
        videos_list_snippet['description'] = args.description

    if 'tags' not in videos_list_snippet:
        videos_list_snippet['tags'] = []
    if args.tags:
        videos_list_snippet['tags'] = arg.tags.split(',')
    elif args.add_tag:
        videos_list_snippet['tags'].append(args.add_tag)

    video_update_response = youtube.videos().update(
        part='snippet',
        body=dict(
            snippet=videos_list_snippet,
            id=args.video_id)
    )).execute()
