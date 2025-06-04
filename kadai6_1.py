
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
    
    
    #HSVの範囲取得　板(黒)（色はカラーバネルなどを用いてHSV値を求めよう）
    lower1_value = np.array([0,0,40])
    upper1_value = np.array([256,256,50])
    
    #板のマスク画像の値を定める
    masked_image1 = cv2.inRange(hsv, lower1_value, upper1_value)

    #中央値フィルタ（ノイズを低減する）
    output_image1 = cv2.medianBlur(masked_image1, 9)

    #板のマスク画像から重心を計算
    moments_image1 = cv2.moments(output_image1)
    m00 = moments_image1['m00']
    centroid1_x,centroid1_y = None, None
    if m00 != 0:
        #x座標
        centroid1_x = int(moments_image1['m10']/m00)
        #y座標
        centroid1_y = int(moments_image1['m01']/m00)
        
    centroid_coordinate1 = (-1,-1)
    #重心が存在する場合
    if centroid1_x != None and centroid1_y != None:
        centroid_coordinate1 = (centroid1_x, centroid1_y)
        cv2.circle(output_image1,centroid_coordinate1, 4, (0,0,0),-1)

    #ブックエンド、板の端、糸の先端の三角形からθpを求める
    vector1_x = centroid1_x + 30
    vector1_y = 798

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
    cv2.imshow('centroid extracted',output_image1)
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break
   
cv2.destroyAllWindows()