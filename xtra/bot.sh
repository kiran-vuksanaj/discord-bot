#!/bin/bash
CLONE_PATH="/home/kiran/other/discord-bot";
cd $CLONE_PATH;

# this bash script can be run from anywhere, so it can be a convenient script to place in a more easily accessible directory
# change CLONE_PATH above to match wherever the repository is cloned.
# i use it for remote control in a single ssh command: $ssh <user@IP> ./scripts/bot.sh

while getopts ":phrkl:" opt; do
    if [[ $opt == "p" ]]; then
	git pull;
    fi;
    if [[ $opt == "h" ]]; then
	echo "usage: ~/scripts/launchbot.sh [-hpr]";
	exit 0;
    fi;
    if [[ $opt == "r" ]]; then
	. kill.sh;
    fi;
    if [[ $opt == "k" ]]; then
	. kill.sh;
	exit 0;
    fi;
    if [[ $opt == "l" ]]; then
	tail -n $OPTARG -f logs/console.txt;
	exit 0;
    fi;
    if [[ $opt == "?" ]]; then
	echo "Usage: ./scripts/bot.sh [-hkpr] [-l [<lines>]]"
    fi;
    if [[ $opt == ":" ]]; then
	tail -n 25 -f logs/console.txt;
	exit 0;
    fi;
done
. init.sh
