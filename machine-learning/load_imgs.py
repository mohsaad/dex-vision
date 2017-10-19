#!/usr/bin/env python
# Mohammad Saad
# 8/27/2017
# load_imgs.py
# Loads images into numpy arrays

import numpy as np
import os
import cv2

def load_pokemon(directory):
    files = sorted(os.listdir(directory))

    pokemon = []
    for i in range(0, len(files)):
        img = (cv2.imread(directory + "/" + files[i]))
        resized_img = cv2.resize(img, (120, 120))
        pokemon.append(resized_img)
        
    return pokemon




if __name__ == '__main__':
    load_pokemon('emerald/')
