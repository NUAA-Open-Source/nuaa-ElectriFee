# -*- coding: utf-8 -*-
import requests
import re
import sys
import random
from bs4 import BeautifulSoup
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import pickle
import json
import yaml

RoomMapping = dict()


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def getViewstate(text):
    bs = BeautifulSoup(text, "html.parser")
    return bs.find("input", {"id": "__VIEWSTATE"}).attrs['value']


def getFee(text):
    bs = BeautifulSoup(text, "html.parser")
    return bs.find("span", {"class": "number"}).text


def getDescriptiveText(text):
    bs = BeautifulSoup(text, "html.parser")
    return bs.find("h6").text


def recursiveFill(num, max, DictData, data):
    # print(DictData)
    if num < max:
        if data[num].isdigit():
            data[num] = int(data[num])
        if data[num] not in DictData:
            DictData[data[num]] = {}
        res = recursiveFill(num + 1, max, DictData[data[num]], data)
    elif num == max:
        DictData[data[num][0]] = data[num][1]
    return DictData


def mergeData(data, value):
    data.append(value)
    global RoomMapping
    recursiveFill(0, len(data) - 1, RoomMapping, data)


'''
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
'''


def CampusRequest(text, res, url, sess, proxies, data):
    soup = BeautifulSoup(res, "html.parser")
    options = [[str(x.text), str(x.attrs['value'])] for x in soup.find(id="drlouming").find_all('option')]
    for option in options:
        if not option[1]:
            continue
        NewData = dict(data)
        NewData['drlouming'] = option[1]
        NewText = text + option[0].strip() + ' - '
        print('[+] Requesting ' + NewText)
        try:
            response = sess.post(url, data=NewData, proxies=proxies, timeout=2)
        except:
            print('[!] ' + NewText + ' failed to response!')
            continue
        # response = requests.post(url, cookies=cookies, data=NewData, proxies=proxies, timeout=2)
        NewData['__VIEWSTATE'] = getViewstate(response.text)
        RegionRequest(NewText, response.text, url, sess, proxies, NewData)


def RegionRequest(text, res, url, sess, proxies, data):
    soup = BeautifulSoup(res, "html.parser")
    options = [[str(x.text), str(x.attrs['value'])] for x in soup.find(id="DropDownList1").find_all('option')]
    for option in options:
        if not option[1]:
            continue
        NewData = dict(data)
        NewData['DropDownList1'] = option[1]
        NewText = text + option[0].strip() + ' - '
        print('[+] Requesting ' + NewText)
        try:
            response = sess.post(url, data=NewData, proxies=proxies, timeout=2)
        except Exception as x:
            print('[!] ' + NewText + ' failed to response!')
            continue
        # response = requests.post(url, cookies=cookies, data=NewData, proxies=proxies, timeout=2)
        NewData['__VIEWSTATE'] = getViewstate(response.text)
        BuildingRequest(NewText, response.text, url, sess, proxies, NewData)


def BuildingRequest(text, res, url, sess, proxies, data):
    soup = BeautifulSoup(res, "html.parser")
    options = [[str(x.text), str(x.attrs['value'])] for x in soup.find(id="drceng").find_all('option')]
    for option in options:
        if not option[1]:
            continue
        NewData = dict(data)
        NewData['drceng'] = option[1]
        NewText = text + option[0].strip() + ' - '
        print('[+] Requesting ' + NewText)
        try:
            response = sess.post(url, data=NewData, proxies=proxies, timeout=2)
        except Exception as x:
            print('[!] ' + NewText + ' failed to response!')
            continue
        # response = requests.post(url, cookies=cookies, data=NewData, proxies=proxies, timeout=2)
        NewData['__VIEWSTATE'] = getViewstate(response.text)
        FloorRequest(NewText, response.text, url, sess, proxies, NewData)


