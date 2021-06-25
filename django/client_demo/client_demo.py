# -*- coding: utf-8 -*- 
import cv2, requests

def cap():
    while True:
        num = input("モードを選択してください\nどのモードを選んでも個人データには集計されます\nランクマッチ・マスターランク以外は非集計を選んでください\nシングルバトル、全体データに集計(通常)…0\nシングルバトル、全体データに非集計………1\nダブルバトル、全体データに集計……………2\nダブルバトル、全体データに非集計…………3\n数字を入力してください(Enterを押すと0になります)...")
        if num == '':
            num = '0'
        if len(num) > 1 or num < '0' or num > '3':
            print("有効な数字を入力してください")
        else:
            break
    temp = cv2.imread("templates/temp.png", 0)
    beforesend = False
    url = 'https://app.roishi.com/pokeapp/upload' + num
    frame = cv2.imread("test.png")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 比較方法:cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(gray,temp, cv2.TM_CCOEFF_NORMED)
    # 判別閾値:0.85
    if result[0][0] > 0.85:
        cv2.imwrite("img.png",frame)
        files = {'image': open("img.png", 'rb'),'key': open("key.txt",'rb'),}
        print("detected")
        res = requests.post(url, files=files)
        print(res.text)

cap()
