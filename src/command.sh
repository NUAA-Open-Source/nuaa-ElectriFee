# 修改第一条指令中的参数drlouming DropDownList1 drceng dr_ceng drfangjian，即可使用第二条指令查询不同区域、类别的电费余额。具体该是怎样的参数……很复杂，不知道是哪个#￥&%的程序员写的。同时建议修改cookie值

curl -b "ASP.NET_SessionId=" -d "__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=&drlouming=&DropDownList1=&drceng=&dr_ceng=&drfangjian=&radio=buyR&ImageButton1.x=52&ImageButton1.y=11" "http://222.192.89.21/sims3/default.aspx"

# 第二条指令获取数据
curl -o data.html -b "ASP.NET_SessionId=" "http://222.192.89.21/sims3/buyRecord.aspx"
