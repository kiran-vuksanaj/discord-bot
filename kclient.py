# Kiran Vuksanaj
# khosekh the bot
# discord client

import os,sys,random,re

import discord

import spotify
import databasing
import discord_utl

from asyncio import TimeoutError

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
        elif message.content.strip().startswith('$track'):
            text = message.content.strip()
            title = text[text.find(' '):].strip()
            vchannel = discord_utl.find_vc_cnx(message.author.id,message.guild)
            playlist = spotify.create_playlist(message.author.id,title)
            print(playlist)
            databasing.register_channel(vchannel.id,message.author.id,playlist['id'])
            await message.channel.send('Successfully Registered!')

                
                

        elif str(message.author)=='Groovy#7254'and len(message.embeds) == 1 and  message.embeds[0].title=="Now playing":
            print('now playing message')
            
            regex_match = re.match(r'\s*\[(.*)\]\s*\((.*)\)\s*\[<@(\d+)>\]\s*',message.embeds[0].description)
            print('title: [{0}]'.format(regex_match.group(1)))
            print('link: [{0}]'.format(regex_match.group(2)))
            print('user: [{0}]'.format(int(regex_match.group(3))))
            title = regex_match.group(1)
            link = regex_match.group(2)
            vc = discord_utl.find_vc_cnx(message.author.id,message.guild)
            vcdata = databasing.get_playlist_data(vc.id) or None
            if vcdata:
                # add song to registered playlist
                if 'spotify.com' in link:
                    song_id = link[link.rfind('/')+1:]
                    if databasing.add_song_nonduplicate(song_id,vcdata['playlist_id']):
                        spotify.add_song(vc.id,song_id)
                        await message.channel.send('Song added to playlist!')
                    else:
                        await message.channel.send('Song already exists in playlist! Skipping.')
                else:
                    searchdata = spotify.search_song(title,vcdata['discord_id'])
                    resultstrings = map(lambda res: '[{0[name]}]({0[external_urls][spotify]}), by {0[artists][0][name]} on album {0[album][name]}'.format(res), searchdata['tracks']['items'])
                    result_emojis = ['🥇','🥈','🥉']
                    
                    description = 'Select option to add to playlist:\n'+'\n'.join(map(lambda info,emoji: emoji+' '+info, resultstrings,result_emojis))
                    response_embed = discord.Embed(title='Select Song:',type='rich',description=description)
                    sent_message = await message.channel.send(embed=response_embed)
                    for i in range(min(3,searchdata['tracks']['total'])):
                        await sent_message.add_reaction(result_emojis[i])
                    await sent_message.add_reaction('❌')
                    await sent_message.add_reaction('➕')
                    def valid_reacc(reaction, user):
                        return reaction.message.id == sent_message.id and user.id == vcdata['discord_id'] and (reaction.emoji in result_emojis or reaction.emoji=='➕' or reaction.emoji=='❌')
                    try:
                        reaction, user = await self.wait_for('reaction_add',timeout=60.0, check=valid_reacc)
                    except TimeoutError:
                        await sent_message.edit(embed=None,content='Song addition menu expired.')
                    else:
                        if reaction.emoji in result_emojis:
                            chosen_index = result_emojis.index(reaction.emoji)
                            print(chosen_index)
                            song_id = searchdata['tracks']['items'][chosen_index]['id']
                            if databasing.add_song_nonduplicate(song_id,vcdata['playlist_id']):
                                spotify.add_song(vc.id,song_id)
                                response_embed.description = 'Option {0} added to playlist.'.format(chosen_index+1)
                            else:
                                response_embed.description = 'Option {0} chosen, skipped as duplicate.'.format(chosen_index+1)
                        elif reaction.emoji=='❌':
                            response_embed.description = 'song addition cancelled.'
                        elif reaction.emoji=='➕':
                            response_embed.description = 'Choose other song: feature coming soon.'
                        await sent_message.edit(embed=response_embed)
            else:
                print('passing, because channel is not registered')


            

        else:
            print('irrelevant message')

