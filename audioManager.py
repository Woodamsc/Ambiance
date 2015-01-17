#!/usr/bin/python

import scheduler
from songQ import SongQ
from log import log
from time_Ambiance import *
from os import path, walk
from random import shuffle

# Purpose/Function:
#  Load all audio files and appropriately
#  assign them to their intended purpose.
#  This won't worry about when to play the audio files,
#  it just reads them from disk and puts them into memory.
#
#  Songs should go to songQ
#  Background stuff should do background stuff.

class AudioManager:
	songQ 		= None
	backgrounds = list # list of bg files. obj for each

	def __init__(self, songQ_obj):
		log('AudioMngr', 'AudioManager created')
		# Register functions with scheduler
		# Probably just a function to be run every hour
		self.songQ = songQ_obj

		# Start the party
		self.prepSongQ( curHour() )
		self.songQ.loadNextSongQ()
		self.songQ.playNextSong()

		# Keep the party going
		scheduler.register_func_hourly_head( self.endOfHourUpdate )
		scheduler.register_func_hourly_tail( self.startOfHourUpdate )

	def endOfHourUpdate(self):
		# Called at `*:59`
		# Do cleanup or w/e for the end of the hour
		self.prepSongQ( nextHour() )

	def startOfHourUpdate(self):
		# Called at `*:00`
		# Change things up for the new hour
		self.songQ.loadNextSongQ()
		self.songQ.playNextSong()


	def prepSongQ(self, hour):
	# Prepare the next hours songQ ahead of time
		nextSongQ = list()
		hour = hour % 24 # Ensure Sane input
		ToD  = 'Day' if hour < 20 and hour > 7 else 'Night'

		srchDir = path.join( 'TimeSlots', ToD, 'Songs' )
		nextSongQ.extend( self.scanDir( srchDir ) )

		srchDir = path.join( 'TimeSlots', ToD, str(hour), 'Songs' )
		nextSongQ.extend( self.scanDir( srchDir ) )

		shuffle( nextSongQ )
		self.songQ.setNextSongQ( nextSongQ );

	def scanDir(self, folder):
		log('AudioMngr', 'Scanning directory ' + str(folder) )
		songList = list()
		try:
			for curDir, subDirs, files in walk( folder ):
				for curFile in files:
					audioFile = path.join( curDir, curFile )
					songList.append( audioFile )
		except Exception, e:
			log( 'AudioMngr',
			     'Error in scanning Directory ' + str(folder)
				  + ' : ' + e )
		return songList

