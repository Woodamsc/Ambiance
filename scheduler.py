#!/usr/bin/python
import schedule, threading, time
from subprocess import call
from log import log
from time_Ambiance import *
from songQ import SongQ

# Purpose/Function:
#	Sort of an interface to the schedule import
#	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-
#
# Notes:
# 	I'm making use of the schedule module. It seems
# 	to be the only module that provides cron-like
# 	capabilities.
# 	schedule 0.3.0 (current): https://pypi.python.org/pypi/schedule
# 	Example: https://github.com/dbader/schedule/blob/master/FAQ.rst
# 	Example: https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py

class Scheduler:

	def __init__(self):
		log('Scheduler', 'Scheduler created')
		self.loop()

	def loop(self):
	# Main loop
		while True:
			schedule.run_pending()
			time.sleep(.5)

def cancel_registration(job):
	schedule.cancel_job(job);

def register_func_hourly_tail(func, *args):
	register_func_hourly_at(0, 59, func, args)

def register_func_hourly_head(func, *args):
	register_func_hourly_at(0, 0, func, args)

def register_func_hourly_at(hour, minute, func, *args):
	time = timeFormat( hour, minute )
	schedule.every().hour.at(time).do( run_threaded, func, *args )

def run_threaded(func, *args):
# This will run any provided function in its own thread
	func_threaded = threading.Thread(target=func, args=args)
	func_threaded.start();

