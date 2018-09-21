# -*- coding: utf-8 -*-

import requests
import re
import sys
import random


def getViewstate(text):
    # 这里使用这样的正则表达式匹配__VIEWSTATE字段，使用Python requests应该这样匹配，其他浏览器可能不一样
    data = re.match(
        r'.*id\=\"\_\_VIEWSTATE\" value\=\"(.*)\" \/\>\r\n\r\n\<div class\=\"acountWrap\"\>', text, re.S)
    return data.group(1)


def getFee(text):
    # 匹配剩余电费
    data = re.match(
        r'.*\<span class\=\"number orange\"\>(\-*\d+\.\d\d)\<\/span\>', text, re.S)
    # 居然会有负数，坑死我了
    return data.group(1)


def getBuilding(text):
    # 此函数用于返回与楼栋对应的drceng的值
    mat = re.match(r'(\d\d)\d\d\d\d\d\d', text)
    building = int(mat.group(1))
    id = building+50
    return str(id)


def getFloor(text):
    # 此函数用于返回与楼层对应的dr_ceng的值
    mat = re.match(r'(\d\d)(\d\d)\d\d\d\d', text)
    building = int(mat.group(1))
    floor = int(mat.group(2))
    id = floor+(building-21)*19+213
    return str(id)


orgRoom = {21: 2647, 22: 3161}  # 每栋楼第一个房间的drfangjian值


def getRoom(text):
    # 此函数用于返回与房间对应的drfangjian的值
    mat = re.match(r'(\d\d)(\d\d)(\d\d)(\d\d)', text)
    building = int(mat.group(1))
    floor = int(mat.group(2))
    big_room = int(mat.group(3))
    small_room = int(mat.group(4))
    if big_room <= 2:
        id = (floor-1)*28+(big_room-1)*4+small_room-1+orgRoom[building]
    else:
        id = (floor-1)*28+(big_room-3)*5+small_room-1+8+orgRoom[building]
    return str(id)

# 模拟请求的过程
def SimuRequest(url, cookies, proxies, data):
    # 第一次请求
    response = requests.post(url, cookies=cookies, proxies=proxies, timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第二次请求
    data['drlouming'] = '1'
    response = requests.post(url, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第三次请求
    data['DropDownList1'] = '2'
    response = requests.post(url, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第四次请求
    data['drceng'] = getBuilding(sys.argv[1])
    response = requests.post(url, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第五次请求
    data['dr_ceng'] = getFloor(sys.argv[1])
    response = requests.post(url, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第六次请求
    data['drfangjian'] = getRoom(sys.argv[1])
    response = requests.post(url, cookies=cookies, data=data, proxies=proxies,timeout=2)
    # print(response.text)
    # print(data)

    return getFee(response.text)


character = 'qwertyuiopasdfghjklzxcvbnm'  # 用于生成随机字符串
randStr = ""
for i in range(0, 5):
    randStr += character[random.randint(0, 25)]  # 生成随机cookie

url_1 = 'http://222.192.89.21/sims3/default.aspx'
url_2 = 'http://222.192.89.21/sims3/buyRecord.aspx'  # emmm这个好像没什么卵用
# 随机cookie，防止多人同时访问引起异常
cookies = {'ASP.NET_SessionId': 'idd1fueg2bcpwokoybe'+randStr}
data = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': '', 'drlouming': '', 'DropDownList1': '',
        'drceng': '', 'dr_ceng': '', 'drfangjian': '', 'radio': 'buyR', 'ImageButton1.x': '45', 'ImageButton1.y': '4'}  # 需要POST的数据
proxies_1 = {'http': 'http://0.0.0.0:0'}  # 填写校内代理
proxies_2 = {'http': 'http://0.0.0.0:1'}  # 填写备用代理


# 下面模拟各次请求，并当一个代理不可用时，尝试备用代理。
try:
    print(SimuRequest(url_1, cookies, proxies_1, data))
except:
    try:
        print(SimuRequest(url_1, cookies, proxies_2, data))
    except:
        print("Error!")
