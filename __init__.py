# Kiran Vuksanaj
# Khosekh Discord Bot
# init file

import os,atexit
import kclient,spotify


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = kclient.KhosekhClient()
    atexit.register( lambda: client.close )
    client.run(TOKEN)



        
