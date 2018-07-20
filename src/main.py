import requests
import re


def getViewstate(text):
    # 这里使用这样的正则表达式匹配__VIEWSTATE字段，使用Python requests应该这样匹配，其他浏览器可能不一样
    data = re.match(
        r'.*id\=\"\_\_VIEWSTATE\" value\=\"(.*)\" \/\>\r\n\r\n\<div class\=\"acountWrap\"\>', text, re.S)
    return data.group(1)


url_1 = 'http://222.192.89.21/sims3/default.aspx'
url_2 = 'http://222.192.89.21/sims3/buyRecord.aspx'
cookies = "{'ASP.NET_SessionId': 'idd1fueg2bcpwokoybevvfjj'}"  # 可自行替换
data = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': '', 'drlouming': '', 'DropDownList1': '',
        'drceng': '', 'dr_ceng': '', 'drfangjian': '', 'radio': 'buyR', 'ImageButton1.x': '45', 'ImageButton1.y': '4'}  # 这个待完善

response = requests.post(url_1, data=data, cookies=cookies)
