#!/usr/bin/python
import schedule, threading, time

from subprocess import call
from log import log
from time_Ambiance import *
from songQ import SongQ

# Purpose/Function:
# 	Provide accurate scheduling for playing audio files
# 	throughout the day.
#
# 	Have three options
# 		(1) Seldom  - - 10 minutes
# 		(2) Periodic  - 05 minutes
# 		(3) Often - - - 02 minutes
#	This is how much time separates one song from the next.
#	i.e. How much silence inbetween songs
#
#	This should also dictate background noise when we get
#	there.
#
#	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-
#
#  ToDo:
#  	Notifications: Use a config file to allow user to schedule 
#  					notifications.
#  				   e.g. At Noon play a specific title
#  				   Consider how to interrupt music currently playing	
#
# Notes:
# 	I'm making use of the schedule module. It seems
# 	to be the only module that provides cron-like
# 	capabilities.
# 	schedule 0.3.0 (current): https://pypi.python.org/pypi/schedule
# 	Example: https://github.com/dbader/schedule/blob/master/FAQ.rst
# 	Example: https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py

SELDOM	= 10
PERIODIC = 5
OFTEN		= 2

class Scheduler:
	songPlaying = False		# Pretty straightforward boolean
	nextSongJob = None		# Holds the job that periodically plays the next song
	songQ = None				# Variable for our SongQ class
	FREQ	= 	PERIODIC			# Default is Periodic = 5 minutes

	def __init__(self, songQ):
		self.songQ = songQ
		self.scheduleAllEvents()
		self.loop()

	def scheduleAllEvents(self):
	# Does initial scheduling, only called once. Better method name?...
	# We schedule songQ swapping, how often to play the next song,
	# and start immediately playing the next song 
		schedule.every().hour.at(":59").do( run_threaded, 
														self.songQ.loadNextSongQ, 
														nextHour() )

		schedule.every().hour.at(":00").do( run_threaded,
														self.hourlyUpdates )

#		There shouldn't be a need to schedule the nextSongJob here.
#		We'll atempt to play and schedule the next song on the next line.
#		The only situation where a song won't immediately play is if
#		it's playTime is longer than the time remaining in the hour.
#		In which case, hourlyUpdates() is called & will create a scheduled
#		job to call playNextSong()
		self.playNextSong()

	def playNextSong(self):
		log('Scheduler', 'Loading next song')
		song = self.songQ.nextSong()
		log('Scheduler', 'Loaded \''+str(song)+'\'')
		if song != None:
			play(song)

			playTime = int(self.songQ.songPlayTime(song))
			hour     = timeStr(curHour())
			minute   = timeStr(self.FREQ + (secs2min(playTime) / 60) + curMin())
			newTime  = str( hour + ':' + minute )
			if int(minute) < 60 and int(minute) >= 0:
				self.nextSongJob = schedule.every().hour.at(':'+minute).do( 
																				run_threaded,
																				self.playNextSong )
				log('Scheduler', 'Scheduled next song for ' + newTime)
			else:
				schedule.cancel_job(self.nextSongJob) # should get cancelled soon anyway
				log('Scheduler', 'End of hour, did not reschedule.')

	def hourlyUpdates(self, *unused):
		log('Scheduler', 'Turn of hour, running updates')
		self.songQ.hourlyUpdate()
		schedule.cancel_job(self.nextSongJob) # this is necessary
		self.playNextSong()

	def loop(self):
	# Main loop
		while True:
			schedule.run_pending()
			time.sleep(.5)

def play(song):
	log('Scheduler', 'Now playing \''+str(song)+'\'')
	call(['play', '-q', song])	# sox must be installed
										# libsox-fmt-mp3 to support mp3 files

def run_threaded(func, *args):
# This will run any provided function in its own thread
	func_threaded = threading.Thread(target=func, args=args)
	func_threaded.start();

