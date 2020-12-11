#!/bin/bash
echo "aaa"

for f in {1..20}
do

	#fuser -n tcp -k 2005
	echo "Processubg $f file...."
	mv ./model/keras_model.h5 ./model/keras_model_abc.h5 


	python runTrain-DDQN-muliThread.py

done

#ps a
#ill -9 PID
#lsof -i -P -n | grep LISTEN
