#!/usr/bin/python
import os, errno
from log import log
from time_Ambiance import *
from random import shuffle
from mutagen.mp3 import MP3
# Purpose/Function:
#	load audio files to be played and looped as background noise
#
# Notes:
# 	This class assumes all paths are full qualified
# 	and doesn't do much defensive programming against the otherwise
#

class Background:
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

		for curDir, subDirs, files in os.walk( os.path.join( 'TimeSlots', ToD, 'Backround' ) ):
			for curFile in files:
				audioFile = os.path.join(curDir, curFile)
				self.nextSongQ.append( audioFile )

		for files in os.walk( os.path.join( 'TimeSlots', ToD, str(hour), 'Background' ) ):
			for curDir, subDirs, curFile in files:
				audioFile = os.path.join(curDir, curFile)
				self.nextSongQ.append( audioFile )

	def hourlyUpdate(self):
		log('SongQ', 'Loading next SongQ')
		self.songQ, self.nextSongQ = self.nextSongQ, []

	def nextSong(self):
	# Return current indexed song, then increase index (if possible)
		Qsize = len(self.songQ)
		if Qsize > 0:
			oldIndex = self.songQIndex
			if self.songQIndex < Qsize-1: 	# The '-1' is proper
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

	def songPlayTime(self, song):
	# Returns playtime of a song in seconds
		return MP3(song).info.length;

