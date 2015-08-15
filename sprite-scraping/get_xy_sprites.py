#!/usr/bin/env python2
# Mohammad Saad
# 8/15/2015
# Gets sprites of first 151 pokemon from the X/Y games and 
# stores them in the aformentioned folder.

import requests
import os
import shutil

class XYScraper:

	# set up some initial class variables
	def __init__(self):

		self.url = 'http://serebii.net/xy/pokemon/'
		self.curr_entry = 1
		self.path = '/home/saad/Documents/Github/PokeVision/xy-sprites' # set to your scraping directory

	# grab an individual sprite
	def grab_sprite(self, number):
		number = number + '.png' # add png to make sure link works
		link = self.url + number # make total link
		r = requests.get(link, stream = True)  # get the picture

		if r.status_code == 200:
			path = self.path + number
			try:
				with open(path, 'wb') as f:
					for chunk in r:
						f.write(chunk)
			except:
				print "Write failed"
				return False
		else:
			print "Scrape failed"
			print "Status code: {0}".format(str(r.status_code))
			return False

		print "Sprite #{0} grabbed.".format(number) 
		return True


	

def main():
	xy = XYScraper()
	xy.grab_sprite('001')

if __name__ == '__main__':
	main()
