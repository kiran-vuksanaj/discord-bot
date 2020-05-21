# Kiran Vuksanaj
# Khosekh Discord Bot
# init file

import os,atexit,sys,datetime
import kclient,spotify

def write_livelog():
    with open('logs/live.txt','x') as live_log:
        live_log.write( '%s\n' % os.getpid() )

if __name__ == "__main__":
    
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    write_livelog()

    TOKEN = os.getenv('DISCORD_TOKEN')

    client = kclient.KhosekhClient()
    atexit.register( lambda: client.close )

    client.run(TOKEN)



        
