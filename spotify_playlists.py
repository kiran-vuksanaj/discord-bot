# Kiran Vuksanaj
# Khosekh - Discord Bot
# Interactions with Spotify API / spotipy wrapper

# testing code from examples
# shows a user's playlists (need to be authenticated via oauth)

from os import getenv
from requests import request
from urllib.parse import urlencode
from base64 import b64encode
from json import dumps

SPOTIFY_CLIENT_ID = getenv('SPOTIFY_CLIENT_ID').strip()
SPOTIFY_CLIENT_SECRET = getenv('SPOTIFY_CLIENT_SECRET').strip()
SPOTIFY_REDIRECT_URI = getenv('SPOTIFY_REDIRECT_URI').strip()

print(SPOTIFY_REDIRECT_URI)


# wait ... this is a constant isnt it?
def gen_requestlink():
    scopes = [
        'playlist-modify-public',
        'playlist-read-private',
        'playlist-modify-private',
        ]
    params = {
        'client_id':SPOTIFY_CLIENT_ID,
        'response_type':'code',
        'redirect_uri':SPOTIFY_REDIRECT_URI,
        # consider adding 'state':urandom stuff
        'scope': ' '.join(scopes),
        'show-dialog':'true' # this seems like it'd be good? leaving it for now
        }
    AUTHORIZE_ENDPOINT = 'https://accounts.spotify.com/authorize'
    return AUTHORIZE_ENDPOINT+'?'+urlencode(params)


print(gen_requestlink())

def request_tokens(authcode):
    auth_header = b64encode( str(SPOTIFY_CLIENT_ID+':'+SPOTIFY_CLIENT_SECRET).encode('ascii') )
    headers = {
        'Authorization':'Basic %s' % auth_header.decode('ascii')
        }
    print(headers)
    params = {
        'grant_type':'authorization_code',
        'code':authcode,
        'redirect_uri':SPOTIFY_REDIRECT_URI,
        }
    TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
    res = request('POST',TOKEN_ENDPOINT,headers=headers,data=params)
    print(dumps(res.json(),indent=4))
    
code = input('auth code: ')
request_tokens(code)
