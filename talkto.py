# Kiran Vuksanaj
# khosekh the bot
# talkto command

import shlex
import argparse
import random

import databasing

class ArgumentException(Exception):
    pass

class ArgumentParser(argparse.ArgumentParser):
    def exit(self,status=0,message=None):
        if status:
            raise ArgumentException(f'Exiting because of an error: {message}')
        print(f'Would have exited with status {status}')

parser = ArgumentParser(prog='talkto',conflict_handler='error')
parser.add_argument('name',action='store',type=str)
parser.add_argument('--new',action='store',default=None,type=str)
parser.add_argument('-a',action='store_true',dest='showall',default=False)

def talkto(command_str):
    print('talkto command: "%s"' % command_str)
    args = shlex.split(command_str)
    try:
        results = parser.parse_args(args[1:])
    except ArgumentException as e:
        return str(e).strip()
    else:
        print(results)
        if results.showall:
            phrases = '\n'.join(databasing.phrases(results.name))
            return f'```Phrases that exist for {results.name}:\n\n{phrases}\n```'
        if results.new:
            databasing.addphrase(results.name,results.new)
            return f'"{results.new}" added to {results.name}\'s talk messages.'
        # else
        phrases = databasing.phrases(results.name)
        if phrases:
            return random.choice(phrases)
        else:
            return f'No entries exist yet for {results.name}. Add one with `$talkto {results.name} --new "<new phrase>"` !'

print(talkto('$talkto kiran'))
