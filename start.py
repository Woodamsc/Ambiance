#!/usr/bin/python
# Every program has to start somewhere
import os, errno

from scheduler import Scheduler
from songQ import SongQ
from log import log
from time_Ambiance import *
from subprocess import call

timeSlots = dict()

def setup():
# Do some basic prep work. e.g. Generating folders
	for hour in xrange(0,24):
		timeSlots[hour] = timeStr(hour) + ':00'

	createTimeSlots()


def createTimeSlots():
	mkDir('TimeSlots')
	for hour in xrange(0,24):
		mkDir( os.path.join( 'TimeSlots', timeSlots[hour] ) );

def mkDir(dirName):
	try:
		os.mkdir( dirName )
		log( 'Setup', 'Created dir ' + str(dirName) )
	except Exception, e:
		if e.errno == 17:
			pass
		else:
			log('Setup', e)
			print( 'Uh-oh. Something weird occured. Check `.log` for more details')
			exit();

# - - - - - - #
# Start Here  #
# - - - - - - #

if call(['which', 'play']):
	print("'sox' is not installed or PATH is incorrectly set")
	exit(1)

log('Start', '#################################')
log('Start', '       Ambiance Launched         ')
log('Start', '#################################')
# Setup Directories
setup()
# Make the SongQ
songQ = SongQ(timeSlots, curHour())
# Start the Scheduler
Scheduler(songQ)

