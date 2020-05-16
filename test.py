# Kiran Vuksanaj
# Khosekh Discord Bot
# Hello World

from os import getenv
import discord

class KhosekhClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print(message)
        if '$hello' in message.content:
            await message.channel.send('Hello World!')
            print('Message sent!')

if __name__ == "__main__":
    TOKEN = getenv('DISCORD_TOKEN')
    client = KhosekhClient()
    client.run(TOKEN)



        