def FloorRequest(text, res, url, sess, proxies, data):
    soup = BeautifulSoup(res, "html.parser")
    options = [[str(x.text), str(x.attrs['value'])] for x in soup.find(id="dr_ceng").find_all('option')]
    for option in options:
        if not option[1]:
            continue
        NewData = dict(data)
        NewData['dr_ceng'] = option[1]
        NewText = text + option[0].strip() + ' - '
        print('[+] Requesting ' + NewText)
        try:
            response = sess.post(url, data=NewData, proxies=proxies, timeout=2)
        except:
            print('[!] ' + NewText + ' failed to response!')
            continue
        # response = requests.post(url, cookies=cookies, data=NewData, proxies=proxies, timeout=2)
        NewData['__VIEWSTATE'] = getViewstate(response.text)
        RoomRequest(NewText, response.text, url, sess, proxies, NewData, option[0].strip())


def RoomRequest(text, res, url, sess, proxies, data, extra):
    soup = BeautifulSoup(res, "html.parser")
    options = [[str(x.text), str(x.attrs['value'])] for x in soup.find(id="drfangjian").find_all('option')]
    for option in options:
        if not option[1]:
            continue
        NewData = dict(data)
        NewData['drfangjian'] = option[1]
        NewText = text + option[0].strip() + ' - '
        NewData.pop('__EVENTTARGET', '')
        NewData.pop('__EVENTARGUMENT', '')
        NewData.pop('__LASTFOCUS', '')
        NewData.pop('radio', '')
        NewData.pop('ImageButton1.x', '')
        NewData.pop('ImageButton1.y', '')
        NewData.pop('__VIEWSTATE', '')
        CampusNo = NewData['drlouming']
        RoomMergedId = re.findall('\d+', option[0].strip())
        RoomMergedId.insert(0, CampusNo)
        mergeData(RoomMergedId, (extra + '-' + option[0].strip(), NewData))
        print('[*] ' + NewText + ' -> ' + str(NewData) + '\n')
        # ProcessResult(NewText, response.text, NewData)


def ProcessResult(text, res, data):
    data.pop('__EVENTTARGET', '')
    data.pop('__EVENTARGUMENT', '')
    data.pop('__LASTFOCUS', '')
    data.pop('radio', '')
    data.pop('ImageButton1.x', '')
    data.pop('ImageButton1.y', '')
    data.pop('__VIEWSTATE', '')
    print('[*] ' + text + ' -> ' + str(data))
    print(getDescriptiveText(res))

# 模拟请求的过程
def SimuRequest(url, cookies, proxies, data):
    # 第一次请求
    # response = requests.post(url, cookies=cookies, proxies=proxies, timeout=2)
    s = requests_retry_session(retries=10)
    response = s.post(url, proxies=proxies, timeout=2)
    data['__VIEWSTATE'] = getViewstate(response.text)
    CampusRequest('', response.text, url, s, proxies, data)
    '''
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
    '''


character = 'qwertyuiopasdfghjklzxcvbnm'  # 用于生成随机字符串
randStr = ""
for i in range(0, 5):
    randStr += character[random.randint(0, 25)]  # 生成随机cookie

url_1 = 'http://222.192.89.21/sims3/default.aspx'
url_2 = 'http://222.192.89.21/sims3/buyRecord.aspx'  # emmm这个好像没什么卵用
# 随机cookie，防止多人同时访问引起异常
cookies = {'ASP.NET_SessionId': 'idd1fueg2bcpwokoybe' + randStr}
data = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': '', 'drlouming': '',
        'DropDownList1': '',
        'drceng': '', 'dr_ceng': '', 'drfangjian': '', 'radio': 'buyR', 'ImageButton1.x': '45',
        'ImageButton1.y': '4'}  # 需要POST的数据
proxies_1 = None

# 下面模拟各次请求，并当一个代理不可用时，尝试备用代理。

SimuRequest(url_1, cookies, proxies_1, data)
with open('file.txt', 'wb') as file:
    pickle.dump(RoomMapping, file, pickle.HIGHEST_PROTOCOL)

with open('data.yml', 'w') as outfile:
    yaml.dump(RoomMapping, outfile, default_flow_style=False)
