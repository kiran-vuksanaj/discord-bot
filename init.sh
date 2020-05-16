if [[ -f ".secret_keys" ]]; then
	echo "Reading Keys from ./.secret_keys...";
	keys=(`cat .secret_keys`);
	export DISCORD_TOKEN=${keys[1]};
	echo "Successfully exported keys to environment.";
else
	echo "./.secret_keys not found. Please enter keys.";
	echo -n "Discord Bot Token: ";
	read ans;
	export DISCORD_TOKEN=$ans;
	echo "discord: $DISCORD_TOKEN" >> .secret_keys;
	echo "Keys exported to environment and ./.secret_keys";
fi

if [[ ! -d "venv" ]]; then
	echo "Creating Virtual Environment...";
	virtualenv venv;
	. venv/bin/activate;
	pip3 install -r requirements.txt;
	deactivate;
fi

. venv/bin/activate
echo "Launching Client..."
echo "Launching Client..." >> longterm_log.txt
date >> longterm_log.txt
python __init__.py &>> longterm_log.txt &
disown;
deactivate;

