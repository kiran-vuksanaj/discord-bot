if [[ -f "logs/live.txt" ]]; then
	PID=(`head -n 1 logs/live.txt`)
	echo "Client Alive at pid $PID"
	kill $PID
	echo "Client Killed"
else
	echo "No client currently alive"
fi

	
