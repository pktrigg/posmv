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

import sys
from glob import glob
import ctypes
import argparse
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
	parser = argparse.ArgumentParser(description='Read POSMV file and convert into human readable format.')
	parser.add_argument('-r', action='store_true', default=False, dest='recursive', help='Search Recursively from the current folder.  [Default: False]')
	parser.add_argument('-i', dest='inputFile', action='store', help='Input ALL filename to image. It can also be a wildcard, e.g. *.all')
	parser.add_argument('-s', dest='step', action='store', type=float, default=0, help='step through the records and sample every n seconds, e.g. -s 10')
	parser.add_argument('-odir', dest='odir', action='store', default="", help='Specify a relative output folder e.g. -odir conditioned')
	parser.add_argument('-summary', dest='summary', action='store_true', default=False, help='dump a summary of the records in the file')
	parser.add_argument('-warning', dest='warning', action='store', default=",", help='dump the user requested warnings from group 10 messages, e.g. -warning GPS to dumpy messages containing the string GPS.  for everything, use -warning ,  for errors use -warning ** or -warning error')

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	args = parser.parse_args()

	fileCounter=0
	matches				= []

	if args.recursive:
		for root, dirnames, filenames in os.walk(os.path.dirname(args.inputFile)):
			for f in fnmatch.filter(filenames, '*.all'):
				matches.append(os.path.join(root, f))
				# print (matches[-1])
	else:
		if os.path.exists(args.inputFile):
			matches.append (os.path.abspath(args.inputFile))
		else:
			for filename in glob(args.inputFile):
				matches.append(filename)
		# print (matches)

	if len(matches) == 0:
		print ("Nothing found in %s to condition, quitting" % args.inputFile)
		exit()
	
# #################################################################################
	#open the file for reading by creating a new POSReader class and passin in the filename to open.
	for filename in matches:

		summary = []
		r = POSReader(filename)
		start_time = time.time() # time the process
		lastRecordTime = 0

		while r.moreData():
			# read a datagram.  If we support it, return the datagram type and aclass for that datagram
			# The user then needs to cPOS the read() method for the class to undertake a fileread and binary decode.  This keeps the read super quick.
			groupID, datagram = r.readDatagram()
			# if (r.recordTime - lastRecordTime) < args.step:
			# 	continue
			

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
			if (groupID == 10): # "General Status & FDIR"
				datagram.read()
				if (args.warning in str(datagram)):
					print (datagram)

				lastRecordTime = r.recordTime
			if (groupID == 56): # "MESSAGE General data"
				datagram.read()

			if (groupID == 110): # "MV General Status & FDIR"
				datagram.read()
				# print (datagram)
				# lastRecordTime = r.recordTime
			if (groupID == 111): # "Heave & True Heave"
				datagram.read()
				# lastRecordTime = r.recordTime
			if (groupID == 112): # "NMEA Strings"
				datagram.read()
				# print (datagram)
				# lastRecordTime = r.recordTime
			# if (groupID == 113): # "Heave & True Heave Metrics"
			# if (groupID == 114): # "TrueZ"
			# if (groupID == 120): # "Unknown120"
			# if (groupID == 135): # "Unknown135"
			# if (groupID == 136): # "Unknown136"
			# if (groupID == 10001): # "Primary GPS Stream"
			# if (groupID == 20102): # "Unknown20102"

			if not groupID in summary:
				summary.append(groupID)


		if args.summary:
			print (summary)

