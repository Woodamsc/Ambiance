#!/usr/bin/python
from time_Ambiance import *

# Purpose/Function:
#  A generic logger to allow separate classes to
#  output information to a singular generic log file.

def log(who, data):
	with open('.log', 'a+') as fOut:
		info = curTime() + '| ' + str(who)
		fOut.write( info + ' - '.rjust(22-len(info)) + str(data).ljust(23) + '\n')
