#!/usr/bin/python
import schedule, threading, time
from songQ import SongQ

# Mac only testing stuff
import subprocess

# Purpose/Function:
# 	Provide accurate scheduling for playing music
# 	throughout the day, and do so with 'intelligence'.
#
# Intelligence Definition:
# 	Have three options
# 		(1) Seldom  - - 10 minutes
# 		(2) Periodic  - 05 minutes
# 		(3) Often - - - 02 minutes
#	This is how much time separates one song from the next.
#	i.e. How much silence between songs
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
		self.loop()

	def scheduleAllEvents(self):
	# Does initial scheduling, only called once. Better method name?...
	# We schedule songQ swapping, how often to play the next song,
	# and start immediately playing the next song 
		schedule.every().hour.at(":59").do( self.run_threaded, 
														self.songQ.loadNextSongQ, 
														self.nextHour() )

		schedule.every().hour.at(":00").do( self.run_threaded,
														self.hourlyUpdates )

#		There shouldn't be a need to schedule the nextSongJob here.
#		We'll atempt to play and schedule the next song on the next line.
#		The only situation where a song won't immediately play is if
#		it's playTime is longer than the time remaining in the hour.
#		In which case, hourlyUpdates() is called & will create a scheduled
#		job to call playNextSong()
		self.playNextSong()

	def playNextSong(self):
		song = self.songQ.nextSong() 					# Note this will increment songQIndex
		if song != None:									# regardless if it is actually played
			playTime = self.songQ.songPlayTime(song)
			if playTime <= self.remainingSeconds():
				newTime = '0' + str(self.curHour()) + ':' + ( (str(self.FREQ) + playTime) / 60 )
				self.nextSongJob = schedule.at(newTime).do(self.run_threaded, self.playNextSong)
# NEEDS TESTING ^
				subprocess.call(["afplay", song]) 	# OSX ONLY

	def hourlyUpdates(self, *unused):
		self.songQ.hourlyUpdate()
		schedule.cancel_job(self.nextSongJob) 		# Necessary? The var is overwritten anyway
		self.playNextSong()
#		self.nextSongJob = schedule.every(self.FREQ).minutes.do(self.run_threaded, 
#												self.playNextSong	)

	def run_threaded(self, func, *args):
	# This will run any provided function in its own thread
		func_threaded = threading.Thread(target=func, args=args)
		func_threaded.start();

	def loop(self):
	# Main loop
		while True:
			schedule.run_pending()

	def curHour(self):
		return time.localtime()[3]

	def nextHour(self):
		return (self.curHour() + 1) % 24;

	def remainingMinutes(self):
		return (60 - time.localtime()[4] );

	def remainingSeconds(self):
		return self.remainingMinutes() * 60;

