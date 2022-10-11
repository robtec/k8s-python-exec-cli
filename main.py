import os.path
import datetime
import time
filename = "test.txt"
here = os.path.dirname(os.path.realpath(__file__))
subdir = "data"
completeName = os.path.join(here,subdir,filename)
file = open(completeName, 'a')

while True:
      now = datetime.datetime.now()
      dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
      print(now.strftime("%d-%m-%Y %H:%M:%S"))
      file.write(str(dt_string)+ '\n')
      file.close()
      time.sleep(86400) # every 24 hours the scripts run
      
