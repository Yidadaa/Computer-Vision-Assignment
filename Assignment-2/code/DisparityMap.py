import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

class DisparityMap:
    def __init__(self, numDisparities, blockSize):
        self.stereo = cv2.StereoSGBM_create(0, numDisparities, blockSize)

    def computeDsiparity(self, l, r):
        return self.stereo.compute(l, r)

    def saveToFile(self, filename, img):
        cv2.imwrite(filename, img)

    def setParams(self, numDisparities, blockSize):
        self.stereo = cv2.StereoSGBM_create(0, numDisparities, blockSize)

if __name__ == '__main__':
    instance = DisparityMap(16, 15)
    lImage = cv2.imread('./dataset/l.png', 0)
    rImage = cv2.imread('./dataset/r.png', 0)

    result_dir = './result'
    for f in os.listdir(result_dir):
        os.remove(result_dir + '/' + f)

    example_gray = 'result/example_gray.jpg'
    example_fakergb = 'result/example_fakergb.jpg'
    disparity = instance.computeDsiparity(lImage, rImage)
    instance.saveToFile(example_gray, disparity)
    gray = cv2.imread(example_gray)
    fakergb = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    instance.saveToFile(example_fakergb, fakergb)

    numDisparities = list(range(16, 16 * 6, 16))
    blockSize = list(range(7, 23, 4))
    for n in numDisparities:
        for b in blockSize:
            instance.setParams(n, b)
            disparity = instance.computeDsiparity(lImage, rImage)
            fname = 'result/%s_%s.png' % (n, b)
            instance.saveToFile(fname, disparity)
            disparity = cv2.imread(fname, 0)
            disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)
            instance.saveToFile(fname, disparity)