from threading import Thread
from os import environ

from flask import Flask, request
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

scope = 'user-read-currently-playing,user-read-recently-played,user-read-playback-state'
sp_oauth = SpotifyOAuth(scope=scope)

@app.route('/', methods = ['GET'])
def root():
  if request.method == 'GET':
    code = request.args.get('code')
    if code:
      with open('.authorization_code', 'w') as file:
         file.write(code)
      func = request.environ.get('werkzeug.server.shutdown')
      func()
    return 'Nice!', 200

print('Access this URL on your browser: ' + sp_oauth.get_authorize_url() + '\n')

server = Thread(target=app.run(), daemon=True)
server.start()

print('All done!')
