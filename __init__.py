# Kiran Vuksanaj
# Khosekh Discord Bot
# Hello World

import os, sys, atexit, datetime, random
import discord

with open('live_log.txt','x') as live_log:
    live_log.write('{0}\n'.format(os.getpid()))


def log(string):
    print('{0} $ {1}'.format(datetime.datetime.now(),string))
    with open('live_log.txt','a') as live_log:
        live_log.write("{0} $ {1}\n".format(datetime.datetime.now(),string))

def close_log():
    print('Killing Client.\n')
    os.remove('live_log.txt')


class KhosekhClient(discord.Client):
    async def on_ready(self):
        log('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        log("{0.author}: {0.content}".format(message))
        if '$hello' in message.content:
            await message.channel.send('Hello World!')
            log('Hello World message sent!')
        elif '$version' in message.content:
            # await message.channel.send('te amo mucho paige\n:yellow_heart:')
            log('received version command ('+message.content+')')
            with open('version_log.txt','r') as version_log:
                await message.channel.send('```\n{0}\n```'.format(version_log.read()))
            # await message.channel.send('```\nCurrent Version\n{0}\n```'.format(commit))
            log('commit message sent')
        elif '$paige' in message.content:
            log('received paige command')
            with open('dat/paige.csv') as paige_messages:
                messages = paige_messages.readlines()
                log(messages)
                await message.channel.send(random.choice(messages))
                log('paige message sent')
            log('end of paige block')
        else:
            log('irrelevant message')


if __name__ == "__main__":
    atexit.register(close_log)

    TOKEN = os.getenv('DISCORD_TOKEN')

    client = KhosekhClient()
    client.run(TOKEN)



        
