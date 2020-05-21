if [[ -f "logs/live.txt" ]]; then
	PID=(`head -n 1 logs/live.txt`)
	echo "Client Alive at pid $PID"
	kill $PID
	echo "Sent Kill Signal"
	# cycle check whether process is alive
	kill -0 $PID
	while [[ $? == 0 ]]; do
	    sleep 1
	    kill -0 $PID &> /dev/null
	done;
	
	echo "Client Dead"
else
	echo "No client currently alive"
fi

	
