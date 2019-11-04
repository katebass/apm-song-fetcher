from requests_html import HTMLSession
import os
from dotenv import load_dotenv
load_dotenv()

playlist_url = os.getenv('APPLE_MUSIC_PLAYLIST_URL')
storage_directory = os.getenv('STORAGE_DIRECTORY')
session = HTMLSession()
r = session.get(playlist_url)
cwd = os.path.abspath(__file__)

artist_item_data_attribute_name = 'data-test-song-artist-url'

tracklists_items = r.html.find('.tracklist-item--song .tracklist-item__text__headline')
artists_items = r.html.find(f'.tracklist-item--song [{artist_item_data_attribute_name}]')
tracklists_headlines = list(map(lambda tracklist_item: tracklist_item.text, tracklists_items))
artists_headlines = list(map(lambda artist_item: artist_item.attrs[artist_item_data_attribute_name], artists_items))

songs = [f'{artist} {tracklists_headlines[i]}' for i, artist in enumerate(artists_headlines)]

for song in songs:
  download_result = os.popen(f'instantmusic -p -s "{song}"').read()
  print(download_result)

  if storage_directory:
    file_name = download_result.split('[ffmpeg] Destination: ', 1)[1].split('\n', 1)[0]
    os.system(f'mv "./{file_name}" {storage_directory}/')