###############################################################################
class C_M56: 
	def __init__(self, fileptr, numberOfBytes, timeOrigin):
		self.name = "General Data Message"
		self.typeOfDatagram = 56
		self.offset = fileptr.tell()
		self.numberOfBytes = numberOfBytes
		self.fileptr = fileptr
		self.fileptr.seek(numberOfBytes, 1)
		self.data = ""
		self.timeOrigin = timeOrigin

	def __str__(self):
		return self.name + from_timestamp(self.time1).strftime('%d/%m/%Y/%m/%d %H:%M:%S.%f')[:-3] + "," + self.data

	def read(self):
		self.fileptr.seek(self.offset, 0)
		rec_fmt = '=4shh h5bhbdddffddddhh2s'
		rec_len = struct.calcsize(rec_fmt)
		rec_unpack = struct.Struct(rec_fmt).unpack
		s = rec_unpack(self.fileptr.read(rec_len))
		
		# intro parameters
		self.groupStart			= s[0]
		self.groupID			= s[1]
		self.byteCount			= s[2]

		# time types structure dddBB
		self.transactionNumber	= s[3] + self.timeOrigin
		self.hours				= s[4] + self.timeOrigin
		self.minutes			= s[5]
		self.seconds			= s[6]
		self.month				= s[7]
		self.day				= s[8]
		self.year				= s[9]
		self.alignmentStatus	= s[10]
		self.latitude			= s[11]
		self.longitude			= s[12]
		self.altitude			= s[13] 
		self.horizontalPositionCEP	= s[14]
		self.initialAltitudeRMS	= s[15]
		self.initialDistance	= s[16]
		self.initialRoll	= s[17]
		self.initialPitch	= s[18]
		self.initialHeading	= s[19]				
		self.pad				= s[20]
		self.checksum			= s[21]
		self.groupEnd			= s[22]

###############################################################################
class C_110:
	def __init__(self, fileptr, numberOfBytes, timeOrigin):
		self.name = "MV General Status & FDIR - Extension (110)"
		self.typeOfDatagram = 110
		self.offset = fileptr.tell()
		self.numberOfBytes = numberOfBytes
		self.fileptr = fileptr
		self.fileptr.seek(numberOfBytes, 1)
		self.data = ""
		self.timeOrigin = timeOrigin

	def __str__(self):
		return "General Status (110), " + str(from_timestamp(self.time1)) + ", " + self.data

	def read(self):
		self.fileptr.seek(self.offset, 0)
		rec_fmt = '=4shh dddBB hhhh2s'
		rec_len = struct.calcsize(rec_fmt)
		rec_unpack = struct.Struct(rec_fmt).unpack
		# bytesRead = rec_len
		s = rec_unpack(self.fileptr.read(rec_len))

		self.groupStart			= s[0]
		self.groupID			= s[1]
		self.byteCount			= s[2]

		# time types structure dddBB
		self.time1				= s[3] + self.timeOrigin
		self.time2				= s[4] + self.timeOrigin
		self.distanceTag		= s[5]
		self.timeTypes			= s[6]
		self.distanceTypes		= s[7]

		self.generalStatus		= s[8]
		self.trueZtimeRemaining	= s[9]
		self.pad				= s[10]
		self.checksum			= s[11]
		self.groupEnd			= s[12]

		self.data = "Warning, status on TrueZ not set"
		if isBitSet(self.generalStatus, 0):
			self.data += "User logged in,"
		if isBitSet(self.generalStatus, 10):
			self.data += "TrueZ active,"
		if isBitSet(self.generalStatus, 11):
			self.data += "TrueZ ready,"
		if isBitSet(self.generalStatus, 12):
			self.data += "TrueZ inuse"

###############################################################################
class C_111: 
	def __init__(self, fileptr, numberOfBytes, timeOrigin):
		self.name = "TrueHeave (111)"
		self.typeOfDatagram = 111
		self.offset = fileptr.tell()
		self.numberOfBytes = numberOfBytes
		self.fileptr = fileptr
		self.fileptr.seek(numberOfBytes, 1)
		self.data = ""
		self.timeOrigin = timeOrigin

	def __str__(self):
		return self.name + from_timestamp(self.time1).strftime('%d/%m/%Y/%m/%d %H:%M:%S.%f')[:-3] + str(",%.3f,%.3f,%.3f,%.3f,%d" % (self.heave, self.trueHeave, self.heaveRMS, self.trueHeaveRMS, self.rejectedIMUCount))

	def read(self):
		self.fileptr.seek(self.offset, 0)
		rec_fmt = '=4shh dddBB ffLffddLLhh2s'
		rec_len = struct.calcsize(rec_fmt)
		rec_unpack = struct.Struct(rec_fmt).unpack
		# bytesRead = rec_len
		s = rec_unpack(self.fileptr.read(rec_len))
		
		# intro parameters
		self.groupStart			= s[0]
		self.groupID			= s[1]
		self.byteCount			= s[2]

		# time types structure dddBB
		self.time1				= s[3] + self.timeOrigin
		self.time2				= s[4] + self.timeOrigin
		self.distanceTag		= s[5]
		self.timeTypes			= s[6]
		self.distanceTypes		= s[7]

		self.trueHeave			= s[8]
		self.trueHeaveRMS		= s[9]
		self.status				= s[10]
		self.heave				= s[11]
		self.heaveRMS			= s[12]
		self.heaveTime1			= s[13] #pkpk can we get GPS weel from this double?
		self.heaveTime2			= s[14]
		self.rejectedIMUCount	= s[15]
		self.outOfRangeIMUCount	= s[16]
		
		self.pad				= s[17]
		self.checksum			= s[18]
		self.groupEnd			= s[19]

