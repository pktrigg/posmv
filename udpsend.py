
from socket import *
import sys
import time

s = socket(AF_INET,SOCK_DGRAM)
host = "127.0.0.1"
port = 9999
buf =1024
addr = (host,port)

filname = "E:/000/reelax_and_capricornus/20160830_leePoint-A.000"
f=open (filname, "rb") 
# f=open (sys.argv[1], "rb") 
data = f.read(buf)
while (data):
	if(s.sendto(data,addr)):
		print ("sending ...", data)
		time.sleep(0.1)    # pause seconds
		data = f.read(buf)
s.close()
f.close()