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

def getRoom(number, text):
    # 匹配房间号前面的option代号。这里我不想算号码了，机智一点直接匹配
    if number[2]=='1': # emmm，这里，10层以下他是不加0的
        toFind = number[0:2]+'\\-'+number[2:6]+'\\-'+number[7:]
    else:
        toFind = number[0:2]+'\\-'+number[3:6]+'\\-'+number[7:]
    data = re.match(
        r'.*\<option value\=\"(\d{8})\"\>'+toFind, text, re.S
    )

    return data.group(1)

# 模拟请求的过程
def SimuRequest(url, cookies, proxies, data):
    # 第一次请求
    response = requests.post(url_1, cookies=cookies, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第二次请求
    data['drlouming'] = '1'
    response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第三次请求
    data['DropDownList1'] = '7'
    response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第四次请求，drceng是 "02"+楼栋号
    data['drceng'] = "02"+sys.argv[1][0:2]
    response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第五次请求
    data['dr_ceng'] = data['drceng']+sys.argv[1][2:4]
    response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies,timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)

    # 第六次请求
    data['drfangjian'] = getRoom(sys.argv[1], response.text)
    response = requests.post(url_1, cookies=cookies, data=data, proxies=proxies,timeout=2)
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
proxies_2 = {'http': 'http://0.0.0.0:1'}  # 填写校内代理


# 下面模拟各次请求，并当一个代理不可用时，尝试备用代理。
try:
    print(SimuRequest(url_1, cookies, proxies_1, data))
except:
    try:
        print(SimuRequest(url_1, cookies, proxies_2, data))
    except:
        print("Error!")
