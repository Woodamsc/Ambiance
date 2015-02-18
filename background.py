#!/usr/bin/python
from time import sleep
from os import path
from sys import exit
from subprocess import call, check_output, Popen
from threading import Thread
from log import log
from time_Ambiance import *
# Purpose/Function:
#	load audio files to be played and looped as background noise
#
# Notes:
# 	This class assumes all paths are full qualified
# 	and doesn't do much defensive programming against the otherwise
#

class Background:
	path			 = None
	title 		 = None
	playTime 	 = None
	bg_thread	 = None

	def __init__(self, songPath):
		self.path 		= path.abspath(songPath)
		self.title 		= str(path.basename( path.normpath(songPath) ))
		self.playTime 	= float( 
							  check_output(['soxi', '-D', songPath]).strip()
							  		 )
		self.bg_thread = Thread( target=self.play )
		self.bg_thread.start()

	def play(self, *args):
		log('Background', 'Playing ' + self.title)
		while( True ):
			Popen(['play', '-q', self.path])
			sleep(self.playTime)

	def terminate(self):
		self.bg_thread.exit(0)

	@property
	def playTime(self):
		return self.playTime

