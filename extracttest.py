#-*- coding: utf-8 -*-

import cv2
import math
import numpy as np

#������́i����t�@�C������ sample.MP4�j
cap = cv2. VideoCapture('sample.MP4')

#�t���[���ԍ� i
i=0
#���������ɐÎ~��ɂ��邩
n=4
#������Î~��ɂ��邩
N=32
while i<n*N:
    #�e�t���[���擾
    ret, frame = cap.read()

    i+=1
    #�t���[���摜�̃t�@�C���������߂�
    filename = 'centroidframe'+ str(i) + '.jpg'
    if i%n == 0:
        # �t���[���摜frame��filename �Ƃ����t�@�C�����ŕۑ�
        cv2. imwrite(filename, frame)
        print(i, filename)
    k = cv2. waitKey(1) & 0xFF
    if k == 27:
        break

cv2. destroyAllWindows()