###############################################################################
class C_112:
	def __init__(self, fileptr, numberOfBytes, timeOrigin):
		self.name = "NMEA Strings (112)"
		self.typeOfDatagram = 112
		self.offset = fileptr.tell()
		self.numberOfBytes = numberOfBytes
		self.fileptr = fileptr
		self.fileptr.seek(numberOfBytes, 1)
		self.data = ""
		self.timeOrigin = timeOrigin

	def __str__(self):
		return self.name + from_timestamp(self.time1).strftime('%d/%m/%Y/%m/%d %H:%M:%S.%f')[:-3] + str(",%.3f,%.3f,%.3f,%.3f,%d" % (self.heave, self.trueHeave, self.heaveRMS, self.trueHeaveRMS, self.rejectedIMUCount))

	def read(self):
		self.fileptr.seek(self.offset, 0)
		self.data = self.fileptr.read(self.numberOfBytes)

		# halt development as we have no example for testing...
		# self.fileptr.seek(self.offset, 0)
		# rec_fmt = '=4shh dddBB H'
		# rec_len = struct.calcsize(rec_fmt)
		# rec_unpack = struct.Struct(rec_fmt).unpack
		# # bytesRead = rec_len
		# s = rec_unpack(self.fileptr.read(rec_len))
		
		# # intro parameters
		# self.groupStart			= s[0]
		# self.groupID			= s[1]
		# self.byteCount			= s[2]

		# # time types structure dddBB
		# self.time1				= s[3] + self.timeOrigin
		# self.time2				= s[4] + self.timeOrigin
		# self.distanceTag		= s[5]
		# self.timeTypes			= s[6]
		# self.distanceTypes		= s[7]
		# self.variableGroupByteCount = s[9]
		# self.NMEA		= s[10]
		
		# self.pad				= s[12]
		# self.checksum			= s[12]
		# self.groupEnd			= s[13]

