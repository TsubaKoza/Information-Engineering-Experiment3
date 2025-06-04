#-*- coding: utf-8 -*-

import cv2
import math
import numpy as np

#動画入力
cap = cv2.VideoCapture('SAMPLE.MP4')

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

    #HSVの範囲取得（色はカラーバネルなどを用いてHSV値を求めよう）
    lower_value = np.array([30,64,0])
    upper_value = np.array([90,255,255])
    #針の固定点の座標
    bar_X = 948
    bar_y = height-946

    #マスク画像の値を定める
    masked_image = cv2.inRange(hsv, lower_value, upper_value)

    #中央値フィルタ（ノイズを低減する）
    output_image = cv2.medianBlur(masked_image, 9)

    #マスク画像から重心を計算
    moments_image = cv2.moments(output_image)
    m00 = moments_image['m00']
    centroid_x,centroid_y = None, None
    if m00 != 0:
        #x座標
        centroid_x = int(moments_image['m10']/m00)
        #y座標
        centroid_y = int(moments_image['m01']/m00)
        
    centroid_coordinate = (-1,-1)
    #重心が存在する場合
    if centroid_x != None and centroid_y != None:
        centroid_coordinate = (centroid_x,centroid_y)
        cv2.circle(output_image,centroid_coordinate, 4, (0,0,0),-1)

    vector_x = centroid_x - bar_X
    vector_y = height - bar_y - centroid_y

    cosine_value = vector_y /math.sqrt((vector_x * vector_x)+(vector_y * vector_y))
    theta = math.acos(cosine_value)

    if vector_x<0:
        degree = -(math.degrees(theta))
    if vector_x >=0:
        degree = math.degrees(theta)

    print(i,degree)

    i+=1

    #フレーム画像（フレームごとに更新）を出力（上書き）
    cv2.imwrite('centroidframe.jpg',frame)
    cv2.imshow('centroid extracted',output_image)
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
