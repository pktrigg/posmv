# POSMVRead.py
# =====
# created:          May 2018
# version           1.0.
# by:               paul.kennedy@guardiangeomatics.com
# description:      python module to read an Applanix .000 binary file
# notes:            See main at end of script for example how to use this
# based on ICD file version 4  
# developed for Python version 3.4 
# See readme.md for more details

import ctypes
import math
import pprint
import struct
import os.path
import time
from datetime import datetime
from datetime import timedelta
import datetime, calendar

###############################################################################
def main():
	#open the file for reading by creating a new POSReader class and passin in the filename to open.
	filename = "C:/development/python/posmv/20170403_0138.000"
	summary = []
	r = POSReader(filename)
	start_time = time.time() # time the process

	while r.moreData():
		# read a datagram.  If we support it, return the datagram type and aclass for that datagram
		# The user then needs to cPOS the read() method for the class to undertake a fileread and binary decode.  This keeps the read super quick.
		groupID, datagram = r.readDatagram()

				#Multibeam Data
		# if (groupID == 1): #"Position, Attitude"
		# 	dg = C_CLOCK(self.fileptr, numberOfBytes)
		# 	return dg.typeOfDatagram, dg 

		# if (groupID == 2): # "Navigation Performance Metric"
		# if (groupID == 4): # "IMU"
		# if (groupID == 9): # "GAMS Solution"
		# if (groupID == 10): #"General Status & FDIR"
		# if (groupID == 20): #"IIN Solution Status"
		# if (groupID == 21): # "Base GPS 1 Modem"
		# if (groupID == 24): # "Aux GPS"
		# if (groupID == 29): # "Unknown29"
		# if (groupID == 32): # "Unknown32"
		# if (groupID == 33): # "Unknown33"
		# if (groupID == 34): # "Unknown34"
		# if (groupID == 35): # "Unknown35"
		# if (groupID == 36): # "Unknown36"
		# if (groupID == 37): # "Unknown37"
		# if (groupID == 38): # "Unknown38"
		# if (groupID == 39): # "Unknown39"
		# if (groupID == 41): # "Unknown41"
		# if (groupID == 50): # "Unknown50"
		# if (groupID == 51): # "Unknown51"
		# if (groupID == 52): # "Unknown52"
		# if (groupID == 53): # "Unknown53"
		# if (groupID == 56): # "Unknown56"
		# if (groupID == 61): # "Unknown61"
		# if (groupID == 91): # "Unknown91"
		# if (groupID == 92): # "Unknown92"
		# if (groupID == 93): # "Unknown93"
		# if (groupID == 99): # "Versions & Stats"
		# if (groupID == 102): # "Sensor 1 Position, Attitude"
		# if (groupID == 106): # "Unknown106"
		# if (groupID == 110): # "MV General Status & FDIR"
		# if (groupID == 111): # "Heave & True Heave"
		# if (groupID == 112): # "NMEA"
		# if (groupID == 113): # "Heave & True Heave Metrics"
		# if (groupID == 114): # "TrueZ"
		# if (groupID == 120): # "Unknown120"
		# if (groupID == 135): # "Unknown135"
		# if (groupID == 136): # "Unknown136"
		# if (groupID == 10001): # "Primary GPS Stream"
		# if (groupID == 20102): # "Unknown20102"


		if not groupID in summary:
			summary.append(groupID)
			print (summary)



		# if groupID == 3 or groupID == 11 or groupID == 12 or groupID == 13  or groupID == 136:
		# 	print(r.recordTime, groupID)
		# if groupID == 10:
		# 	print(r.recordTime, groupID)
		if groupID == 112: # NMEA
			print(r.recordTime, groupID)
		# 	datagram.read()
		# if groupID == 114: # TrueZ
		# 	# continue

def getDatagramName(groupID):
	'''Convert the datagram type from the code to a user readable string.  Handy for displaying to the user'''

	if (groupID == 1):
		return "Position, Attitude"
	if (groupID == 2):
		return "Navigation Performance Metric"
	if (groupID == 4):
		return "IMU"
	if (groupID == 9):
		return "GAMS Solution"
	if (groupID == 10):
		return "General Status & FDIR"
	if (groupID == 20):
		return "IIN Solution Status"
	if (groupID == 21):
		return "Base GPS 1 Modem"
	if (groupID == 24):
		return "Aux GPS"
	if (groupID == 29):
		return "Unknown29"
	if (groupID == 32):
		return "Unknown32"
	if (groupID == 33):
		return "Unknown33"
	if (groupID == 34):
		return "Unknown34"
	if (groupID == 35):
		return "Unknown35"
	if (groupID == 36):
		return "Unknown36"
	if (groupID == 37):
		return "Unknown37"
	if (groupID == 38):
		return "Unknown38"
	if (groupID == 39):
		return "Unknown39"
	if (groupID == 41):
		return "Unknown41"
	if (groupID == 50):
		return "Unknown50"
	if (groupID == 51):
		return "Unknown51"
	if (groupID == 52):
		return "Unknown52"
	if (groupID == 53):
		return "Unknown53"
	if (groupID == 56):
		return "Unknown56"
	if (groupID == 61):
		return "Unknown61"
	if (groupID == 91):
		return "Unknown91"
	if (groupID == 92):
		return "Unknown92"
	if (groupID == 93):
		return "Unknown93"
	if (groupID == 99):
		return "Versions & Stats"
	if (groupID == 102):
		return "Sensor 1 Position, Attitude"
	if (groupID == 106):
		return "Unknown106"

	if (groupID == 110):
		return "MV General Status & FDIR"
	if (groupID == 111):
		return "Heave & True Heave"
	if (groupID == 112):
		return "NMEA"
	if (groupID == 113):
		return "Heave & True Heave Metrics"

	if (groupID == 114):
		return "TrueZ"
	if (groupID == 120):
		return "Unknown120"
	if (groupID == 135):
		return "Unknown135"
	if (groupID == 136):
		return "Unknown136"

	if (groupID == 10001):
		return "Primary GPS Stream"
	if (groupID == 20102):
		return "Unknown20102"