###############################################################################
class C_10: 
	def __init__(self, fileptr, numberOfBytes, timeOrigin):
		self.name = "General FDIR Metrics (10)"
		self.typeOfDatagram = 10
		self.offset = fileptr.tell()
		self.numberOfBytes = numberOfBytes
		self.fileptr = fileptr
		self.fileptr.seek(numberOfBytes, 1)
		self.data = ""
		self.timeOrigin = timeOrigin

	def __str__(self):
		return self.name + from_timestamp(self.time1).strftime('%d/%m/%Y/%m/%d %H:%M:%S.%f')[:-3] + "," + self.data

	def read(self):
		self.fileptr.seek(self.offset, 0)
		rec_fmt = '=4shh dddBB LLLLHHHHHLH2s'
		rec_len = struct.calcsize(rec_fmt)
		rec_unpack = struct.Struct(rec_fmt).unpack
		# bytesRead = rec_len
		s = rec_unpack(self.fileptr.read(rec_len))
		
		# intro parameters
		self.groupStart			= s[0]
		self.groupID			= s[1]
		self.byteCount			= s[2]

		# time types structure dddBB
		self.time1					= s[3] + self.timeOrigin
		self.time2					= s[4] + self.timeOrigin
		self.distanceTag			= s[5]
		self.timeTypes				= s[6]
		self.distanceTypes			= s[7]

		self.generalStatusA			= s[8]
		self.generalStatusB			= s[9]
		self.generalStatusC			= s[10]
		self.FDIRLevel1Status		= s[11]
		self.FDIRLevel1IMUFailures	= s[12]
		self.FDIRLevel2Status		= s[13]
		self.FDIRLevel3Status		= s[14]
		self.FDIRLevel4Status		= s[15]
		self.FDIRLevel5Status		= s[16]
		self.extendedStatus			= s[17]
		
		self.checksum				= s[18]
		self.groupEnd				= s[19]

		if isBitSet(self.FDIRLevel1Status, 0):
			self.data += "**IMU-POS checksum error, "
		if isBitSet(self.FDIRLevel1Status, 1):
			self.data += "**IMU status bit set by IMU, "
		if isBitSet(self.FDIRLevel1Status, 2):
			self.data += "**Successive IMU failures, "
		if isBitSet(self.FDIRLevel1Status, 3):
			self.data += "**IIN configuration mismatch failure, "
		if isBitSet(self.FDIRLevel1Status, 45):
			self.data += "**Primary GPS not in Navigation mode, "
		if isBitSet(self.FDIRLevel1Status, 6):
			self.data += "**Primary GPS not available for alignment, "
		if isBitSet(self.FDIRLevel1Status, 7):
			self.data += "**Primary data gap, "
		if isBitSet(self.FDIRLevel1Status, 8):
			self.data += "**Primary GPS PPS time gap, "
		if isBitSet(self.FDIRLevel1Status, 9):
			self.data += "**Primary GPS time recovery data not received, "
		if isBitSet(self.FDIRLevel1Status, 10):
			self.data += "**Primary GPS observable data gap, "
		if isBitSet(self.FDIRLevel1Status, 11):
			self.data += "**Primary ephemeris data gap, "
		if isBitSet(self.FDIRLevel1Status, 13):
			self.data += "**Primary GPS missing ephemeris, "
		if isBitSet(self.FDIRLevel1Status, 20):
			self.data += "**Secondary GPS data gap, "
		if isBitSet(self.FDIRLevel1Status, 21):
			self.data += "**Secondary GPS observable data gap, "
		if isBitSet(self.FDIRLevel1Status, 25):
			self.data += "Auxiliary GPS data gap, "
		if isBitSet(self.FDIRLevel1Status, 26):
			self.data += "**GAMS ambiguity resolution failed, "
		if isBitSet(self.FDIRLevel1Status, 30):
			self.data += "**IIN WL ambiguity error, "
		if isBitSet(self.FDIRLevel1Status, 31):
			self.data += "**IIN NL ambiguity error, "

		if isBitSet(self.FDIRLevel4Status, 0):
			self.data += "**Primary GPS position rejected, "
		if isBitSet(self.FDIRLevel4Status, 1):
			self.data += "**Primary GPS velocity rejected, "
		if isBitSet(self.FDIRLevel4Status, 2):
			self.data += "**GAMS heading rejected, "
		if isBitSet(self.FDIRLevel4Status, 3):
			self.data += "**Auxiliary GPS data rejected, "
		if isBitSet(self.FDIRLevel4Status, 5):
			self.data += "**Primary GPS observables rejected, "

		if isBitSet(self.FDIRLevel5Status, 0):
			self.data += "**X accelerometer failure, "
		if isBitSet(self.FDIRLevel4Status, 1):
			self.data += "**Y accelerometer failure, "
		if isBitSet(self.FDIRLevel4Status, 2):
			self.data += "**Z accelerometer failure, "
		if isBitSet(self.FDIRLevel4Status, 3):
			self.data += "**X gyro failure, "
		if isBitSet(self.FDIRLevel4Status, 4):
			self.data += "**Y gyro failure, "
		if isBitSet(self.FDIRLevel4Status, 5):
			self.data += "**Z gyro failure, "
		if isBitSet(self.FDIRLevel4Status, 6):
			self.data += "**Excessive GAMS heading offset, "
		if isBitSet(self.FDIRLevel4Status, 7):
			self.data += "**Excessive primary GPS lever arm error, "
		if isBitSet(self.FDIRLevel4Status, 8):
			self.data += "**Excessive auxiliary 1 GPS lever arm error, "
		if isBitSet(self.FDIRLevel4Status, 9):
			self.data += "**Excessive auxiliary 2 GPS lever arm error, "
		if isBitSet(self.FDIRLevel4Status, 10):
			self.data += "**Excessive POS position error RMS, "
		if isBitSet(self.FDIRLevel4Status, 11):
			self.data += "**Excessive primary GPS clock drift, "

		# now decode into a string.
		if isBitSet(self.generalStatusA, 0):
			self.data += "Coarse levelling active, "
		if isBitSet(self.generalStatusA, 1):
			self.data += "Coarse levelling failed, "
		if isBitSet(self.generalStatusA, 2):
			self.data += "Quadrant resolved, "
		if isBitSet(self.generalStatusA, 3):
			self.data += "Fine align active, "
		if isBitSet(self.generalStatusA, 4):
			self.data += "Inertial navigator initialised, "
		if isBitSet(self.generalStatusA, 5):
			self.data += "Inertial navigator alignment active, "
		if isBitSet(self.generalStatusA, 6):
			self.data += "Degraded navigation solution, "
		if isBitSet(self.generalStatusA, 7):
			self.data += "Full navigation solution, "
		if isBitSet(self.generalStatusA, 8):
			self.data += "Initial position valid, "
		if isBitSet(self.generalStatusA, 9):
			self.data += "Reference to Primary GPS Lever arms = 0, "
		if isBitSet(self.generalStatusA, 10):
			self.data += "Reference to Sensor 1 Lever arms = 0, "
		if isBitSet(self.generalStatusA, 11):
			self.data += "Reference to Sensor 2 Lever arms = 0, "
		if isBitSet(self.generalStatusA, 12):
			self.data += "Logging Port file write error, "
		if isBitSet(self.generalStatusA, 13):
			self.data += "Logging Port file open, "
		if isBitSet(self.generalStatusA, 14):
			self.data += "Logging Port logging enabled, "
		if isBitSet(self.generalStatusA, 15):
			self.data += "Logging Port device full, "
		if isBitSet(self.generalStatusA, 16):
			self.data += "RAM configuration differs from NVM, "
		if isBitSet(self.generalStatusA, 17):
			self.data += "NVM write successful, "
		if isBitSet(self.generalStatusA, 18):
			self.data += "NVM write fail, "
		if isBitSet(self.generalStatusA, 19):
			self.data += "NVM read fail, "
		if isBitSet(self.generalStatusA, 20):
			self.data += "CPU loading exceeds 55% threshold, "
		if isBitSet(self.generalStatusA, 21):
			self.data += "CPU loading exceeds 85% threshold, "

		if isBitSet(self.generalStatusB, 0):
			self.data += "User attitude RMS performance, "
		if isBitSet(self.generalStatusB, 1):
			self.data += "User heading RMS performance, "
		if isBitSet(self.generalStatusB, 2):
			self.data += "User position RMS performance, "
		if isBitSet(self.generalStatusB, 3):
			self.data += "User velocity RMS performance, "
		if isBitSet(self.generalStatusB, 4):
			self.data += "GAMS calibration in progress, "
		if isBitSet(self.generalStatusB, 5):
			self.data += "GAMS calibration complete, "
		if isBitSet(self.generalStatusB, 6):
			self.data += "GAMS calibration failed, "
		if isBitSet(self.generalStatusB, 7):
			self.data += "GAMS calibration requested, "
		if isBitSet(self.generalStatusB, 8):
			self.data += "GAMS installation parameters valid, "
		if isBitSet(self.generalStatusB, 9):
			self.data += "GAMS solution in use, "
		if isBitSet(self.generalStatusB, 10):
			self.data += "GAMS solution OK, "
		if isBitSet(self.generalStatusB, 11):
			self.data += "GAMS calibration suspended, "
		if isBitSet(self.generalStatusB, 12):
			self.data += "GAMS calibration forced, "
		if isBitSet(self.generalStatusB, 13):
			self.data += "Primary GPS navigation solution in use, "
		if isBitSet(self.generalStatusB, 14):
			self.data += "Primary GPS initialization failed, "
		if isBitSet(self.generalStatusB, 15):
			self.data += "Primary GPS reset command sent, "
		if isBitSet(self.generalStatusB, 16):
			self.data += "Primary GPS configuration file sent, "
		if isBitSet(self.generalStatusB, 17):
			self.data += "Primary GPS not configured, "
		if isBitSet(self.generalStatusB, 18):
			self.data += "Primary GPS in C/A mode, "
		if isBitSet(self.generalStatusB, 19):
			self.data += "Primary GPS in Differential mode, "
		if isBitSet(self.generalStatusB, 20):
			self.data += "Primary GPS in float RTK mode, "
		if isBitSet(self.generalStatusB, 21):
			self.data += "Primary GPS in wide lane RTK mode, "
		if isBitSet(self.generalStatusB, 22):
			self.data += "Primary GPS in narrow lane RTK mode, "
		if isBitSet(self.generalStatusB, 23):
			self.data += "Primary GPS observables in use, "
		if isBitSet(self.generalStatusB, 24):
			self.data += "Secondary GPS observables in use, "
		if isBitSet(self.generalStatusB, 25):
			self.data += "Auxiliary GPS navigation solution in use, "
		if isBitSet(self.generalStatusB, 26):
			self.data += "Auxiliary GPS in P-code mode, "
		if isBitSet(self.generalStatusB, 27):
			self.data += "Auxiliary GPS in Differential mode, "
		if isBitSet(self.generalStatusB, 28):
			self.data += "Auxiliary GPS in float RTK mode, "
		if isBitSet(self.generalStatusB, 29):
			self.data += "Auxiliary GPS in wide lane RTK mode, "
		if isBitSet(self.generalStatusB, 20):
			self.data += "Auxiliary GPS in narrow lane RTK mode, "
		if isBitSet(self.generalStatusB, 31):
			self.data += "Primary GPS in P-code mode, "

		if isBitSet(self.generalStatusC, 0):
			self.data += "Gimbal input ON, "
		if isBitSet(self.generalStatusC, 1):
			self.data += "Gimbal data in use, "
		if isBitSet(self.generalStatusC, 2):
			self.data += "DMI data in use, "
		if isBitSet(self.generalStatusC, 3):
			self.data += "ZUPD processing enabled, "
		if isBitSet(self.generalStatusC, 4):
			self.data += "ZUPD in use, "
		if isBitSet(self.generalStatusC, 5):
			self.data += "Position fix in use, "
		if isBitSet(self.generalStatusC, 6):
			self.data += "RTCM differential corrections in use, "
		if isBitSet(self.generalStatusC, 7):
			self.data += "RTCM RTK messages in use, "
		if isBitSet(self.generalStatusC, 8):
			self.data += "RTCA RTK messages in use, "
		if isBitSet(self.generalStatusC, 9):
			self.data += "CMR RTK messages in use, "
		if isBitSet(self.generalStatusC, 10):
			self.data += "IIN in DR mode, "
		if isBitSet(self.generalStatusC, 11):
			self.data += "IIN GPS aiding is loosely coupled, "
		if isBitSet(self.generalStatusC, 12):
			self.data += "IIN in C/A GPS aided mode, "
		if isBitSet(self.generalStatusC, 13):
			self.data += "IIN in RTCM DGPS aided mode, "
		if isBitSet(self.generalStatusC, 14):
			self.data += "IIN in code DGPS aided mode, "
		if isBitSet(self.generalStatusC, 15):
			self.data += "IIN in float RTK aided mode, "
		if isBitSet(self.generalStatusC, 16):
			self.data += "IIN in wide lane RTK aided mode, "
		if isBitSet(self.generalStatusC, 17):
			self.data += "IIN in narrow lane RTK aided mode, "
		if isBitSet(self.generalStatusC, 18):
			self.data += "Received RTCM Type 1 message, "
		if isBitSet(self.generalStatusC, 19):
			self.data += "Received RTCM Type 3 message, "
		if isBitSet(self.generalStatusC, 20):
			self.data += "Received RTCM Type 9 message, "
		if isBitSet(self.generalStatusC, 21):
			self.data += "Received RTCM Type 18 messages, "
		if isBitSet(self.generalStatusC, 22):
			self.data += "Received RTCM Type 19 messages, "
		if isBitSet(self.generalStatusC, 23):
			self.data += "Received CMR Type 0 message, "
		if isBitSet(self.generalStatusC, 24):
			self.data += "Received CMR Type 1 message, "
		if isBitSet(self.generalStatusC, 25):
			self.data += "Received CMR Type 2 message, "
		if isBitSet(self.generalStatusC, 26):
			self.data += "Received CMR Type 94 message, "
		if isBitSet(self.generalStatusC, 27):
			self.data += "Received RTCA SCAT-1 messageV, "


		if isBitSet(self.extendedStatus, 0):
			self.data += "Primary GPS in Marinestar HP mode, "
		if isBitSet(self.extendedStatus, 1):
			self.data += "Primary GPS in Marinestar XP mode, "
		if isBitSet(self.extendedStatus, 2):
			self.data += "Primary GPS in Marinestar VBS mode, "
		if isBitSet(self.extendedStatus, 3):
			self.data += "Primary GPS in PPP mode, "
		if isBitSet(self.extendedStatus, 4):
			self.data += "Aux. GPS in Marinestar HP mode, "
		if isBitSet(self.extendedStatus, 5):
			self.data += "Aux. GPS in Marinestar XP mode, "
		if isBitSet(self.extendedStatus, 6):
			self.data += "Aux. GPS in Marinestar VBS mode, "
		if isBitSet(self.extendedStatus, 7):
			self.data += "Aux. GPS in PPP mode, "
		if isBitSet(self.extendedStatus, 12):
			self.data += "Primary GPS in Marinestar G2 mode, "
		if isBitSet(self.extendedStatus, 14):
			self.data += "Primary GPS in Marinestar HPXP mode, "
		if isBitSet(self.extendedStatus, 15):
			self.data += "Primary GPS in Marinestar HPG2 mode, "


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
	#  time distance fields are dddBB
	POSPacketHeader_fmt = '=4shhdddBB'
	POSPacketHeader_len = struct.calcsize(POSPacketHeader_fmt)
	POSPacketHeader_unpack = struct.Struct(POSPacketHeader_fmt).unpack_from

