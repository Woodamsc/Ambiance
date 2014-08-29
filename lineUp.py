#!/usr/bin/python
import os, errno, time

# Purpose/Function:
#	Load music to be played for each hour
#	Each time slot can have any number of songs (including 0)
#	TimeSlots are subfolders in the 'TimeSlots' directory
#	PlayList class receives requests for the next song to play
#	and determines which song to play, then returns it.
#	It will only have music for the current (and next?) hour
#	loaded into a lineup (nextHourLineUp?)
#
# Notes:
# 	This class assumes all paths are full qualified
# 	and doesn't do much defensive programming against the otherwise
#
# ToDo:
# 	Instead of loading all song titles from all hours of the day,
# 	just load all songs for the current hour
# 	 -> Theoretically, then, you could adjust music before it loads
# 	 	 in the next hour...

class LineUp:
	curHour  = int				# Current hour of day (necessary?)
	lineUp	= list()			# Current music lineup for the hour
	lineUpIndex = 0			# Index for songs within the lineup
	timeSlots = dict()		# Stores Directory name locations for each hour
									# Just easier to reference the dirs this way
	
	for hour in xrange(0,24):	# Dirty way to fill the dict() 
		time = '0' + str(hour) + ':00'
		if hour > 9:
			time = time[1:]
		timeSlots[hour] = 'Slot: ' + time	# Done filling 

	def __init__(self):
			self.setCurHour()
			self.createTimeSlots()
			self.loadLineUp(self.curHour); 
  
	def loadLineUp(self, hour):
	# Removes old songs, then loads new songs from the given hour
		for song in self.lineUp:
			self.lineUp.pop()
		for curDir, subDirs, files in os.walk( os.path.join( 'TimeSlots', self.timeSlots[hour] ) ):
			for curFile in files:
				self.lineUp.append( os.path.join(curDir, curFile) );

	def createTimeSlots(self):
			self.mkFile('TimeSlots')
			for hour in xrange(0,24):
				self.mkFile( os.path.join( 'TimeSlots', self.timeSlots[hour]) );

	def mkFile(self, path):
	# Attempts to make a file/dir. If it exists, fails silently
			try:
				os.mkdir( path )
			except Exception as e:
				if e.errno == 17: # File Exists Error, OK move on to next dir
					pass
				else: # Something whacky happened
					print(e)
					exit();

	def nextSong(self):
		if lineUpIndex >= len(lineUp):
			lineUpIndex = 0
		else:
			 lineUpIndex += 1
		return self.lineUp[lineUpIndex];

	@curHour.setter
	def setCurHour(self):
	# Sets it to the hour portion of a struct_time object
		self.curHour = time.localtime()[3];

	@property
	def getLineUpSize():
		# return ( lineUp.playtime, len(lineUp) )
		pass


