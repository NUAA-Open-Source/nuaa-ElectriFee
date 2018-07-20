import requests
import re


def getViewstate(text):
    # 这里使用这样的正则表达式匹配__VIEWSTATE字段，使用Python requests应该这样匹配，其他浏览器可能不一样
    data = re.match(
        r'.*id\=\"\_\_VIEWSTATE\" value\=\"(.*)\" \/\>\r\n\r\n\<div class\=\"acountWrap\"\>', text, re.S)
    return data.group(1)

def getFee(text):
    # 匹配剩余电费
    data = re.match(
        r'.*\<span class\=\"number orange\"\>(\d\d\.\d\d)\<\/span\>', text, re.S)
    return data.group(1)


url_1 = 'http://222.192.89.21/sims3/default.aspx'
url_2 = 'http://222.192.89.21/sims3/buyRecord.aspx'
cookies = {'ASP.NET_SessionId': 'idd1fueg2bcpwokoybevvfjj'}  # 可自行替换
data = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': '', 'drlouming': '', 'DropDownList1': '',
        'drceng': '', 'dr_ceng': '', 'drfangjian': '', 'radio': 'buyR', 'ImageButton1.x': '45', 'ImageButton1.y': '4'}  # 需要POST的数据

# 下面模拟各次请求，以将军路校区怡园21栋空调用电为例。
# 暂时吧数据写死，先测试几下

# 第一次请求
response = requests.post(url_1, cookies=cookies)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第二次请求
data['drlouming'] = '1'
response = requests.post(url_1, cookies=cookies, data=data)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第三次请求
data['DropDownList1'] = '2'
response = requests.post(url_1, cookies=cookies, data=data)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第四次请求
data['drceng'] = '71'
response = requests.post(url_1, cookies=cookies, data=data)
data['__VIEWSTATE'] = getViewstate(response.text)

# 以下以60305模拟
# 第五次请求
data['dr_ceng'] = '219'
response = requests.post(url_1, cookies=cookies, data=data)
data['__VIEWSTATE'] = getViewstate(response.text)

# 第六次请求
data['drfangjian'] = '2799'
response = requests.post(url_1, cookies=cookies, data=data)
# print(response.text)
# print(data)

# 打印电费
print(getFee(response.text))
