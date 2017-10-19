#!/usr/bin/env python
# Mohammad Saad
# 8/27/2017
# nn.py
# Nearest Neighbor for Pokemon

from load_imgs import load_pokemon
import numpy as np
import sys
from sklearn.decomposition import PCA

from numpy import array, dot, mean, std, empty, argsort
from numpy.linalg import eigh, solve
from numpy.random import randn
from matplotlib.pyplot import subplots, show

num_classes = 150

# We wil do one-class nearest neighbor as a baseline.
def l1_nearest(base, target):
    classes = np.zeros(num_classes)

    test_classes = np.zeros(num_classes)
    for i in range(0, num_classes):
        for j in range(0, num_classes):
            test_classes[j] = np.sum(np.abs(target[i] - base[j]))

        classes[i] = np.argmin(test_classes)

    return classes

def l2_nearest(base, target):
    classes = np.zeros(num_classes)

    test_classes = np.zeros(num_classes)
    for i in range(0, num_classes):
        for j in range(0, num_classes):
            test_classes[j] = np.sum(np.power(np.subtract(base[j], target[i]), 2))

        classes[i] = np.argmin(test_classes)

    return classes

def cov(X):
    """
    Covariance matrix
    note: specifically for mean-centered data
    note: numpy's `cov` uses N-1 as normalization
    """
    return dot(X.T, X) / X.shape[0]
    # N = data.shape[1]
    # C = empty((N, N))
    # for j in range(N):
    #   C[j, j] = mean(data[:, j] * data[:, j])
    #   for k in range(j + 1, N):
    #       C[j, k] = C[k, j] = mean(data[:, j] * data[:, k])
    # return C

def pca(data, pc_count = None):
    """
    Principal component analysis using eigenvalues
    note: this mean-centers and auto-scales the data (in-place)
    """
    data -= mean(data, 0)
    data /= std(data, 0)
    C = cov(data)
    E, V = eigh(C)
    key = argsort(E)[::-1][:pc_count]
    E, V = E[key], V[:, key]
    U = dot(data, V)  # used to be dot(V.T, data.T).T
    return U, E, V

def vectorize(img):
    cur_shape = img.shape
    resized_shape = 1
    for i in range(0, len(cur_shape)):
        resized_shape *= cur_shape[i]

    return np.reshape(img, (resized_shape, 1))

base_imgs = load_pokemon('sunmoon/')
target_imgs = load_pokemon('xy/')

for i in range(0, num_classes):
    base_imgs[i] = pca(vectorize(base_imgs[i]).astype(np.float), 12)
    target_imgs[i] = pca(vectorize(target_imgs[i]).astype(np.float), 12)

results = l2_nearest(base_imgs, target_imgs)
acc_vec = np.zeros(num_classes)
for i in range(0, num_classes):
    if(results[i] == i):
        acc_vec[i] = 1

print("Classification accuracy: {0}%" .format(np.sum(acc_vec) / num_classes))
