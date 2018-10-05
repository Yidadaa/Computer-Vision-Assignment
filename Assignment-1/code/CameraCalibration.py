import cv2
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

def filter_word(string, words):
    '''
    Return True if string contains the word from array words.
    '''
    for word in words:
        if word in string:
            return True
    return False

root = __file__[0:__file__.rfind(os.sep)]

# 首先找到棋盘格角点
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
w, h = 9, 6 # 棋盘大小

points = np.zeros((w * h, 3), np.float32)
points[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)

object_points = [] # 世界坐标系的三维点
img_points = [] # 平面中的二维点

images = glob.glob(root + '/images/*')

for filename in images:
    if filter_word(filename, ['with_corners']):
        continue
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 搜索棋盘格点
    ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
    if ret is True:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        object_points.append(points)
        img_points.append(corners)
        # 显示角点
        cv2.drawChessboardCorners(image, (w, h), corners, ret)
        new_fileaname = filename.replace('.', '_') + '_with_corners.jpg'
        cv2.imwrite(new_fileaname, image)

# 开始相机标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, img_points, gray.shape[::-1], None, None)

for filename in glob.glob(root + '/test/*'):
    if filter_word(filename, ['undistorted']):
        continue
    # 去除畸变
    test_img = cv2.imread(filename)
    height, width = test_img.shape[:2]
    result = cv2.undistort(test_img, mtx, dist, None, mtx)
    cv2.imwrite(filename.replace('.', '_') + '_undistorted.jpg', result)

# 反投影误差
total_error = 0
errors = []
N = len(object_points)
for i in range(N):
    img_points2, _ = cv2.projectPoints(object_points[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
    total_error += error
    errors.append(error)
mean_error = total_error / N

print('Mean error: %f' % mean_error)

# 绘制图表
plt.figure(figsize=(5, 3))
plt.bar(range(N), errors, width=0.4, color='black')
plt.savefig(root.replace('code', '') + 'doc/errors.pdf')