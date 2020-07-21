from datetime import datetime
from os import environ

from jinja2 import Environment, FileSystemLoader
from pytz import utc
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

with open('.authorization_code', 'r') as file:
  authorization_code = file.read()

scope = 'user-read-currently-playing,user-read-recently-played,user-read-playback-state'
sp_oauth = SpotifyOAuth(cache_path=environ['SPOTIPY_CACHE_PATH'], scope=scope)

try:
  tokens = sp_oauth.get_access_token(code=authorization_code, as_dict=True)
except Exception as e: 
   tokens = sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])

expires_at = tokens['expires_at']
artists_names = []
artists_urls = []

if expires_at > int(datetime.now().strftime('%s')):
  sp = Spotify(auth_manager=sp_oauth)
  last_updated = datetime.now(tz=utc).strftime('%Y-%m-%d %H:%M:%S %Z')
  currently_playing = sp.current_user_playing_track()
  if currently_playing:
    song_name = currently_playing['item']['name']
    song_url = currently_playing['item']['external_urls']['spotify']
    album_name = currently_playing['item']['album']['external_urls']['spotify']
    album_image_url = currently_playing['item']['album']['images'][0]['url']
    artists = currently_playing['item']['artists']
    if len(artists) > 1:
      for artist in artists:
        artists_names.append(artist['name'])
        artists_urls.append(artist['external_urls']['spotify'])
    else:
      artists_names.append(artists[0]['name'])
      artists_urls.append(artists[0]['external_urls']['spotify'])
  else:
    song_name = ''
    song_url = ''
    artists = []
    album_name = ''
    album_image_url = ''

templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader, autoescape=True)
template = templateEnv.get_template("template.md")
output = template.render(song_name=song_name, song_url=song_url, album_name=album_name, album_image_url=album_image_url, artists_names=artists_names, artists_urls=artists_urls)
