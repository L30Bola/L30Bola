from os import environ
from time import time

from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

with open('.authorization_code', 'r') as file:
  authorization_code = file.read()

scope = 'user-read-currently-playing,user-read-recently-played,user-read-playback-state'
sp_oauth = SpotifyOAuth(cache_path=environ['SPOTIPY_CACHE_PATH'], scope=scope)

try:
  tokens = sp_oauth.get_access_token(code=authorization_code, as_dict=True)
except Exception as e: 
   tokens = sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])

expires_at = tokens['expires_at']

if expires_at > int(time()):
  sp = Spotify(auth_manager=sp_oauth)
  currently_playing = sp.current_user_playing_track()
  song_name = currently_playing['item']['name']
  artists = currently_playing['item']['artists']
  album_image_url = currently_playing['item']['album']['images'][0]['url']