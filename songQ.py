#!/usr/bin/python

from log 			 import log
from subprocess	 import call, check_output, Popen
from time_Ambiance import *
import scheduler

# Purpose/Function:
#	Handles all logic for playing Songs during an hour.
#	Determines how often to play a song, and the interval
#	between songs.
#
# Notes:
# 	This class assumes all paths are full qualified
# 	and doesn't do much defensive programming against the otherwise
#

SELDOM	= 10
PERIODIC	= 5
OFTEN		= 2

class SongQ:
	FREQ			= 1
	songQ			= []		# Current music lineup for the hour
	songQIndex	= 0		# Index for songs within the queue
	timeSlots 	= dict()	# Holds dir names for each hour
	nextSongJob = None	# Holds Job ID of a scheduled task
	
	def __init__(self, timeSlots):
		log('SongQ', 'SongQ created')
		self.timeSlots = timeSlots

	def loadNextSongQ(self, newSongQ):
		log('SongQ', 'Loading next SongQ')
		self.songQ = newSongQ;

	def playNextSong(self, *args):
		self.play( self.incrementSongQ() )
		self.scheduleNextSong();

	def incrementSongQ(self):
		Qsize = len(self.songQ)
		if Qsize < 1:
			self.songQIndex = 0
			log( 'SongQ', 'No songs are loaded to play' );
		else:
			oldIndex = self.songQIndex
			if self.songQIndex < Qsize-1: 	# The -1 is proper
				self.songQIndex += 1
			else:
				self.songQIndex  = 0
			return self.songQ[oldIndex]
		return None;

	def play(self, song):
		if self.nextSongJob != None:
			scheduler.cancel_registration(self.nextSongJob)
		if song == None: return # log it
		# Wrap in try/except?
		Popen(['play', '-q', str(song)]) # Runs in background
		log( 'SongQ', 'Now playing \'' + str(song) + '\'' )
		# Shorten the song var down to just its name for logging

	def scheduleNextSong(self):
		song = self.nextSong()
		playTime = int( self.songPlayTime(song) )
		minute	= self.FREQ + (secs2min(playTime) + curMin())
		if minute <= 0 or minute > 60:
			log('songQ', 'End of hour, did not reschedule')
			return
		self.nextSongJob = scheduler.register_func_hourly_at(\
								 minute, self.playNextSong )
		log('SongQ', 'Next song scheduled to play at ' +
											str(self.nextSongJob.next_run) )

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
		# Wrap in try/except?
		return float(check_output(['soxi','-D', song]).strip())

	def nextSong(self):
		index = self.songQIndex + 1
		if index == len(self.songQ):
			index = 0
		return self.songQ[index]

	def curSong(self):
		return self.songQ[self.songQIndex]

