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

tokens = {}

class NotAuthenticatedError(Exception):
    pass


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

    params = {
        'grant_type':'authorization_code',
        'code':authcode,
        'redirect_uri':SPOTIFY_REDIRECT_URI,
        }
    TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
    response = request('POST',TOKEN_ENDPOINT,headers=headers,data=params).json()
    if 'error' in response:
        print('Token Grant Error')
        print( dumps(response,indent=4) )
    else:
        return response


    
def get_profile(tokens):
    if tokens == {}:
        raise NotAuthenticatedError('no access token')
    headers = {
        'Authorization':'Bearer %s' % tokens['access_token']
        }
    endpoint = 'https://api.spotify.com/v1/me'
    response = request('GET',endpoint,headers=headers)
    return response.json()



def create_playlist(tokens,username,title):
    if tokens == {}:
        raise NotAuthenticatedError('no access token')
    endpoint = "https://api.spotify.com/v1/users/%s/playlists" % username
    headers = {
        'Authorization':'Bearer %s' % tokens['access_token'],
        'Content-Type':'application/json'
        }
    params = {
        'name':title,
        'description':'Khosekh Groove-Scratcher - Playlist made from Groovy Queue'
        }
    response = request('POST',endpoint,headers=headers,json=params).json()
    return response

# code = input('auth code: ')
# tokens = request_tokens(code)
# print('access token: %s' % tokens['access_token'])
# profile = get_profile(tokens)
# print(dumps(profile,indent=4))
# create_playlist(tokens,profile['id'],'dream of loneliness')
