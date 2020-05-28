# Kiran Vuksanaj
# khosekh the bot
# databasing functions (round ii)

import sqlite3
import atexit

# =============== GLOBAL VARIABLES =============== #

DB_FILENAME = 'dat/khosekh.db'
db = sqlite3.connect(DB_FILENAME)
c = db.cursor()
atexit.register(lambda: db.close())

# =============== TABLE INITIALIZATION =============== #

def init_tables():
    tables = {
        'auths' : [
            ['discord_uid','INTEGER PRIMARY KEY'],
            ['access_token','TEXT'],
            ['refresh_token','TEXT'],
            ['spotify_user','TEXT']
            ] ,
        'vchannels' : [
            ['channel_id','INTEGER PRIMARY KEY'],
            ['tracker_uid','INTEGER'],
            ['spotify_user','TEXT'],
            ['playlist_id','TEXT']
            ] ,
        'songs' : [
            ['song_id','TEXT'],
            ['playlist_id','TEXT']
            ] ,
        'phrases' : [
            ['name','TEXT'],
            ['phrase','TEXT']
            ]
        }
    for table in tables:
        command = 'CREATE TABLE IF NOT EXISTS %s (%s)' % ( table, ', '.join(map(lambda col: ' '.join(col),tables[table])) )
        # print(command)
        c.execute(command)
        # i use % formatting here because im creating actual names in the sqlite table, not just strings!
        # also, no concern because no user input is used
    db.commit()
    return True

# =============== AUTH TABLE FUNCTIONS =============== #

def add_auth(uid,tokens,profile):
    command = 'INSERT INTO auths (discord_uid,access_token,refresh_token,spotify_user) VALUES (?, ?, ?, ?)'
    params = (uid,tokens['access_token'],tokens['refresh_token'],profile['id'])
    c.execute(command,params)
    db.commit()
    return True

def get_atoken(uid):
    command = 'SELECT access_token FROM auths WHERE discord_uid=:uid'
    c.execute(command, {'uid':uid})
    out = c.fetchone()[0]
    db.commit()
    return out

def get_rtoken(uid):
    command = 'SELECT refresh_token FROM auths WHERE discord_uid=:uid'
    c.execute(command,{'uid':uid})
    out = c.fetchone()[0]
    db.commit()
    return out

def get_spotuser(uid):
    command = 'SELECT spotify_user FROM auths WHERE discord_uid=:uid'
    c.execute(command,{'uid':uid})
    out = c.fetchone()[0]
    db.commit()
    return out

def update_tokens(uid,tokens):
    command = 'UPDATE auths SET access_token=?, refresh_token=? WHERE discord_uid=?'
    params = (tokens['access_token'],tokens['refresh_token'],uid)
    c.execute(command,params)
    db.commit()
    return True

# =============== VCHANNEL TABLE FUNCTIONS =============== #

def register_channel(channel_id,uid,playlist_id):
    spot_user = get_spotuser(uid)
    command = 'INSERT INTO vchannels (channel_id,tracker_uid,spotify_user,playlist_id) VALUES (?, ?, ?, ?)'
    params = (channel_id,uid,spot_user,playlist_id)
    c.execute(command,params)
    db.commit()
    return True

def get_playlist_data(channel_id):
    command = 'SELECT tracker_uid,spotify_user,playlist_id FROM vchannels WHERE channel_id=:channel_id'
    c.execute(command,{'channel_id':channel_id})
    resp = c.fetchone()
    db.commit()
    return {
        'discord_id':resp[0],
        'spotify_user':resp[1],
        'playlist_id':resp[2]
        } or None



# =============== SONG TABLE FUNCTIONS =============== #

def add_song_nonduplicate(song_id,playlist_id):
    command = 'SELECT song_id,playlist_id FROM songs WHERE song_id=? AND playlist_id=?'
    params = (song_id,playlist_id)
    c.execute(command,params)
    db.commit()
    if c.fetchone():
        return False
    else:
        command = 'INSERT INTO songs (song_id,playlist_id) VALUES (?, ?)'
        c.execute(command,params)
        db.commit()
        return True
    
# =============== PHRASE TABLE FUNCTIONS =============== #

def addphrase(name,phrase):
    command = 'INSERT INTO phrases (name,phrase) VALUES (?, ?)'
    params = (name,phrase)
    c.execute(command,params)
    db.commit()
    return True

def phrases(name):
    command = 'SELECT phrase FROM phrases WHERE name=?;'
    c.execute(command, (name,))
    db.commit()
    res = c.fetchall()
    if res:
        return list(map(lambda ary: ary[0], res))
    else:
        return []

# =============== CONFIG FUNCTION CALLS =============== #
init_tables()

# # test auths table
# add_auth(44,{'access_token':'green','refresh_token':'blue'},{'id':'card'})
# print('rtoken:',get_rtoken(44))
# print('atoken:',get_atoken(44))
# update_tokens(44,{'access_token':'white','refresh_token':'blue'})
# print('atoken:',get_atoken(44))
# # test vchannels table
# register_channel(42,44,'honey')
# print(get_playlist_data(42))
# # test songs table
# print(add_song_nonduplicate('hey bitch','do ya'))
# print(add_song_nonduplicate('hey bitch','do ya'))
# print(add_song_nonduplicate('hey bitch','do you'))
# print(add_song_nonduplicate('hiya bitch','do ya'))
# print(add_song_nonduplicate('we are','asymptotic'))
