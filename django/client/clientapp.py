# -*- coding: utf-8 -*- 
import cv2
import numpy as np
from time import sleep
import requests
from PIL import Image

def camera_check():
    print('Switchの画面を探しています...')
    # カメラ番号を9～0まで変えて、switchの画面を表示しているカメラを探す
    for camera_number in range(10,0,-1):
        capture = cv2.VideoCapture(camera_number)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        temp = cv2.imread("templates/tempb.png", 0)
        temp2 = cv2.imread("templates/tempb2.png", 0)
        ret, frame = capture.read()
        if ret is True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 比較方法:cv2.TM_CCOEFF_NORMED
            result = cv2.matchTemplate(gray,temp, cv2.TM_CCOEFF_NORMED)
            result2 = cv2.matchTemplate(gray,temp2, cv2.TM_CCOEFF_NORMED)
            # 判別閾値:0.85
            if result[0][0] > 0.85 or result2[0][0] > 0.85:
                print("見つかりました!")
                return camera_number
    print("見つかりませんでした")
    return -1

def cap():
    while True:
        num = input("モードを選択してください\nどのモードを選んでも個人データには集計されます\nランクマッチ・マスターランク以外は非集計を選んでください\nシングルバトル、全体データに集計(通常)…0\nシングルバトル、全体データに非集計………1\nダブルバトル、全体データに集計……………2\nダブルバトル、全体データに非集計…………3\n数字を入力してください(Enterを押すと0になります)...")
        if num == '':
            num = '0'
        if len(num) > 1 or num < '0' or num > '3':
            print("有効な数字を入力してください")
        else:
            break
    cameranum = camera_check()
    if cameranum < 0:
        return
    capture = cv2.VideoCapture(cameranum)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    temp = cv2.imread("templates/temp.png", 0)
    beforesend = False
    url = 'https://poke-db.com/upload' + num
    while(True):
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 比較方法:cv2.TM_CCOEFF_NORMED
        result = cv2.matchTemplate(gray,temp, cv2.TM_CCOEFF_NORMED)
        # 判別閾値:0.85
        if result[0][0] > 0.85 and not beforesend:
            # 一度送ってからは90秒開かないと送信不可
            cv2.imwrite("img.png",frame)
            files = {'image': open("img.png", 'rb'),'key': open("key.txt",'rb'),}
            print("detected")
            res = requests.post(url, files=files)
            print(res.text)
            beforesend = True
            sleep(90)
        else:
            # キャプチャ間隔:1秒
            beforesend = False
            sleep(1)

cap()
