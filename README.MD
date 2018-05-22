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
* determine the GPS week so we can probide correct time stamps
* test the file name for the GPS week
* test the NMEA strings for GPS week
* test the group 3 message for GPS week (primary GPS)
* test the group 11,12,13 message for GPS week (aux GPS)
* 
* DONE
* basic loop through the file reading the header and skipping the data
* core loop

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
    * ALL types to python struct types
    * signed char = 1 byte = "b"
    * unsigned char = 1 byte = "B"
    * XTFWORD = signed short int 2 bytes = h
    * XTFWORD = UNsigned int 2 bytes = H (for unipolar data)
    * DWORD = unsigned int 4 bytes = "L"
    * short = short integer 2 bytes = "h"
    * char = 1 byte = "c"
	* double = 8 bytes = "d"
	* string = n bytes = "s"

