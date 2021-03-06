#!/usr/bin/python
import os, errno, mutagen
from log import log
from time_Ambiance import *
from random import shuffle

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
#	Add support for multiple types of music files
#		currently only supporting mp3

class SongQ:
	songQ			= []				# Current music lineup for the hour
	nextSongQ	= []				# Next hour's song queue
	timeSlots 	= dict()			# Stores Directory name locations for each hour
	songQIndex	= 0				# Index for songs within the queue
	
	def __init__(self, timeSlots, hour):
			self.timeSlots = timeSlots
			self.loadNextSongQ(hour); 
			self.hourlyUpdate()

	def loadNextSongQ(self, hour):
	# Loads new songs for the given hour and randomizes the queue
		hour = hour % 24 # Ensure sanitized input
		ToD = 'Night'
		if hour > 7 and hour < 20:
			ToD = 'Day'
		hour = timeStr(hour)

		# Scan the `ToD`/Song directory for songs to play
		for curDir, subDirs, files in os.walk( os.path.join( 'TimeSlots', ToD, 'Songs' ) ):
			for curFile in files:
				file = os.path.join(curDir, curFile)
				if self.isAudioFile( file ):
					self.nextSongQ.append( file )

		# Now scan the `ToD`/`hour`/Song directory for songs to play
		for curDir, subDirs, files in os.walk( os.path.join( 'TimeSlots', ToD, str(hour), 'Songs' ) ):
			for curFile in files:
				file = os.path.join(curDir, curFile)
				if self.isAudioFile( file ):
					self.nextSongQ.append( file )

		shuffle(self.nextSongQ);

	def hourlyUpdate(self):
		log('SongQ', 'Loading next SongQ')
		self.songQ, self.nextSongQ = self.nextSongQ, []

	def nextSong(self):
	# Return current indexed song, then increase index (if possible)
		Qsize = len(self.songQ)
		if Qsize > 0:
			oldIndex = self.songQIndex
			if self.songQIndex < Qsize-1: 	# The '-1' is correct
				self.songQIndex += 1
			else:
				self.songQIndex  = 0
			return self.songQ[oldIndex]
		else:
			self.songQIndex = 0
			return None;

	def getSongQInfo(self):
	# Return total time of all songs in the Song Queue in seconds
		return ( self.songQPlayTime(), len(self.songQ) );

	def songQPlayTime(self):
		totalTime = 0
		for song in self.SongQ:
			totalTime = totalTime + self.songPlayTime(song)
		return totalTime;
	
	def isAudioFile(self, song):
		try:
			fTypes = mutagen.File(song).mime
			for fType in fTypes:
				if 'audio' in fType:
					return True
		except:
			log( 'SongQ', 'Mutagen could not determine file type of ' + str(song) + ', or it has no mime types' )
		return False;

	def songPlayTime(self, song):
	# Returns playtime of a song in seconds
		try:
			playTime = int( float( mutagen.File(song).info.length) );
		except:
			log('SongQ', 'Mutagen could not get play time of ' + str(song) + '. Removing from Queue')
			playTime = 0
# 		remove from queue
		return playTime;