###############################################################################
	def __init__(self, POSfileName):
		if not os.path.isfile(POSfileName):
			print ("file not found:", POSfileName)
		self.fileName = POSfileName
		self.fileptr = open(POSfileName, 'rb')		
		self.fileSize = os.path.getsize(POSfileName)
		self.recordDate = 0
		self.recordTime = 0
		self.timeOrigin = 0

		# now try and parse the filename for the GPS week.  There may be no datagram with this!
		#  default filename is in the format 20170403_0138.000, 20170403_0138.001 etc
		try:
			base = os.path.basename(POSfileName)
			name = os.path.splitext(base)[0]
			fileDate = datetime.datetime.strptime(name[0:8],"%Y%m%d")
			self.week, gpsWeekInSeconds, gpsDayofWeek, gpsSecondsOfWeek, microseconds = self.utcToWeekSeconds(fileDate, 16)
			self.timeOrigin = gpsWeekInSeconds
			# self.weekInSeconds = self.utcToWeekSeconds
			date = self.weekSecondsToUtc(self.week, 0,0)
			print ("FileName: %s GPS Week: %d $s" % (POSfileName, self.week, date))
		except:
			self.week = 0
			print ("filename does not contain a valid GPS week signature, timestamp correction needs to come from a datagram: ", POSfileName)
