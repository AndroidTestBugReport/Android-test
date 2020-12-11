#!/bin/bash
echo "aaa"
FOLDERS=/SPACE/reforce-project/dataset/monkey2/unfinished/*

for f in $FOLDERS
do

	#fuser -n tcp -k 2000
	echo "Processubg $f file...."
	rm -r ./monkey2/coverage.ec

	adb -s emulator-5554 emu kill
	#gnome-terminal -e "./closeEmulator.sh"
	sleep 0.1m

	gnome-terminal -e "./startEmulator_5554.sh"
	sleep 1.5m
	
	adb -s emulator-5554 shell rm -r sdcard/*
	adb -s emulator-5554 shell rm -r sdcard/coverage.ec

	apkPath=$(find "$f"/bin -type f -name "*-debug.apk")

	packageName=$(aapt dump badging "$apkPath" | awk -v FS="'" '/package: name=/{print $2}')
	adb -s emulator-5554 uninstall "$packageName"
	adb -s emulator-5554 install "$apkPath"

	adb -s emulator-5554 shell ps | awk '/com\.android\.commands\.monkey/ { system("adb -s emulator-5554 shell kill " $2) }'
	adb -s emulator-5554 logcat -c
	timeout 1h adb -s emulator-5554 shell monkey -p "$packageName" -v --throttle 200 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --bugreport 1000000 > monkey2/"$(basename "$f")"
	echo "Monkey finish"
	adb -s emulator-5554 logcat -d>monkey2/"$(basename "$f")_logcat"

        adb -s emulator-5554 shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE
	adb -s emulator-5554 pull /mnt/sdcard/coverage.ec ./monkey2/coverage.ec
	java -cp /home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/lib/emma.jar emma report -r txt -in "$f"/bin/coverage.em,./monkey2/coverage.ec -Dreport.txt.out.file=./monkey2/"$(basename "$f")_coverage.txt"

	echo "Finish $f"
	mv "$f" /SPACE/reforce-project/dataset/monkey2/finished
	sleep 5s

	

done

#ps a
#ill -9 PID

