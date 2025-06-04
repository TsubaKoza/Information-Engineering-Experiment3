
#-*- coding: utf-8 -*-

import cv2
import math
import numpy as np
from matplotlib import pyplot

#動画入力
cap = cv2.VideoCapture('4622045_kadai6.MP4')

i=1
while(1):
    #各フレーム取得
    ret, frame = cap.read()
    #終了判定
    if ret == False:
        break
    height = frame.shape[0]
    width = frame.shape[1]

    #BGRをHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #HSVの範囲取得　右のメトロノーム(青)（色はカラーバネルなどを用いてHSV値を求めよう）
    lower2_value = np.array([90,150,0])
    upper2_value = np.array([150,255,120])
    
    #右のメトロノームの針の固定点の座標
    bar1_X = 1207
    bar1_y = 185
    
    #右のメトロノームのマスク画像の値を定める
    masked_image2 = cv2.inRange(hsv, lower2_value, upper2_value)
    
    #中央値フィルタ（ノイズを低減する）
    output_image2 = cv2.medianBlur(masked_image2, 9)

    #マスク画像から重心を計算
    moments_image2 = cv2.moments(output_image2)
    m00 = moments_image2['m00']
    centroid2_x,centroid2_y = None, None
    if m00 != 0:
        #x座標
        centroid2_x = int(moments_image2['m10']/m00)
        #y座標
        centroid2_y = int(moments_image2['m01']/m00)
        
    centroid_coordinate2 = (-1,-1)
    #重心が存在する場合
    if centroid2_x != None and centroid2_y != None:
        centroid_coordinate2 = (centroid2_x, centroid2_y)
        cv2.circle(output_image2,centroid_coordinate2, 4, (0,0,0),-1)

    vector1_x = centroid2_x - bar1_X
    vector1_y = height - bar1_y - centroid2_y

    cosine_value = vector1_y /math.sqrt((vector1_x * vector1_x)+(vector1_y * vector1_y))
    theta = math.acos(cosine_value)

    if vector1_x<0:
        degree = -(math.degrees(theta))
    if vector1_x >=0:
        degree = math.degrees(theta)

    print(degree)
    
    if i == 1800:
        break
    i+=1

    #フレーム画像（フレームごとに更新）を出力（上書き）
    cv2.imwrite('centroidframe.jpg',frame)
    cv2.imshow('centroid extracted',output_image2)
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break

cv2.destroyAllWindows()