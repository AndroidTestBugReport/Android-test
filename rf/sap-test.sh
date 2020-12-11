#!/bin/bash
echo "aaa"
FOLDERS=/SPACE/reforce-project/dataset/sapienze/unfinished/*

for f in $FOLDERS
do

	#fuser -n tcp -k 2005
	echo "Processubg $f file...."

	adb -s emulator-5554 emu kill
	#gnome-terminal -e "./closeEmulator.sh"
	sleep 0.1m

	gnome-terminal -e "./startEmulator_5554.sh"
	sleep 2m

	adb -s emulator-5554 shell rm -r sdcard/*
	adb -s emulator-5554 shell rm -r sdcard/coverage.ec
	adb -s emulator-5554 logcat -c
	#timeout 1h ruby /SPACE/stoat/Stoat-master/Stoat/bin/run_stoat_testing.rb --model_time 0.4h --mcmc_time 0.6h --app_dir "$f" --avd_name testAVD --avd_port 5554 --stoat_port 2000 --project_type ant>sapienze/"$(basename "$f")"


	timeout 1h python /SPACE/Sapienz-unChanged/main.py "$f">sapienze/"$(basename "$f")"

	adb -s emulator-5554 logcat -d>sapienze/"$(basename "$f")_logcat"

	sleep 5s

	echo "Sap finish"
	adb -s emulator-5554 logcat -d>sapienze/"$(basename "$f")_logcat"

        adb -s emulator-5554 shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE
	adb -s emulator-5554 pull /mnt/sdcard/coverage.ec ./sapienze/coverage.ec
	java -cp /home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/lib/emma.jar emma report -r txt -in "$f"/bin/coverage.em,./sapienze/coverage.ec -Dreport.txt.out.file=./sapienze/"$(basename "$f")_coverage.txt"

	echo "Finish $f"
	mv "$f" /SPACE/reforce-project/dataset/sapienze/finished


done

#ps a
#ill -9 PID
#lsof -i -P -n | grep LISTEN