###############################################################################
class POSReader:
	'''class to read a Applanix .000 file'''
	# group start 	4 chars
	# group id		2 ushort
	# byte count	2 ushort
	# time1			8 double
	# time2			8 double
	# disatance tag	8 double
	# time type		1 B
	# distance type	1 B
	# pad			0-3
	# checksum		2 ushort
	# group end		2 char
	POSPacketHeader_fmt = '=4shhddBB'
	POSPacketHeader_len = struct.calcsize(POSPacketHeader_fmt)
	POSPacketHeader_unpack = struct.Struct(POSPacketHeader_fmt).unpack_from

###############################################################################
	def __init__(self, POSfileName):
		if not os.path.isfile(POSfileName):
			print ("file not found:", POSfileName)
		self.fileName = POSfileName
		self.fileptr = open(POSfileName, 'rb')		
		self.fileSize = os.path.getsize(POSfileName)
		self.recordDate = ""
		self.recordTime = ""

		# now try and parse the filename for the GPS week.  There may be no datagram with this!
		#  default filename is in the format 20170403_0138.000, 20170403_0138.001 etc
		try:
			base = os.path.basename(POSfileName)
			name = os.path.splitext(base)[0]
			fileDate = datetime.datetime.strptime(name[0:8],"%Y%m%d")
			self.week, gpsdays, gpsseconds, microseconds = self.utcToWeekSeconds(fileDate, 16)
			date = self.weekSecondsToUtc(self.week, 0,0)
			print ("GPS Week: ", self.week, date)
		except:
			self.week = 0
			print ("filename does not contain a valid GPS week signature, timestamp correction needs to come from a datagram: ", POSfileName)
###############################################################################
	def __str__(self):
		return pprint.pformat(vars(self))

###############################################################################
	def currentRecordDateTime(self):
		'''return a python date object from the current datagram objects raw date and time fields '''
		date_object = datetime.strptime(str(self.recordDate), '%Y%m%d') + timedelta(0,self.recordTime)
		return date_object

###############################################################################
	def to_DateTime(self, recordDate, recordTime):
		'''return a python date object from a split date and time record'''
		date_object = datetime.strptime(str(recordDate), '%Y%m%d') + timedelta(0,recordTime)
		return date_object

###############################################################################
	def weekSecondsToUtc(self, gpsweek, gpsseconds, leapseconds):
		datetimeformat = "%Y-%m-%d %H:%M:%S"
		epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
		elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds+leapseconds))
		return datetime.datetime.strftime(epoch + elapsed,datetimeformat)

###############################################################################
	# utctoweekseconds(datetime.datetime.strptime('2014-09-22 21:36:52',"%Y-%m-%d %H:%M:%S"),16)
	## gives: (1811, 1, 164196,0)
	def utcToWeekSeconds(self, utcDate, leapseconds):
		""" Returns the GPS week, the GPS day, and the seconds 
			and microseconds since the beginning of the GPS week """
		datetimeformat = "%Y-%m-%d %H:%M:%S"
		epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
		tdiff = utcDate - epoch - datetime.timedelta(seconds=leapseconds)
		gpsweek = tdiff.days // 7 
		gpsdays = tdiff.days - 7*gpsweek         
		gpsseconds = tdiff.seconds + 86400* (tdiff.days -7*gpsweek) 
		return gpsweek,gpsdays,gpsseconds,tdiff.microseconds

