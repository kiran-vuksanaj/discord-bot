# Kiran Vuksanaj
# khosekh the bot
# discord client

import os,sys,random,re

import discord

import spotify
import databasing
import discord_utl

class KhosekhClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def close(self):
        await super().close()
        os.remove('logs/live.txt')
        print('Live log removed.')
        print('Killing Client\n')

    async def on_message(self, message):
        print("{0.author}: {0.content} // {1}".format(message,len(message.embeds)))
        # print( pprint.pformat(message, indent=4, depth=2) )

        if '$hello' in message.content:
            await message.channel.send('Hello World!')
            print('Hello World message sent!')


        elif '$version' in message.content:
            # await message.channel.send('te amo mucho paige\n:yellow_heart:')
            print('received version command ('+message.content+')')
            with open('logs/version.txt','r') as version_log:
                await message.channel.send('```\n{0}\n```'.format(version_log.read()))
            # await message.channel.send('```\nCurrent Version\n{0}\n```'.format(commit))
            print('commit message sent')


        elif '$paige' in message.content:
            print('received paige command')
            with open('dat/paige.csv') as paige_messages:
                messages = paige_messages.readlines()
                print(messages)
                await message.channel.send(random.choice(messages))
                print('paige message sent')


        elif message.content.strip() == '$auth':
            print('received auth command')
            auth_embed = discord.Embed(
                title='Spotify Authentication',
                type='rich',
                description='Click here to provide spotify authentication',
                url=spotify.gen_requestlink()
                )
            print(auth_embed)
            print(auth_embed.to_dict())
            await message.channel.send(embed=auth_embed)

        elif message.content.strip().startswith('$auth-code'):
            print('received authorization code')
            terms = message.content.split()
            print(terms)
            if len(terms) < 2:
                await message.channel.send('Improper usage: $auth-code <authorization code>')
                print('error message sent')
            else:
                print('valid message')
                authcode = terms[1]
                print(authcode)
                try:
                    tokens = spotify.request_tokens(authcode)
                    profile = spotify.get_profile(tokens)
                    print(message.author.id)
                    print(profile)
                    print('got profile, author, tokens')
                    databasing.add_auth(message.author.id,tokens,profile)
                    await message.channel.send('Success! you have now been authenticated.')
                    print('success message sent')
                except spotify.NotAuthenticatedError:
                    await message.channel.send('Token failure?')
                    print(token)
                    print('fail message sent')
        
        elif len(message.embeds) == 1 and message.embeds[0].title=="Now playing":
            print('now playing message')
            regex_match = re.match(r'\s*\[(.*)\]\s*\((.*)\)\s*\[<@(\d+)>\]\s*',message.embeds[0].description)
            print('title: [{0}]'.format(regex_match.group(1)))
            print('link: [{0}]'.format(regex_match.group(2)))
            print('user: [{0}]'.format(int(regex_match.group(3))))
            print( discord_utl.find_vc_cnx(message.author.id,message.guild).id )
            await message.channel.send('hey groovy whats good')


        else:
            print('irrelevant message')

