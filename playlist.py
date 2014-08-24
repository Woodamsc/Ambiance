#!/usr/bin/python3
import os, errno

# Load music to be played 00:00 - 23:59
# Each time slot can have any number of songs (including 0)
# PlayList class receives requests for the next song to play
# and determines which song to play, then returns it

class Playlist:
	self.schedule = dict()

	def __init__(self):
			self.createTimeSlots() # Just attempt to make dirs instead of finding missing
			self.schedule = self.fillTimeSlots()
  
	# Scan through directories & files in 'TimeSlots' directory.
	# Subfolders of 'TimeSlots' are an hour for each in the day.
	# Each subfolder is an entry in the dict() (a timeSlot),
	# then files therein are appended to that given timeslot
	def fillTimeSlots(self):
		timeSlot = dict()
		for curDir, subDirs, files in os.walk('TimeSlots'):
			for curFile in files:
				timeSlot['curDir'].append( os.path.join(curDir, curFile) )
		return timeSlot

	def createTimeSlots(self):
			self.mkFile('TimeSlots')
			for hour in xrange(0,24):
				time = '0' + str(hour) + ':00'
				if hour > 9:
					time = time[1:]
				self.mkFile( os.path.join( 'TimeSlots', 'Slot: ' + time ) )

	def mkFile(self, path):
			try:
				os.mkdir( path )
			except Exception as e:
				if e.errno == 17: # File Exists Error, OK move on to next dir
					pass
				else: # Something whacky happened
					print(e)
				exit()

	def nextSong(self):
		# Based off of current time, time since last play
		# Maybe amount of plays per hour goes by config file?
		# Remember to handle repeating after 24 hours
		# return schedule[hour][song_index]
		pass

	
play = Playlist()
