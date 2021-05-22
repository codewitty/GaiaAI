#!/usr/bin/python
## get subprocess module 
import subprocess
 
## call date command ##
p = subprocess.Popen("Main.py", stdout=subprocess.PIPE, shell=True)
 
## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
## or None, if no data should be sent to the child.
(output, err) = p.communicate()
 
## Wait for date to terminate. Get return returncode ##
p_status = p.wait()
print (f'Command output : {output}')
#print "Command exit status/return code : ", p_status
