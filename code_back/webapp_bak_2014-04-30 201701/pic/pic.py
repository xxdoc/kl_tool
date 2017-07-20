#!/usr/bin/python

from scipy.cluster.vq import kmeans, vq
from numpy import array, reshape, zeros
from PIL import Image as image

vqclst = [2, 10, 100, 256]
te_img = image.open('wowfish+2.bmp')

if te_img.mode != 'RGB':
    te_img = te_img.convert("RGB")

temp_data = list(te_img.getdata())
width = te_img.size[0]
height = te_img.size[1]
channel = 3

data = reshape(temp_data, (height*width, channel))

for k in vqclst:
    print 'Generating vq-%d...' % k
    (centroids, distor) = kmeans(data, k)
    (code, distor) = vq(data, centroids)
    print 'distor: %.6f' % distor.sum()

    im_vq = centroids[code, :]

    temp_data = reshape(im_vq, (height*width, channel) )
    temp_data = list(temp_data)
    temp_data = map(list, temp_data)
    temp_data = map(tuple, temp_data)

    te_img.putdata(temp_data)

    te_img.save('result-%d.jpg' % k)