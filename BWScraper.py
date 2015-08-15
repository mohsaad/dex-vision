#
# Meraj Siddiqui
# 8/15/2015
# Gets Sprites of all 155 pokemon from Black/White and stores them
#

import requests
import os
import shutil
import time

class BWScraper:

	def __init__(self):
		self.url = 'http://www.serebii.net/pokedex-bw/'
		self.curr_entry = 1
		self.path = '/Users/biomedace001/Desktop/DexV/bw-sprites'
		
		
		# grab an individual sprite
	def grab_sprite(self, number):
		number = number + '.png' # add png to make sure link works
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
			time.sleep(5) # sleep to not overload server

		print "All {0} sprites grabbed!".format(str(num_sprites))





def main():
	bw = BWScraper()
	bw.grab_num_sprites(155)

if __name__ == '__main__':
	main()