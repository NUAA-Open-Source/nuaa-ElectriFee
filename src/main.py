# -*- coding: utf-8 -*-

import requests
import re
import sys
import random


character='qwertyuiopasdfghjklzxcvbnm' # 用于生成随机字符串

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


def getFloor(text):
    # 此函数用于返回与楼层对应的dr_ceng的值
    mat = re.match(r'\d\d(\d\d)\d\d\d\d', text)
    floor = mat.group(1)
    id = int(floor)+213
    return str(id)


def getRoom(text):
    # 此函数用于返回与楼层对应的drfangjian的值
    mat = re.match(r'\d\d(\d\d)(\d\d)(\d\d)', text)
    floor = mat.group(1)
    big_room = mat.group(2)
    small_room = mat.group(3)
    if int(big_room) <= 2:
        id = (int(floor)-1)*28+(int(big_room)-1)*4+int(small_room)-1+2647
    else:
        id = (int(floor)-1)*28+(int(big_room)-3)*5+int(small_room)-1+2647+8
    return str(id)

randStr = ""
for i in range(0,5):
    randStr += character[random.randint(0,25)] # 生成随机cookie

url_1 = 'http://222.192.89.21/sims3/default.aspx'
url_2 = 'http://222.192.89.21/sims3/buyRecord.aspx'  # emmm这个好像没什么卵用
cookies = {'ASP.NET_SessionId': 'idd1fueg2bcpwokoybe'+randStr}  # 可自行替换
data = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': '', 'drlouming': '', 'DropDownList1': '',
        'drceng': '', 'dr_ceng': '', 'drfangjian': '', 'radio': 'buyR', 'ImageButton1.x': '45', 'ImageButton1.y': '4'}  # 需要POST的数据
proxies = {'http': 'http://frp.vvzero.com:21402/'}  # 自己设的校内代理


# 下面模拟各次请求，以将军路校区怡园21栋空调用电为例。

# 第一次请求
response = requests.post(url_1, cookies=cookies, proxies=proxies)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第二次请求
data['drlouming'] = '1'
response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第三次请求
data['DropDownList1'] = '2'
response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第四次请求
data['drceng'] = '71'
response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第五次请求
data['dr_ceng'] = getFloor(sys.argv[1])
response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第六次请求
data['drfangjian'] = getRoom(sys.argv[1])
response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies)
# print(response.text)
# print(data)

# 打印电费
print(getFee(response.text))
