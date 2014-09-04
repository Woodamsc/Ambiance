#!/usr/bin/python
import schedule, threading, time
from songQ import SongQ

# Purpose/Function:
# 	Provide accurate scheduling for playing music
# 	throughout the day, and do so with 'intelligence'.
#	Also keeps the LineUp class' curHour variable
#	up to date.
#
# Intelligence Definition:
# 	Have three options as core modifiers:
# 		(1) Seldom
# 		(2) Periodic
# 		(3) Often
#	These choices adjust the frequency songs are
#	played; the amount of time  before playing the next song.
#	The full ratio is determined with this modifier and
#	the total length of playtime each songQ has.
#
#  ToDo:
#  	Implement 'Intelligence'
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
	songQ = SongQ(time.localtime()[3])

	def __init__(self):
		self.scheduleEvents()
		self.loop()

	def scheduleEvents(self):
		schedule.every().hour.at(":55").do(self.run_threaded, self.songQ.loadNextSongQ(self.curHour() + 1) )
		schedule.every().hour.at(":59").do(self.run_threaded, self.songQ.hourlyUpdate)
		schedule.every(10).minutes.do(self.run_threaded, self.playNextSong)
#		ToDo: Use songQ data to play songs periodically

	def playNextSong(self):
		# os.play{ self.songQ.nextSong() }
		# Set flag to indicate song is playing 
		pass

	def run_threaded(self, func):
		# This will run any provided function in its own thread
		func_threaded = threading.Thread(target=func)
		func_threaded.start()


	def loop(self):
		# Main loop
		while True:
			schedule.run_pending()

	def curHour(self):
		return time.localtime()[3]
sched = Scheduler()
