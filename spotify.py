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

import databasing

SPOTIFY_CLIENT_ID = getenv('SPOTIFY_CLIENT_ID').strip()
SPOTIFY_CLIENT_SECRET = getenv('SPOTIFY_CLIENT_SECRET').strip()
SPOTIFY_REDIRECT_URI = getenv('SPOTIFY_REDIRECT_URI').strip()

tokens = {}

class NotAuthenticatedError(Exception):
    pass
class APIError(Exception):
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


def request_tokens(code,refresh=False):
    auth_header = b64encode( str(SPOTIFY_CLIENT_ID+':'+SPOTIFY_CLIENT_SECRET).encode('ascii') )
    headers = {
        'Authorization':'Basic %s' % auth_header.decode('ascii')
        }
    if refresh:
        params = {
            'grant_type':'refresh_token',
            'refresh_token':code
            }
    else:
        params = {
            'grant_type':'authorization_code',
            'code':code,
            'redirect_uri':SPOTIFY_REDIRECT_URI,
        }
    TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
    response = request('POST',TOKEN_ENDPOINT,headers=headers,data=params).json()
    if 'error' in response:
        print('Token Grant Error')
        print( dumps(response,indent=4) )
    else:
        return response

def access_rest(endpoint,uid,method,json=None):
    atoken = databasing.get_atoken(uid)
    BASE_URL = 'https://api.spotify.com/v1/'
    headers = {
        'Authorization':'Bearer %s' % atoken,
        'content-type':'application/json'
        }
    url = BASE_URL + endpoint.format(databasing.get_spotuser(uid))
    resp = request(method,url,json=json,headers=headers)
    r_json = resp.json()
    if 'error' in r_json:
        if r_json['error']['status']==401:
            rtoken = databasing.get_rtoken(uid)
            tokens = request_tokens(rtoken,refresh=True)
            print('new tokens:',tokens)
            if not 'refresh_token' in tokens:
                tokens['refresh_token'] = rtoken
            databasing.update_tokens(uid,tokens)
            return access_rest(endpoint,uid,method,json=json)
        else:
            print('REST Error')
            print(r_json)
            raise APIError

    return r_json


def get_profile(tokens):
    if tokens == {}:
        raise NotAuthenticatedError('no access token')
    headers = {
        'Authorization':'Bearer %s' % tokens['access_token']
        }
    endpoint = 'https://api.spotify.com/v1/me'
    response = request('GET',endpoint,headers=headers)
    return response.json()



def create_playlist(uid,title):
    params = {
        'name':title,
        'description':'Khosekh Groove-Scratcher - Playlist made from Groovy Queue'
        }
    return access_rest('users/{0}/playlists',uid,'POST',json=params)    

def add_song(channel_id,song):
    cdata = databasing.get_playlist_data(channel_id)
    endpoint = 'playlists/%s/tracks' % cdata['playlist_id']
    params = {
        "uris":[
            "spotify:track:%s" % song
            ]
        }
    return access_rest(endpoint,cdata['discord_id'],'POST',json=params)
        

# code = input('auth code: ')
# tokens = request_tokens(code)
# print('access token: %s' % tokens['access_token'])
# profile = get_profile(tokens)
# print(dumps(profile,indent=4))
# create_playlist(tokens,profile['id'],'dream of loneliness')
