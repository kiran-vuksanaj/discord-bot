# Kiran Vuksanaj
# khosekh the bot
# discord client

import os,sys

import discord

import spotify
import databasing
from logs import log

class KhosekhClient(discord.Client):
    async def on_ready(self):
        log('Logged on as {0}!'.format(self.user))

    async def close(self):
        await super().close()
        os.remove('logs/live.txt')
        print('Live log removed.')
        print('Killing Client\n')

    async def on_message(self, message):
        log("{0.author}: {0.content} // {1}".format(message,len(message.embeds)))
        # log( pprint.pformat(message, indent=4, depth=2) )

        if '$hello' in message.content:
            await message.channel.send('Hello World!')
            log('Hello World message sent!')


        elif '$version' in message.content:
            # await message.channel.send('te amo mucho paige\n:yellow_heart:')
            log('received version command ('+message.content+')')
            with open('logs/version.txt','r') as version_log:
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


        elif message.content.strip() == '$auth':
            log('received auth command')
            auth_embed = discord.Embed(
                title='Spotify Authentication',
                type='rich',
                description='Click here to provide spotify authentication',
                url=spotify.gen_requestlink()
                )
            log(auth_embed)
            log(auth_embed.to_dict())
            await message.channel.send(embed=auth_embed)

        elif message.content.strip().startswith('$auth-code'):
            log('received authorization code')
            terms = message.content.split()
            log(terms)
            if len(terms) < 2:
                await message.channel.send('Improper usage: $auth-code <authorization code>')
                log('error message sent')
            else:
                log('valid message')
                authcode = terms[1]
                log(authcode)
                try:
                    tokens = spotify.request_tokens(authcode)
                    profile = spotify.get_profile(tokens)
                    log(message.author.id)
                    log(profile)
                    log('got profile, author, tokens')
                    databasing.add_auth(message.author.id,tokens,profile)
                    await message.channel.send('Success! you have now been authenticated.')
                    log('success message sent')
                except spotify.NotAuthenticatedError:
                    await message.channel.send('Token failure?')
                    log(token)
                    log('fail message sent')
                    

        elif len(message.embeds) == 1 and message.embeds[0].title=="Now playing":
            log('now playing message')
            regex_match = re.match(r'\s*\[(.*)\]\s*\((.*)\)\s*\[<@(\d+)>\]\s*',message.embeds[0].description)
            log('title: [{0}]'.format(regex_match.group(1)))
            log('link: [{0}]'.format(regex_match.group(2)))
            log('user: [{0}]'.format(int(regex_match.group(3))))
            await message.channel.send('hey groovy whats good')


        else:
            log('irrelevant message')

