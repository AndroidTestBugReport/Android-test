#!/bin/bash
echo "aaa"
FOLDERS=/SPACE/reforce-project/dataset/stoat/unfinished/*

for f in $FOLDERS
do

	fuser -n tcp -k 2000
	echo "Processubg $f file...."

	adb -s emulator-5554 emu kill
	#gnome-terminal -e "./closeEmulator.sh"
	sleep 0.1m

	#gnome-terminal -e "./startEmulator.sh"
	#sleep 0.6m



	timeout 1h ruby /SPACE/stoat/Stoat-master/Stoat/bin/run_stoat_testing.rb --model_time 0.4h --mcmc_time 0.6h --app_dir "$f" --avd_name testAVD --avd_port 5554 --stoat_port 2000 --project_type ant>stoat/"$(basename "$f")"

	echo "Finish $f"
	mv "$f" /SPACE/reforce-project/dataset/stoat/finished
	sleep 5s


done

#ps a
#ill -9 PID
#lsof -i -P -n | grep LISTEN
