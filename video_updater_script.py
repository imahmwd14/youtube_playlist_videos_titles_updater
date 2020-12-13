# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = [
    "https://www.googleapis.com/auth/youtubepartner",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]


# %%
playlist_ID = ""
string_to_add_to_titles = ""


# %%
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


# %%
request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=100,
        playlistId=playlist_ID,
        prettyPrint=True,
        pageToken=""
    )


# %%
response = request.execute()


# %%
video_ids = []
responses = [response]


# %%
curr_token = response['nextPageToken']
curr_res = response
while 'nextPageToken' in curr_res:
    curr_res = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=100,
            playlistId=playlist_ID,
            prettyPrint=True,
            pageToken=curr_token
        ).execute()
    responses += [curr_res]
    curr_token = curr_res['nextPageToken']


# %%
video_ids = []
for res in responses:
    for i in res['items']:
        video_ids += [i['snippet']['resourceId']['videoId']]


# %%
for v_id in video_ids:
    print(v_id)


# %%
videos_responses = []


# %%
for vId in video_ids:
    videos_responses += [youtube.videos().list(
        part="snippet,contentDetails",
        id=vId
    ).execute()]


# %%
len(videos_responses)


# %%
print('-----')
videos_responses[0]['items'][0]['snippet']
videos_responses[0]['items'][0]


# %%
for v in videos_responses:
    v['items'][0]['snippet']['title'] = v['items'][0]['snippet']['title'].strip() + string_to_add_to_titles


# %%
# for num in range(len(videos_responses)):
#     try:
#         youtube.videos().update(
#             part="snippet",
#             body={
#                 "id": videos_responses[num]['items'][0]['id'],
#                 "snippet": {
#                     "categoryId": videos_responses[num]['items'][0]['snippet']['categoryId'],
#                     "defaultLanguage": videos_responses[num]['items'][0]['snippet']['defaultLanguage'],
#                     "description": videos_responses[num]['items'][0]['snippet']['description'],
#                     "tags": videos_responses[num]['items'][0]['snippet']['tags'],
#                     "title": videos_responses[num]['items'][0]['snippet']['title']
#                 }
#             }
#         ).execute()
#     except:
#         pass


# %%
{
        "id": videos_responses[0]['items'][0]['id'],
        "snippet": {
            "categoryId": videos_responses[0]['items'][0]['snippet']['categoryId'],
            "defaultLanguage": videos_responses[0]['items'][0]['snippet']['defaultLanguage'],
            "description": videos_responses[0]['items'][0]['snippet']['description'],
            'tags': videos_responses[0]['items'][0]['snippet']['tags'],
            "title": videos_responses[0]['items'][0]['snippet']['title']
          }
    }


# %%
response


# %%



