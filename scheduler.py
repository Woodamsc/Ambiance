#!/usr/bin/python
import schedule, threading, time
from songQ import SongQ

# Purpose/Function:
# 	Provide accurate scheduling for playing music
# 	throughout the day, and do so with 'intelligence'.
#
# Intelligence Definition:
# 	Have three options as core modifiers:
# 		(1) Seldom  - - 20 minutes
# 		(2) Periodic  - 10 minutes
# 		(3) Often - - - 05 minutes
#	A song will be played at every increment.
#	The songQ is randomly filled, so there should
#	be a good mix of songs after each rescheduling
#
#  ToDo:
#  	Notifications: Use a config file to allow user to schedule notifications
#  				   e.g. At Noon play a specific title
#  				   Consider how to interrupt music currently playing	
#  	Use os module to play songs - use os default program to play
#
# Notes:
# 	I'm making use of the schedule module. It seems
# 	to be the only module that provides cron-like
# 	capabilities.
# 	schedule 0.3.0 (current): https://pypi.python.org/pypi/schedule
# 	Example: https://github.com/dbader/schedule/blob/master/FAQ.rst
# 	Example: https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py

class Scheduler:
	songPlaying = False		# Pretty straightforward boolean
	nextSongJob = None		# Holds the job that periodically plays the next song
	songQ = None				# Variable for our SongQ class
	FREQ	= 10					# Default is Periodic = 10 minutes

	def __init__(self):
		self.songQ = SongQ(self.curHour())
		self.scheduleAllEvents()
		# Load songQ initially and play next song
		self.loop()

	def scheduleAllEvents(self):
		schedule.every().hour.at(":55").do(self.run_threaded, self.songQ.loadNextSongQ(
																							  self.curHour() + 1) )
		schedule.every().hour.at(":59").do(self.run_threaded, self.hourlyUpdates)

	def playNextSong(self):
		song = self.songQ.nextSong() 					# Note this will increment songQIndex
		playTime = self.songQ.songPlayTime(song)	# regardless if it is actually played
		if playTime <= self.remainingTime():
			self.songPlaying = True
			# os.play{ self.songQ.nextSong() }

	def hourlyUpdates(self):
		self.songQ.hourlyUpdate()
		schedule.cancel_job(nextSongJob) 				# Every hour, recalc freq because there
		#size, playTime = self.songQ.getSongQInfo()	# can be different songQ size ?ToDo?
		nextSongJob = schedule.every(	self.FREQ).minutes.do(self.run_threaded, 
												self.playNextSong	)
		# Right now the FREQ isn't recalculated every hour.
		# I haven't decided on it's behavior quite yet

	def run_threaded(self, func):
		# This will run any provided function in its own thread
		func_threaded = threading.Thread(target=func)
		func_threaded.start()

	def loop(self):
		# Main loop
		while True:
			schedule.run_pending()

	def curHour(self):
		return time.localtime()[3] # Grabs hour out of localtime index

	def remainingTime(self):
		return time.localtime[4] - 60

sched = Scheduler()

