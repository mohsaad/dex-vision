#!/home/saad/envs/mxnet/bin python
import mxnet as mx
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
# define a simple data batch
from collections import namedtuple
Batch = namedtuple('Batch', ['data'])

# path='http://data.mxnet.io/models/imagenet-11k/'
# [mx.test_utils.download(path+'resnet-152/resnet-152-symbol.json'),
#  mx.test_utils.download(path+'resnet-152/resnet-152-0000.params'),
#  mx.test_utils.download(path+'synset.txt')]

 # vgg-net
# path='http://data.mxnet.io/models/imagenet/'
# [mx.test_utils.download(path+'vgg/vgg19-symbol.json', dirname = 'vgg/'),
#   mx.test_utils.download(path+'vgg/vgg19-0000.params', dirname = 'vgg/'),
#   mx.test_utils.download(path+'synset.txt', dirname = 'vgg/')]

# resnet-200
# path='http://data.mxnet.io/models/imagenet/'
# [mx.test_utils.download(path+'resnet/200-layers/resnet-200-symbol.json', dirname = 'resnet-200/'),
#   mx.test_utils.download(path+'resnet/200-layers/resnet-200-0000.params', dirname = 'resnet-200/'),
#   mx.test_utils.download(path+'synset.txt', dirname = 'resnet-200/')]


sym, arg_params, aux_params = mx.model.load_checkpoint('inception-bn/Inception-BN', 0)
mod = mx.mod.Module(symbol = sym, context = mx.gpu(), label_names = None)
mod.bind(for_training=False, data_shapes=[('data', (1,3,224,224))],
            label_shapes=mod._label_shapes)

mod.set_params(arg_params, aux_params, allow_missing=True)
with open('resnet-200/synset.txt', 'r') as f:
    labels = [l.rstrip() for l in f]

def get_image(url, show=False):
    # download and show the image
    fname = mx.test_utils.download(url)
    img = cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB)
    if img is None:
         return None
    if show:
         plt.imshow(img)
         plt.axis('off')
    # convert into format (batch, RGB, width, height)
    img = cv2.resize(img, (224, 224))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img

def get_pokemon_image(filename):
    img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
    if img is None:
        return None

    img = cv2.resize(img, (224, 224))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img


def predict(img, name, f):
    #img = get_image(url, show=True)

    mod.forward(Batch([mx.nd.array(img)]))
    prob = mod.get_outputs()[0].asnumpy()
    # print the top-5
    prob = np.squeeze(prob)
    a = np.argsort(prob)[::-1]

    print(name)
    print('---------------------------------')
    for i in a[0:5]:
        print('probability=%f, class=%s' %(prob[i], labels[i]))
        f.write('%s,%f,%s\n' % (name, prob[i], labels[i]))
    print('---------------------------------')


def classify_pokemon(directory, outfile):
    files = sorted(os.listdir(directory))
    results = []
    f = open(outfile, 'w')
    for i in range(0, len(files)):
        img = get_pokemon_image(directory + files[i])
        predict(img, files[i].split('.')[0], f)

    f.close()



def extract_features():
    all_layers = sym.get_internals()
    print(all_layers.list_outputs()[-10:])
    fe_sym = all_layers['flatten0_output']
    fe_mod = mx.mod.Module(symbol=fe_sym, context=mx.gpu(), label_names=None)
    fe_mod.bind(for_training=False, data_shapes=[('data', (1,3,224,224))])
    fe_mod.set_params(arg_params, aux_params)

    img = get_image('http://writm.com/wp-content/uploads/2016/08/Cat-hd-wallpapers.jpg')
    fe_mod.forward(Batch([mx.nd.array(img)]))
    features = fe_mod.get_outputs()[0].asnumpy()
    print(features.shape)
    assert features.shape == (1, 2048)

if __name__ == '__main__':
    classify_pokemon('../../sunmoon/', 'inception_sunmoon_results.txt')
