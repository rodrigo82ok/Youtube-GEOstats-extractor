import pandas as pd
from apiclient.discovery import build
from oauth2client.tools import argparser

#region Youtube Parameters
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SEARCH_TERM = "Deep Learning"
#endregion

#region Search Terms
argparser.add_argument("--q", help="Search term", default=SEARCH_TERM )
argparser.add_argument("--max-results", help="Max results", default=25)
args = argparser.parse_args()
options = args
#endregion

#region Get and Print Results

# Call the search.list method to retrieve results matching the specified
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
search_response = youtube.search().list(
 q=options.q,
 type="video",
 part="id,snippet",
 maxResults=options.max_results
).execute()
videos = {}
# Add each result to the appropriate list, and then display the lists of matching videos. Filter out channels, and playlists.
for search_result in search_response.get("items", []):
 if search_result["id"]["kind"] == "youtube#video":
  videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
s = ','.join(videos.keys())
#endregion

#region Get video Statistics

videos_list_response = youtube.videos().list(
 id=s,
 part='id,statistics'
).execute()

res = []

for i in videos_list_response['items']:
 temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
 temp_res.update(i['statistics'])
 res.append(temp_res)
#endregion

#Create pandas DataFrame and export to csv file
df = pd.DataFrame.from_dict(res)
df.to_csv('youtubeStats.csv', encoding='utf-8')

