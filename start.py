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
	for hour in range(0,24):
		timeSlots[hour] = timeStr(hour)

	createTimeSlots()


def createTimeSlots():
	mkDir('TimeSlots')
	mkDir('TimeSlots/Day')
	mkDir('TimeSlots/Day/Songs')
	mkDir('TimeSlots/Day/Background')
	mkDir('TimeSlots/Night')
	mkDir('TimeSlots/Night/Songs')
	mkDir('TimeSlots/Night/Background')
	for hour in range(0,24):
		if hour > 7 and hour < 20:
			mkDir( os.path.join( 'TimeSlots/Day', timeSlots[hour] ) )
			mkDir( os.path.join( 'TimeSlots/Day', timeSlots[hour], 'Songs' ) )
			mkDir( os.path.join( 'TimeSlots/Day', timeSlots[hour], 'Background' ) )
		else:
			mkDir( os.path.join( 'TimeSlots/Night', timeSlots[hour] ) );
			mkDir( os.path.join( 'TimeSlots/Night', timeSlots[hour], 'Songs' ) );
			mkDir( os.path.join( 'TimeSlots/Night', timeSlots[hour], 'Background' ) );

def mkDir(dirName):
	try:
		os.mkdir( dirName )
		log( 'Setup', 'Created dir ' + str(dirName) )
	except Exception as e:
		if e.errno == 17:
			pass
		else:
			log('Setup', e)
			print( 'Uh-oh. Something weird occured. Check `.log` for more details')
			exit();

# - - - - - - #
# Start Here  #
# - - - - - - #

log('Start', '#################################')
log('Start', '       Ambiance Launched         ')
log('Start', '#################################')
# Setup Directories
setup()
# Make the SongQ
songQ = SongQ(timeSlots, curHour())
# Start the Scheduler
Scheduler(songQ)

