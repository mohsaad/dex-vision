#!/usr/bin/env python2
# Mohammad Saad
# 8/15/2015
# Gets sprites of first 151 pokemon from the X/Y games and
# stores them in the aformentioned folder.

import requests
import os
import shutil
import time
import argparse

class XYScraper:

	# set up some initial class variables
	def __init__(self, directory, generation="xy"):

		self.url = 'http://serebii.net/{0}/pokemon/'.format(generation)
		self.curr_entry = 1
		self.path = directory # set to your scraping directory

	# grab an individual sprite
	def grab_sprite(self, number):
		number = number + '.gif' # add png to make sure link works
		link = self.url + number # make total link
		r = requests.get(link, stream = True)  # get the picture

		if r.status_code == 200:
			path = self.path + number
			try:
				# taken from http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
				with open(path, 'wb') as f:
					for chunk in r:
						f.write(chunk)
			except:
				print "Write failed"
				return False
		else:
			# just a bunch of error handling conditions
			print "Scrape failed"
			print "Status code: {0}".format(str(r.status_code))
			return False

		# print which sprite we grabbed
		print "Sprite #{0} grabbed.".format(number)
		return True

	# now loop over and grab a bunch of them
	def grab_num_sprites(self, num_sprites):
		while self.curr_entry <= num_sprites:
			num = str(self.curr_entry)
			# make sure each number is at least 3 digits
			# if not, append zeros to the front
			while len(num) < 3:
				num = '0' + num # append zeros to the front


			res = self.grab_sprite(num)
			if not res:
				break # break out of loop if something happens (too many requests, etc.)

			self.curr_entry += 1 # iterate
			time.sleep(1) # sleep to not overload server

		print "All {0} sprites grabbed!".format(str(num_sprites))





def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("directory", help = "directory to store sprites")
	parser.add_argument("generation", help = "generation of sprite")
	parser.add_argument("-n", "--number", help = "number of sprites to grab")

	args = parser.parse_args()
	xy = XYScraper(args.directory, args.generation)
	xy.grab_num_sprites(151)

if __name__ == '__main__':
	main()
