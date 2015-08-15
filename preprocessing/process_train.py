#!/usr/bin/env python2
# Mohammad Saad
# 8/15/2015
# A preprocessing script to turn each training sprite into
# a feature matrix.

import numpy as np
import cv2

class Preprocessor:

	def __init__(self, path_to_training_data, path_to_output):
		self.input = path_to_training_data
		self.output = path_to_output

	def readImage(self, numstr):
		# just read in our image
		img = cv2.imread(self.input + numstr + '.png')
		return img

	def turn_into_vector(self, img):
		# standardize image into 120x120 image (or 80x80, or 64x64... just a square image)
		# uses height, may need to do special handling (for all sprites I noticed somevalue x 120)
		empt_sprite = np.zeros([len(img), len(img), 3], dtype= 'uint8')
		
		# copies sprite, cuts off any bad length
		for i in range(0, len(empt_sprite)):
			for j in range(0, len(empt_sprite[0])):
				empt_sprite[i][j] = img[i][j]

		

def main():
	p = Preprocessor('/home/saad/Documents/Github/PokeVision/xy-sprites/', '/home/saad/Documents/Github/PokeVision/preprocessing/')
	a = p.readImage('006')
	p.turn_into_vector(a)





if __name__ == '__main__':
	main()

