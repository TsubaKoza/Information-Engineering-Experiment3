#-*- coding: utf-8 -*-

import cv2
import math
import numpy as np

#動画入力（動画ファイル名は sample.MP4）
cap = cv2. VideoCapture('sample.MP4')

#フレーム番号 i
i=0
#何枚おきに静止画にするか
n=4
#何枚を静止画にするか
N=32
while i<n*N:
    #各フレーム取得
    ret, frame = cap.read()

    i+=1
    #フレーム画像のファイル名を決める
    filename = 'centroidframe'+ str(i) + '.jpg'
    if i%n == 0:
        # フレーム画像frameをfilename というファイル名で保存
        cv2. imwrite(filename, frame)
        print(i, filename)
    k = cv2. waitKey(1) & 0xFF
    if k == 27:
        break

cv2. destroyAllWindows()