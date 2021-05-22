import cv2
import numpy as np
from time import sleep
import csv
from sample.settings import BASE_DIR
import datetime
from .models import KP
from .models import Battledetail

def countup(id,mode):
    kp = KP.objects.get(id=id)
    if mode == 0:
        kp.count = kp.count + 1
    else:
        kp.count2 = kp.count2 + 1
    kp.save()

def pokeinput():
    temp = []
    temp2 = []
    count = 0
    for i in range(400):
        img = cv2.imread(BASE_DIR+"/static/img/"+(str)(i+1) + ".png",0)
        if not img is None:
            temp.append(img)
            temp2.append(count)
            if i == 181:
                count += 1
            elif i == 326:
                count = 328
            elif i == 364:
                count = 367
            elif i == 371:
                count += 1
        for j in range(5):
            img = cv2.imread(BASE_DIR+"/static/img/"+(str)(i+1) + "_" + (str)(j+1) + ".png",0)
            if not img is None:
                temp.append(img)
                temp2.append(count)
                if i == 371:
                    count += 1
        if i != 371:
            count += 1
    return temp,temp2

def getpoke(impimg,key,mode):
    # データ読み込み
    try:
        with open(BASE_DIR+'/static/data/PokeDataSimple.csv', encoding="shift-jis", errors='ignore') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            f.close()
        # frame = cv2.imread("kensaku.png", 0)
        frame = impimg[194:894,328:428]
        frame2 = impimg[194:894,1228:1328]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        temp,temp2 = pokeinput()
        #類似度の設定(0~1)
        threshold = 0.9
        resultimg = impimg
        w, h = temp[0].shape[::-1]
        my = []
        enemy = []
        for i in range(len(temp)):
            #比較方法はcv2.TM_CCOEFF_NORMEDを選択
            result = cv2.matchTemplate(frame, temp[i], cv2.TM_CCOEFF_NORMED)
            result2 = cv2.matchTemplate(frame2, temp[i], cv2.TM_CCOEFF_NORMED)
            #検出結果から検出領域の位置を取得
            if (len(list(zip(*np.where(result >= threshold)))) > 0):
                loc = np.where(result >= threshold)
                #検出領域を四角で囲んで保存
                for top_left in zip(*loc[::-1]):
                    top_left = (top_left[0] + 328, top_left[1] + 194)
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                    cv2.rectangle(resultimg,top_left, bottom_right, (255, 0, 0), 2)
                    my.append(temp2[i])
                    print("自分",l[temp2[i]][2],top_left[1],top_left[0])
            if (len(list(zip(*np.where(result2 >= threshold)))) > 0):
                loc2 = np.where(result2 >= threshold)
                for top_left in zip(*loc2[::-1]):
                    top_left = (top_left[0] + 1228, top_left[1] + 194)
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                    cv2.rectangle(resultimg,top_left, bottom_right, (0, 255, 0), 2)
                    enemy.append(temp2[i])
                    if mode % 2 == 0:
                        countup(temp2[i],mode)
                    print("相手",l[temp2[i]][2],top_left[1],top_left[0])
        while (len(enemy) < 6):
            enemy.append(-1)
        while (len(my) < 6):
            my.append(-1)
        dt_now = datetime.datetime.now()
        cv2.imwrite(BASE_DIR+"/result/"+dt_now.strftime('%Y%m%d_%H%M%S')+".png", resultimg)
        line = dt_now.strftime('%Y%m%d_%H%M%S') + ","
        for i in range(6):
            if (enemy[i] > -1):
                line += l[enemy[i]][2] + ","
                print(l[enemy[i]][2])
            else:
                line += "--,"
                print("--")
        newdetail = Battledetail(key=key)
        newdetail.date = dt_now.strftime('%Y%m%d_%H%M%S')
        if mode < 2:
            newdetail.battletype = "single"
        else:
            newdetail.battletype = "double"
        if mode % 2 == 0:
            newdetail.memory = "yes"
        else:
            newdetail.memory = "no"
        if my[0] > -1:
            newdetail.mypoke1 = l[my[0]][2]
        if my[1] > -1:
            newdetail.mypoke2 = l[my[1]][2]
        if my[2] > -1:
            newdetail.mypoke3 = l[my[2]][2]
        if my[3] > -1:
            newdetail.mypoke4 = l[my[3]][2]
        if my[4] > -1:
            newdetail.mypoke5 = l[my[4]][2]
        if my[5] > -1:
            newdetail.mypoke6 = l[my[5]][2]
        if enemy[0] > -1:
            newdetail.poke1 = l[enemy[0]][2]
        if enemy[1] > -1:
            newdetail.poke2 = l[enemy[1]][2]
        if enemy[2] > -1:
            newdetail.poke3 = l[enemy[2]][2]
        if enemy[3] > -1:
            newdetail.poke4 = l[enemy[3]][2]
        if enemy[4] > -1:
            newdetail.poke5 = l[enemy[4]][2]
        if enemy[5] > -1:
            newdetail.poke6 = l[enemy[5]][2]
        newdetail.save()
        line = line.rstrip(",")
        line += "\n"
        with open(BASE_DIR+'/result/EnemyLog.csv', 'a', encoding="utf-8") as f2:
            f2.writelines(line)
            f2.close()
        return line
    except Exception as e:
        return str(e)