###############################################################################
	def __str__(self):
		return pprint.pformat(vars(self))

###############################################################################
	def currentRecordDateTime(self):
		'''return a python date object from the current datagram objects raw date and time fields '''
		# date_object = datetime.strptime(str(self.recordDate), '%Y%m%d') + timedelta(0,self.recordTime)
		date_object = from_timestamp(self.recordTime)
		return date_object

###############################################################################
	def to_DateTime(self, recordDate, recordTime):
		'''return a python date object from a split date and time record'''
		date_object = datetime.strptime(str(recordDate), '%Y%m%d') + timedelta(0,recordTime)
		return date_object

###############################################################################
# https://stackoverflow.com/questions/45422739/gps-time-in-weeks-since-epoch-in-python	
# utctoweekseconds(datetime.datetime.strptime('2014-09-22 21:36:52',"%Y-%m-%d %H:%M:%S"),16)
# gives: (1811, 1, 164196,0)
###############################################################################
###############################################################################
	def weekSecondsToUtc(self, gpsweek, gpsseconds, leapseconds):
		datetimeformat = "%Y-%m-%d %H:%M:%S"
		epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
		elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds+leapseconds))
		return datetime.datetime.strftime(epoch + elapsed,datetimeformat)

	def utcToWeekSeconds(self, utcDate, leapseconds):
		""" Returns the GPS week, the GPS day, and the seconds 
			and microseconds since the beginning of the GPS week """
		datetimeformat = "%Y-%m-%d %H:%M:%S"
		epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
		# tdiff = utcDate - epoch - datetime.timedelta(seconds=leapseconds)
		tdiff = utcDate - epoch
		gpsweek = tdiff.days // 7 
		gpsDayofWeek = tdiff.days - (7 * gpsweek)
		gpsSecondsOfWeek = tdiff.seconds + 86400* (tdiff.days - (7 * gpsweek))
		gpsWeekInSeconds = tdiff.seconds + 86400* (7 * gpsweek)

		# date = self.weekSecondsToUtc(gpsweek, gpsSecondsOfWeek, leapseconds)

		return gpsweek, gpsWeekInSeconds, gpsDayofWeek, gpsSecondsOfWeek,  tdiff.microseconds

