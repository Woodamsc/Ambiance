#!/usr/bin/python

from log 			 import log
from scheduler 	 import Scheduler
from subprocess	 import call, check_output
from mutagen.mp3 	 import MP3
from time_Ambiance import *

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

SELDOM	= 10
PERIODIC	= 5
OFTEN		= 2

class SongQ:
	FREQ			= PERIODIC
	songQ			= []		# Current music lineup for the hour
	songQIndex	= 0		# Index for songs within the queue
	nextSongQ	= []		# Next hour's song queue
	timeSlots 	= dict()	# Holds dir names for each hour
	scheduler	= None
	
	def __init__(self, timeSlots, scheduler_obj):
			self.timeSlots = timeSlots
			self.scheduler = scheduler_obj

	def loadNextSongQ(self):
		log('SongQ', 'Loading next SongQ')
		self.songQ, self.nextSongQ = self.nextSongQ, []

	def playNextSong(self):
	# Check size of Q, increment and play song if possible
   # Wrap around when you reach the end
		Qsize = len(self.songQ)
		if Qsize > 0:
			oldIndex = self.songQIndex
			if self.songQIndex < Qsize-1: 	# The -1 is proper
				self.songQIndex += 1
			else:
				self.songQIndex  = 0
			song = self.songQ[oldIndex]
			self.play(song)
		else:
			self.songQIndex = 0;
			log( 'SongQ' 'No song loaded to play' );

	def play(self, song):
		if song == None: return # log it
		call(['play', '-q', song])
		log( 'SongQ' 'Now playing \'' + str(song) + '\'' )

		# Schedule next song
		playTime = int(self.songPlayTime(song))
#???	minute	= self.FREQ + (secs2min(playTime) / 60 + curMin())
		minute	= self.FREQ + (secs2min(playTime) + curMin())
		nextPlay = timeFormat( curHour(), minute )
		# Schedule playNextSong at nextPlay
		

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
		return float(check_output(['soxi','-D', song]).strip())

	def setNextSongQ(self, nextSongQ):
	# Just a setter. Apparently these are bad in python or something?
		self.nextSongQ = nextSongQ
		log('SongQ', 'Recieved next hours songQ: ' + str(nextSongQ)

