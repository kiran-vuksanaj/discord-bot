# Kiran Vuksanaj
# Khosekh Discord Bot
# Hello World

import os, sys, atexit, datetime, random, pprint, json, re
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
        log("{0.author}: {0.content} // {1}".format(message,len(message.embeds)))
        # log( pprint.pformat(message, indent=4, depth=2) )
        if len(message.embeds) > 0:
            for embed in message.embeds:
                log( json.dumps( embed.to_dict(), indent=4, sort_keys=True ) )
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
        elif len(message.embeds) == 1 and message.embeds[0].title=="Now playing":
            log('now playing message')
            regex_match = re.match(r'\s*\[(.*)\]\s*\((.*)\)\s*\[<@(\d+)>\]\s*',message.embeds[0].description)
            log('title: [{0}]'.format(regex_match.group(1)))
            log('link: [{0}]'.format(regex_match.group(2)))
            log('user: [{0}]'.format(int(regex_match.group(3))))
            await message.channel.send('hey groovy whats good')
        else:
            log('irrelevant message')


if __name__ == "__main__":
    atexit.register(close_log)

    TOKEN = os.getenv('DISCORD_TOKEN')

    client = KhosekhClient()
    client.run(TOKEN)



        
