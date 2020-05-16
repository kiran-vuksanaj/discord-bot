if [[ -f "live_log.txt" ]]; then
	PID=(`head -n 1 live_log.txt`)
	echo "Client Alive at pid $PID"
	kill $PID
	echo "Client Killed"
else
	echo "No client currently alive"
fi

	
