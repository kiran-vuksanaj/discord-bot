# Kiran Vuksanaj
# Khosekh Discord Bot
# Hello World

import os
import sys
import atexit
import datetime
import discord

with open('live_log.txt','x') as live_log:
    live_log.write('{0}\n'.format(os.getpid()))


def log(string):
    print(string)
    with open('live_log.txt','a') as live_log:
        live_log.write("{0} $ {1}\n".format(datetime.datetime.now(),string))

def close_log():
    print('Killing Client.')
    os.remove('live_log.txt')

    
class KhosekhClient(discord.Client):
    async def on_ready(self):
        log('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        log("{0.author}: {0.content}".format(message))
        if '$hello' in message.content:
            await message.channel.send('Hello World!')
            log('Message sent!')

if __name__ == "__main__":
    atexit.register(close_log)

    TOKEN = os.getenv('DISCORD_TOKEN')

    client = KhosekhClient()
    client.run(TOKEN)



        
