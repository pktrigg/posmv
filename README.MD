POSMVRead.py
=====
* created:          May 2018
* version           1.0.
* by:               paul.kennedy@guardiangeomatics.com
* description:      python module to read an Applanix .000 binary file
* notes:            See main at end of script for example how to use this
* based on ICD file version 4  
* developed for Python version 3.4 

* 2DO
* 
* DONE
* test the file name for the GPS week
* determine the GPS week so we can provide correct time stamps
* basic loop through the file reading the header and skipping the data
* core loop
* MESSAGE 56 does not change in terms throughout the file of timestamp or date.  All messages are identical

Time Of Week
* test the group 11,12,13 message for GPS week (aux GPS)
* test the group 3 message for GPS week (primary GPS)
* test the NMEA strings for GPS week

##GROUPS##
0 - 99 POS Core User data groups
100 - 199 POS MV User data groups
200 - 299 POS AV User data groups
300 - 399 POS TG User data groups
400 - 499 POS LV User data groups
500 - 599 POS LS User data groups
600 - 699 POS SV User data groups
700 - 799 POS MC User data groups
800 - 9999 Reserved
10000 - 10099 POS Core Raw data groups
10100 - 10199 POS MV Raw data groups
10200 - 10299 POS AV Raw data groups
10300 - 10399 POS TG Raw data groups
10400 - 10499 POS LV Raw data groups
10500 - 10599 POS LS Raw data groups
10600 - 10699 POS SV Raw data groups
10700 - 10799 POS MC Raw data groups
10800 - 19999 Reserved
20000 POS Core User diagnostic group
20001 - 20099 POS Core Proprietary diagnostic groups
20100 POS MV User diagnostic group


Data Type Conversions from POS to Python::
https://docs.python.org/2/library/struct.html
    * ALL types to python struct types
    * signed char = 1 byte 				= "b"
    * unsigned char = 1 byte 			= "B"

    * signed int 4 bytes 				= "i"
    * UNsigned int 4 bytes 				= "I"

    * signed long int 4 bytes 			= "l"
    * UNsigned long int 4 bytes 		= "L"

    * signed short integer 2 bytes 		= "h"
    * UNsigned short integer 2 bytes 	= "H"

	* double = 8 bytes 					= "d"
	* float = 4 bytes 					= "f"
    
	* char = 1 byte 					= "c"
	* string = n bytes 					= "s"

