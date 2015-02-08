#!/usr/bin/python
from os import path
from sys import exit
from subprocess import call, checkoutput
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
	Title 		= None
	playTime 	= None
	Path			= None

	def __init__(self, songPath):
		self.path 		= songPath
		self.title 		= str(path.basename( path.normpath(songPath) ))
		self.playTime 	= float( 
							  check_output(['Soxi', '-D', songPath]).strip()
							  		 )
		self.play();

	def play():
		print(self.title + ' says hello!')

	def stop_and_cancel():
		exit(0)

	@property
	def playTime(self):
		return self.playTime

