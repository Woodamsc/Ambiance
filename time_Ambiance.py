#!/usr/bin/python
import time

def remainingMins():
	return ( 60 - curMin() );

def remainingSecs():
	return ( 3600 - curSec() );

def curHour():
	return time.localtime()[3];

def curMin():
	return time.localtime()[4];

def curSec():
	return time.localtime()[5];

def nextHour():
	return (curHour() + 1) % 24;

def secs2min(secs):
# always rounds up
	if secs % 60 != 0:
		return (secs / 60) + 1
	return secs / 60

def timeStr(numb):
# Formats a number so it's better
# time compatible.
# e.g. 5 => '05'
	if numb < 10:
		return '0' + str(numb)
	return str(numb);

def curTime():
	return timeStr(curHour()) + ':' +timeStr(curMin()) + ':' + timeStr(curSec());

