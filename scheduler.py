#!/usr/bin/python
import schedule
from threading import Thread
from time import sleep
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
	SLEEP_TIME = .1

	def __init__(self):
		log('Scheduler', 'Scheduler created')
		self.loop()

	def loop(self):
	# Main loop
		log('Scheduler', 'Looping - waiting for pending tasks')
		while True:
			schedule.run_pending()
			sleep(self.SLEEP_TIME)

def unregister(job):
	schedule.cancel_job(job);

def register_func_hourly_tail(func, *args):
	return register_func_hourly_at( 59, func, args)

def register_func_hourly_head(func, *args):
	return register_func_hourly_at( 0, func, args)

def register_func_hourly_at(minute, func, *args):
	time = timeFormat( "", minute )
	j = schedule.every().hour.at(time).do( run_threaded, func, *args )
	return j

def run_threaded(func, *args):
# This will run any provided function in its own thread
	func_threaded = Thread(target=func, args=args)
	func_threaded.start();

