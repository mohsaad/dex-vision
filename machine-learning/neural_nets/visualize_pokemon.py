import matplotlib
import matplotlib.pyplot as plt
import os
import cv2

directory = '../../sunmoon/'
files = sorted(os.listdir(directory))
result_file = open('resnet-200/resnet200_sunmoon_results.txt', 'r')

img_names = []
img_class = []
img_prob = []

for i in range(0, len(files)):
    testline = result_file.readline()
    line = testline.split('\n')[0].split(',')
    img_prob.append(line[1])
    img_class.append(" ".join(line[2].split(" ")[1:]))

    for j in range(0, 4):
        result_file.readline()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 5}

matplotlib.rc('font', **font)

f, axarr = plt.subplots(5,5)
plt.subplots_adjust(bottom=0.1)
count = 126
for i in range(0,5):
    for j in range(0,5):
        img = cv2.cvtColor(cv2.imread(directory+files[count]), cv2.COLOR_BGR2RGB)
        axarr[i,j].imshow(img)
        axarr[i,j].set_title('\n%s' % img_class[count])
        axarr[i,j].axis('off')

        count += 1

plt.show()
#plt.savefig('test.png', format = 'png')
