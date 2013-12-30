#!/usr/bin/python
#  -*- coding: utf8
#
# Program to time exercises.
#
# A program to play sounds at defined intervals. Program is designed to help
# doing exercises that have a set duration for each repetition and break
# between repetitions. When started program waits for pre-set amount of
# seconds, then repeats the exercise + break cycle for desired number of times.
# At the start of each repetition program speaks the number of the repetition.
# At the end of each repetition a sound is played.
#
# For the program to work SOUND_DIR must contain .wav sound files for each
# number up to the desired number of repetitions. E.g. 1.wav, 2.wav, ...
# 

import sys
import argparse
import pygame
import wave
from time import sleep
from os import path

def play_sound(path):
	# Init the pygame mixer
	pygame.mixer.quit()
	if(path.endswith('.wav')):
		wave_fh = wave.open(path, 'rb')
		pygame.mixer.init(frequency=wave_fh.getframerate())
		wave_fh.close()
	else:
		pygame.mixer.init()
	# Load the sound file
	pygame.mixer.music.load(path)
	# Play the sound
	pygame.mixer.music.play()

def main():
	# Define command line options
	parser = argparse.ArgumentParser(description='Time some exercises')
	parser.add_argument('-p', '--prelude-time', dest='prelude_time', type=float,
					  default=3, 
					  help='Time to wait before starting the exercise set.')
	parser.add_argument('-d', '--duration', dest='duration', type=float,
					  default=5, help='Duration of one rep.')
	parser.add_argument('-s', '--sleep', dest='sleep', type=float,
					  default=3, help='Time to wait between repetitions.')
	parser.add_argument('-r', '--repetitions', dest='repetitions', type=int,
					  default=10, help='Number of repetitions.')
	parser.add_argument('--sound_dir', dest='sound_dir', default='~/Music/',
					   help='Directory containing the sounds')
	parser.add_argument('--sound_postfix', dest='sound_postfix', help='Postfix ' + \
					  'affixed to sound file names, when searching sounds.')
	parser.add_argument('--end_sound', dest='end_sound', default='end.wav',
					  help='Sound played at the end of a rep.')

	# Parse command line options
	opts = parser.parse_args()
	# Tilde expansion for user home directories
	sound_dir = path.expanduser(opts.sound_dir)
	# Add slash, if missing. Helps with path creation later.
	if not sound_dir.endswith('/'):
		sound_dir += '/'
	# If end sound path does not start with '/' prepend sound dir.
	if opts.end_sound.startswith('/'):
		end_sound = opts.end_sound
	else:
		end_sound = sound_dir + '/' + opts.end_sound
	# Try to figure out which files to use for repetition count sounds.
	if opts.sound_postfix is not None:
		sound_postfixes = [opts.sound_postfix]
	else:
		sound_postfixes = ['wav', 'ogg', 'oga', 'mp3']
	sound_postfix = None
	for postfix in sound_postfixes:
		if path.exists(sound_dir + '1.' + str(postfix)):
			sound_postfix = '.' + str(postfix)
			break
	if sound_postfix is None:
		print "Can't find sound files for repetition count. Most likely " + \
			  "sound files does not exist. Check that directory " + \
			  "specified by --sound_dir parameter contains properly " + \
			  "named files for all numbers smaller and equal to " + \
			  "repetition count. " + \
			  "E.g. 1.wav, 2.wav, ..., 12.wav, ..., 42.wav."
		sys.exit(0)

	# Sleep given time before starting the repetitions
	sleep(opts.prelude_time)

	# play start and end sounds 'repetitions' times 'interval' seconds apart
	# sleeping 'sleep' seconds between repeats.
	for repeat in range(1, opts.repetitions + 1):
		try:
			play_sound(sound_dir + str(repeat) + sound_postfix)
		except pygame.error as e:
			print "Can't play sound for repetition count. Most likely " + \
				  "sound file does not exist. Check that directory " + \
				  "specified by --sound_dir parameter contains properly " + \
				  "named sound files for all numbers smaller and equal to " + \
				  "repetition count. " + \
				  "E.g. 1.wav, 2.wav, ..., 12.wav, ..., 42.wav."
			print str(e)
			sys.exit(0)
		sleep(opts.duration)
		try:
			play_sound(end_sound)
		except pygame.error as e:
			print "Can't play end sound. Most likely sound file does not " + \
				  "exist. Check that --end_sound parameter specifies an " + \
				  "existing sound file."
			print str(e)
			sys.exit(0)
		sleep(opts.sleep)

if __name__ == "__main__":
	main()
