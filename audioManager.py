#!/usr/bin/python

import scheduler
from background import Background
from threading import Thread
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
	nextSongQ	= []
	bgAudioList	= list # list of bg files. obj created for each

	def __init__(self, songQ_obj):
		log('AudioMngr', 'AudioManager created')
		# Register functions with scheduler
		# Probably just a function to be run every hour
		self.songQ = songQ_obj

		# Start the party
		self.prepAudio( curHour() )
		self.startOfHourUpdate()

		# Keep the party going
		scheduler.register_func_hourly_head( self.endOfHourUpdate )
		scheduler.register_func_hourly_tail( self.startOfHourUpdate )

	def endOfHourUpdate(self, *args):
		# Called at `*:59`
		# Do cleanup or w/e for the end of the hour
		self.prepAudio( nextHour() )
		for bg in self.bgAudioList:
			bg.terminate()

	def startOfHourUpdate(self, *args):
		# Called at `*:00`
		# Start new set of audio for the new hour
		self.songQ.loadNextSongQ(self.nextSongQ)
		self.songQ.playNextSong()
		i = 0
		# loop through bg files, replace each index with the thread
		# started to play that file
		for bg in self.bgAudioList:
			self.bgAudioList[i] = Background(bg)
			i += 1;
		# I'm sure there's a more 'pythonic' way of doing this..

	def prepAudio(self, hour ):
	# Prepare the next hours audio ahead of time

		nextSongQ = list()
		bgAudioList = list()
		hour = hour % 24 # Ensure Sane input
		ToD  = 'Day' if hour < 20 and hour > 7 else 'Night'
		hour = str(hour)

		srchDir = path.join( 'TimeSlots', ToD, 'Songs' )
		nextSongQ.extend( self.scanDir( srchDir ) )

		srchDir = path.join( 'TimeSlots', ToD, hour, 'Songs' )
		nextSongQ.extend( self.scanDir( srchDir ) )

		srchDir = path.join( 'TimeSlots', ToD, 'Background' )
		bgAudioList.extend( self.scanDir( srchDir ) )

		srchDir = path.join( 'TimeSlots', ToD, hour, 'Background' )
		bgAudioList.extend( self.scanDir( srchDir ) )

		shuffle( nextSongQ )
		self.nextSongQ = nextSongQ
		self.bgAudioList = bgAudioList;

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