###############################################################################
	def readDatagramHeader(self):
			'''read the common header for any datagram'''
			try:
				curr = self.fileptr.tell()
				data = self.fileptr.read(self.POSPacketHeader_len)
				s = self.POSPacketHeader_unpack(data)
				# now reset file pointer
				self.fileptr.seek(curr, 0)

				groupStart		= s[0]
				groupID			= s[1]
				numberOfBytes   = s[2]

				# we are dealing with messages rather than groups, so the format after the first 3 params is different, so quit.
				if groupStart.decode("utf-8") == "$MSG":
					# print ("message:", groupID)
					return numberOfBytes + 8, groupID, self.recordDate, self.recordTime

				self.recordDate			= s[3] + self.timeOrigin #GPS seconds of the week using user prefernece.  We normally use this and the default is fine
				self.recordTime			= s[4] + self.timeOrigin #GPS seconds of the week in POS time (time since startup)
				# distanceTag		= s[5]
				# timeTypes		= s[6]
								
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

		if groupID == 10: 
			dg = C_10(self.fileptr, numberOfBytes, self.timeOrigin)
			return dg.typeOfDatagram, dg 
		if groupID == 56: 
			dg = C_M56(self.fileptr, numberOfBytes, self.timeOrigin)
			return dg.typeOfDatagram, dg 
		if groupID == 110: 
			dg = C_110(self.fileptr, numberOfBytes, self.timeOrigin)
			return dg.typeOfDatagram, dg 
		if groupID == 111: 
			dg = C_111(self.fileptr, numberOfBytes, self.timeOrigin)
			return dg.typeOfDatagram, dg 
		if groupID == 112: 
			dg = C_112(self.fileptr, numberOfBytes, self.timeOrigin)
			return dg.typeOfDatagram, dg 
		
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
		return "True Heave"
	if (groupID == 112):
		return "NMEA"
	if (groupID == 113):
		return "True Heave Metrics"
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


def isBitSet(int_type, offset):
	'''testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.'''
	mask = 1 << offset
	return (int_type & (1 << offset)) != 0

def to_timestamp(recordDate):
	return (recordDate - datetime.datetime(1970, 1, 1)).total_seconds()

def from_timestamp(unixtime):
	return datetime.datetime(1970, 1 ,1) + timedelta(seconds=unixtime)
		
###############################################################################
if __name__ == "__main__":
		main()