###############################################################################
	def readDatagramHeader(self):
			'''read the common header for any datagram'''
			try:
				curr = self.fileptr.tell()
				data = self.fileptr.read(self.POSPacketHeader_len)
				s = self.POSPacketHeader_unpack(data)

				groupStart		= s[0]
				groupID	= s[1]
				numberOfBytes   = s[2]
				time1			= s[3] #GPS seconds of the week using user prefernece.  We normally use this and the default is fine
				time2			= s[4] #GPS seconds of the week in POS time (time since startup)
				distanceTag		= s[5]
				timeTypes		= s[6]
				self.recordDate = time1
				self.recordTime = time1

				# now read the trailing part of the header and compute the pad as we go.
				# pad			0-3
				# checksum		2 ushort
				# group end		2 char
				# self.data = self.fileptr.read(numberOfBytes % 4)
				# rec_fmt = '=H2s'
				# rec_len = struct.calcsize(rec_fmt)
				# rec_unpack = struct.Struct(rec_fmt).unpack_from
				# s = rec_unpack(self.fileptr.read(rec_len))



				# now reset file pointer
				self.fileptr.seek(curr, 0)
		
				# # we need to add 4 bytes as the message does not contain the 4 bytes used to hold the size of the message
				# # trap corrupt datagrams at the end of a file.  We see this in EM2040 systems.
				# if (curr + numberOfBytes + 4 ) > self.fileSize:
				# 	numberOfBytes = self.fileSize - curr - 4
				# 	groupID = 'XXX'
				# 	return numberOfBytes + 8, STX, groupID, EMModel, RecordDate, RecordTime
		
				return numberOfBytes + 8, groupID, self.recordDate, self.recordTime
			except struct.error:
				return 0,0,0,0,0,0
		

###############################################################################
	def close(self):
		'''close the current file'''
		self.fileptr.close()
		
###############################################################################
	def rewind(self):
		'''go back to start of file'''
		self.fileptr.seek(0, 0)				
	
###############################################################################
	def currentPtr(self):
		'''report where we are in the file reading process'''
		return self.fileptr.tell()

###############################################################################
	def moreData(self):
		'''report how many more bytes there are to read from the file'''
		return self.fileSize - self.fileptr.tell()
			
###############################################################################
	def readDatagramBytes(self, offset, byteCount):
		'''read the entire raw bytes for the datagram without changing the file pointer.  this is used for file conditioning'''
		curr = self.fileptr.tell()
		self.fileptr.seek(offset, 0)   # move the file pointer to the start of the record so we can read from disc			  
		data = self.fileptr.read(byteCount)
		self.fileptr.seek(curr, 0)
		return data

###############################################################################
	def getRecordCount(self):
		'''read through the entire file as fast as possible to get a count of POS records.  useful for progress bars so user can see what is happening'''
		count = 0
		self.rewind()
		while self.moreData():
			numberOfBytes, groupID, RecordDate, RecordTime = self.readDatagramHeader()
			self.fileptr.seek(numberOfBytes, 1)
			count += 1
		self.rewind()		
		return count

###############################################################################
	def readDatagram(self):
		'''read the datagram header.  This permits us to skip datagrams we do not support'''
		numberOfBytes, groupID, RecordDate, RecordTime = self.readDatagramHeader()
		
		# if groupID == '3': # 3_EXTRA PARAMETERS DECIMAL 51
		# 	dg = E_EXTRA(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg
		# if groupID == 'A': # A ATTITUDE
		# 	dg = A_ATTITUDE(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg
		# if groupID == 'C': # C Clock 
		# 	dg = C_CLOCK(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# if groupID == 'D': # D DEPTH
		# 	dg = D_DEPTH(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg
		# if groupID == 'H': # H Height  
		# 	dg = H_HEIGHT(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# if groupID == 'I': # I InstPOSation (Start)
		# 	dg = I_INSTPOSATION(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# if groupID == 'i': # i InstPOSation (Stop)
		# 	dg = I_INSTPOSATION(self.fileptr, numberOfBytes)
		# 	dg.groupID = 'i' #override with the instPOS stop code
		# 	return dg.groupID, dg 
		# if groupID == 'n': # n ATTITUDE
		# 	dg = n_ATTITUDE(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg
		# if groupID == 'N': # N Angle and Travel Time
		# 	dg = N_TRAVELTIME(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg
		# if groupID == 'R': # R_RUNTIME
		# 	dg = R_RUNTIME(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# if groupID == 'P': # P Position
		# 	dg = P_POSITION(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# if groupID == 'U': # U Sound Velocity
		# 	dg = U_SVP(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg
		# if groupID == 'X': # X Depth
		# 	dg = X_DEPTH(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# if groupID == 'Y': # Y_SeabedImage
		# 	dg = Y_SEABEDIMAGE(self.fileptr, numberOfBytes)
		# 	return dg.groupID, dg 
		# else:
		dg = UNKNOWN_RECORD(self.fileptr, numberOfBytes, groupID)
		return dg.groupID, dg
			# self.fileptr.seek(numberOfBytes, 1)

###############################################################################
class UNKNOWN_RECORD:
	'''used as a convenience tool for datagrams we have no bespoke classes.  Better to make a bespoke class'''
	def __init__(self, fileptr, numberOfBytes, groupID):
		self.groupID = groupID
		self.offset = fileptr.tell()
		self.numberOfBytes = numberOfBytes
		self.fileptr = fileptr
		self.fileptr.seek(numberOfBytes, 1)
		self.data = ""
	def read(self):
		self.fileptr.seek(self.offset, 0)
		self.data = self.fileptr.read(self.numberOfBytes)
		

###############################################################################
if __name__ == "__main__":
		main()
