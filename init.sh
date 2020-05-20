if [[ -f ".secret_keys" ]]; then
	echo "Reading Keys from ./.secret_keys...";
	keys=(`cat .secret_keys`);
	export DISCORD_TOKEN=${keys[1]};
	export SPOTIFY_CLIENT_ID=${keys[3]};
	export SPOTIFY_CLIENT_SECRET=${keys[5]};
	export SPOTIFY_REDIRECT_URI=${keys[7]};
	echo "Successfully exported keys to environment.";
else
	echo "./.secret_keys not found. Please enter keys.";
	echo -n "Discord Bot Token: ";
	read ans;
	export DISCORD_TOKEN=$ans;
	echo "discord: $DISCORD_TOKEN" >> .secret_keys;
	echo -n "Spotify Client ID: ";
	read ans;
	export SPOTIFY_CLIENT_ID=$ans;
	echo "spotify_id: $SPOTIFY_CLIENT_ID" >> .secret_keys;
	echo -n "Spotify Client Secret: ";
	read ans;
	export SPOTIFY_CLIENT_SECRET=$ans;
	echo "spotify_secret: $SPOTIFY_CLIENT_SECRET" >> .secret_keys;
	echo -n "Spotify Redirect URI: ";
	read ans;
	export SPOTIFY_REDIRECT_URI=$ans;
	echo "spotify_uri: $SPOTIFY_REDIRECT_URI" >> .secret_keys;
	echo "Keys exported to environment and ./.secret_keys";
fi

if [[ ! -d "venv" ]]; then
	echo "Creating Virtual Environment...";
	python3 -m venv venv;
	. venv/bin/activate;
	pip3 install -r requirements.txt;
	deactivate;
fi

if [[ -f "live_log.txt" ]]; then
	echo "Client already running.";
else
	. venv/bin/activate;
	git show -s > dat/version.txt;
	echo "Launching Client...";
	echo "Launching Client..." >> logs/longterm.txt;
	date >> logs/longterm.txt;
	python __init__.py &>> logs/longterm.txt &
	disown;
	deactivate;
fi


