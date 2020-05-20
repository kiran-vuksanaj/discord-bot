# Kiran Vuksanaj
# khosekh the bot
# logging methods

import os,datetime

with open('logs/live.txt','x') as live_log:
    live_log.write('{0}\n'.format(os.getpid()))


def log(string):
    print('{0} $ {1}'.format(datetime.datetime.now(),string))
    with open('logs/live.txt','a') as live_log:
        live_log.write("{0} $ {1}\n".format(datetime.datetime.now(),string))

