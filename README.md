# nuaa-ElectriFee

## 开发目的

此项目旨在为南京航空航天大学住宿生提供更方便的电费查询方式。

目前已经开发完成怡园21-22, 35-37栋空调电费查询。

目前部署的微信公众号：裂帛碎玉的想法

![](https://source.vvzero.com/wechat-qcode.jpg)



## 说明

`src/*`是获取电费的python脚本。

`inspect/inspect.txt`是本人暂时整理的对应关系。

## Usage
Before you can query Electricity Fee via query.py, you have to generate data by running ```python3 BF.py```

This script will retrieve all the info from the Electricity Query Website and build a tree structure which a dorm is pointed to a dict of arguments required to be submitted.

By executing so, you shall have a pkl file in the current working directory.

Simply run ```python3 query.py <pkl filename>``` and make a HTTP request to http://localhost:5000

Here is a sample curl request:
```
curl -d "campus=1&building=22&public_dorm=702&private_dorm=3" http://localhost:5000 -vvv
```

Then it will return all the information including remaining balance and history of electricity purchase in JSON format.

## 附录
电费查询网址（需校园内网）`http://222.192.89.21/sims3/default.aspx`
