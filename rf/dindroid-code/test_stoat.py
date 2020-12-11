import os
import shutil
import ENV
import commands


port="5554"

for folderName in os.listdir("/SPACE/reforce-project/dataset/stoat/unfinished"):
    
    sourceCodePath="/SPACE/reforce-project/dataset/stoat/unfinished/"+folderName
    print(sourceCodePath)
    source = sourceCodePath
    
    #ENV.restartAndroidEumlator(port,commands)
    cmd=" fuser -n tcp -k 2000"
    print(commands.getstatusoutput(cmd))

    cmd="timeout 1h ruby /SPACE/stoat/Stoat-master/Stoat/bin/run_stoat_testing.rb --model_time 0.4h --mcmc_time 0.6h --app_dir "+sourceCodePath+" --avd_port 5554 --stoat_port 2000 --project_type ant>stoat/"+folderName
    outPut=commands.getstatusoutput(cmd)
    print("finish: "+sourceCodePath)

    # Destination path  
    destination = '/SPACE/reforce-project/dataset/stoat/finished'
    desFolder=destination+"/"+folderName
      
    # Move the content of  
    # source to destination  
    #dest = shutil.move(source, destination)
    print("After moving file:")
