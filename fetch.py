from requests_html import HTMLSession
import os
from dotenv import load_dotenv
load_dotenv()

playlist_url = os.getenv("APPLE_MUSIC_PLAYLIST_URL")	
session = HTMLSession()
r = session.get(playlist_url)

cwd = os.path.abspath(__file__)
tracklists_items = r.html.find(".tracklist-item__text__headline")
tracklists_headlines = list(map(lambda tracklist_item: tracklist_item.text, tracklists_items))

download_result = os.popen(f'instantmusic -p -s {tracklists_headlines[0]}').read()

storage_directory = os.getenv("STORAGE_DIRECTORY")

if storage_directory:
  song_name = download_result.split('[ffmpeg] Destination: ', 1)[1].split('\n', 1)[0]
  os.system(f'mv "./{song_name}" {storage_directory}/')
