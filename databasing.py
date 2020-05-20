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

def update_tokens(uid,tokens):
    command = 'UPDATE auths SET access_token=?, refresh_token=? WHERE discord_uid=?'
    params = (tokens['access_token'],tokens['refresh_token'],uid)
    c.execute(command,params)
    db.commit()
    return True

# =============== VCHANNEL TABLE FUNCTIONS =============== #



# =============== SONG TABLE FUNCTIONS #

# =============== CONFIG FUNCTION CALLS =============== #
init_tables()

# test auths table
# add_auth(44,{'access_token':'green','refresh_token':'blue'},{'id':'card'})
# print('rtoken:',get_rtoken(44))
# print('atoken:',get_atoken(44))
# update_tokens(44,{'access_token':'white','refresh_token':'blue'})
# print('atoken:',get_atoken(44))
