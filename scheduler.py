#!/usr/bin/python
import schedule, threading
from lineUp import LineUp

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
#	the total length of playtime each lineUp has.
#
#  ToDo:
#  	Implement 'Intelligence'
#  	Notifications: Use a config file to allow user to schedule notifications
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

class Scheduler:
	lineUp = LineUp()

	def __init__(self):
		self.scheduleEvents()
		self.loop()

	def scheduleEvents(self):
		schedule.every().hour.at(":00").do(self.run_threaded, self.updateCurHour)
		schedule.every(10).minutes.do(self.run_threaded, self.playNextSong)
#		ToDo: Use lineUp data to play songs periodically

	def updateCurHour(self):
	# The scheduler calls this method in a newly created thread
		self.lineUp.setCurHour()

	def playNextSong(self):
		# Play{ self.lineUp.nextSong() }
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

sched = Scheduler()
