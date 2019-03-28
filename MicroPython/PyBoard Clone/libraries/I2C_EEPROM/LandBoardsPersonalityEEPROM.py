# LandBoardsPersonalityEEPROM.py
# Methods for handling Land Boards Personality EEPROMs
# Uses I2C_EEPROM library
#	Library provides lower level methods for read/write of EEPROMs
# Personality EEPROM contents are described here
#	http://land-boards.com/blwiki/index.php?title=Open_Data_Acquisition_System#Personality_EEPROM
# 	Data Structure (in C) is:
#		struct eep_vals
#		{
#		  char signature[4]; // "ODAS" in ASCII
#		  byte fmt_version;  // EEPROM data format version (0x00 reserved, 0x01 = first version)
#		  byte rsvd;         // set to 0
#		  short numatoms;    // set to 2
#		  long eeplen;       // set to 96 dec
#		  char uuid[16];     // "0000000000000000" in ASCII
#		  short pid;         // See PID table
#		  char vslen;        // set to 32 dec
#		  char pslen;        // set to 32 dec
#		  char vstr[32];     // Vendor Null terminated String
#		  char pstr[32];     // Product Null terminated String
#		};
# Code is a port of the Arduino sketch
#	https://github.com/land-boards/lb-Arduino-Code/blob/master/LBCards/ODAS/ODASTESTER/ODASEEPROM.ino
#
# Product ID (pid) table  
PID_NONE=0
PID_DIGIO16I2C_CARD=1
PID_DIGIO128_CARD=2
PID_DIGIO128_64_CARD=3
PID_OPTOIN8I2C_CARD=4
PID_OPTOOUT8I2C_CARD=5
PID_DIGIO32I2C_CARD=6
PID_PROTO16I2C_CARD=7
PID_ODASPSOC5_CARD=8
PID_ODASRELAY16_CARD=9
PID_NEW_CARD=499
PID_NOEEPROMAFTER=500
PID_I2CIO8_CARD=501
PID_I2CIO8X_CARD=502
PID_OPTOFST_SML_NON_INVERTING_CARD=503
PID_OPTOFST_SML_INVERTING_CARD=504
PID_I2CRPT01_CARD=505
PID_SWLEDX8_I2C_CARD=506

def getPID(pidString):
	pidDict={
	PID_DIGIO16I2C_CARD : "DIGIO16-I2C",
	PID_DIGIO128_CARD : "DIGIO-128",
	PID_DIGIO128_64_CARD : "DIGIO-128/64",
	PID_OPTOIN8I2C_CARD : "OptoIn8-I2C",
	PID_OPTOOUT8I2C_CARD : "OptoOut8-I2C",
	PID_DIGIO32I2C_CARD : "DIGIO32-I2C",
	PID_PROTO16I2C_CARD : "PROTO16-I2C",
	PID_ODASPSOC5_CARD : "ODAS-PSOC5",
	PID_ODASRELAY16_CARD : "ODAS-RELAY16"
	}
	
