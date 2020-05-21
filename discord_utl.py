# Kiran Vuksanaj
# khosekh the bot
# discord.py utility functions


def find_vc_cnx(uid,guild):
    for channel in guild.channels:
        # print(channel.name, type(channel).__name__)
        if type(channel).__name__=='VoiceChannel':
            for member in channel.members:
                if member.id == uid:
                    return channel
    # search = filter(
    #     lambda channel: type(channel).__name__=='VoiceChanel' and filter(lambda member: member.id==uid, channel.members),
    #     guild.channels
    #     )
    # print(list(search))
    return None
