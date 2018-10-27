import requests
from bs4 import BeautifulSoup
import re
import sys
from qqbot import qqbotsched

reload(sys)
sys.setdefaultencoding('utf-8')
cookieUrl = 'http://3ns2r9.v.vote8.cn/Front/VerifyCodeImage/Vote8Click.ashx'
headers = {
    'Cookie': 'Vote.VerifyCodeAtFirst=1519976599,c38e54f27b4a5a916d330f34eda4d45d; CNZZDATA5855278=cnzz_eid%3D1077353255-1519959197-%26ntime%3D1519975651; Vote.WeixinPublicAccountHasSubscribed.2870615=2018/3/2 15:01:57|6b549089278f13e72c9fc4706db87124; Vote.HasVoteJustNow=1; Vote.IsFromOptionSearch=1; ctrl_time=1; yjs_id=3601b584b41580656d9dba76c669dbe3; ASP.NET_SessionId=domwq21dcwxcpkjxjlaqhnu1; UM_distinctid=161e4b5a9e75-053d98dd3a0008-513f1d4a-c0000-161e4b5a9e81e3; __cfduid=d185bfe00b7c707c540fdcaa758b6cc4b1519960564',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.6.3 NetType/WIFI Language/zh_CN',
    'Referer': 'http://3ns2r9.v.vote8.cn/m/Rank',
    'Accept-Language': 'zh-cn',
    'X-Requested-With': 'XMLHttpRequest'
}
r0 = requests.get(cookieUrl, headers=headers).content.split(',');
url0 = 'http://3ns2r9.v.vote8.cn/m/Rank'
data = "hiddenVote8ClickValidateCode=" + r0[0]+'%2C'+r0[1]+"&hiddenVerifyAtFirstType=Vote8Click"
headers1 = {
    'Cookie': 'CNZZDATA5855278=cnzz_eid%3D1077353255-1519959197-%26ntime%3D1519975651; Vote.VerifyCodeAtFirst=1519974117,27536d28d9e045279773293caea05ff7; Vote.WeixinPublicAccountHasSubscribed.2870615=2018/3/2 15:01:57|6b549089278f13e72c9fc4706db87124; Vote.HasVoteJustNow=1; Vote.IsFromOptionSearch=1; ctrl_time=1; yjs_id=3601b584b41580656d9dba76c669dbe3; ASP.NET_SessionId=domwq21dcwxcpkjxjlaqhnu1; UM_distinctid=161e4b5a9e75-053d98dd3a0008-513f1d4a-c0000-161e4b5a9e81e3; __cfduid=d185bfe00b7c707c540fdcaa758b6cc4b1519960564',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.6.3 NetType/WIFI Language/zh_CN',
    'Origin': 'http://3ns2r9.v.vote8.cn/m/',
    'Referer': 'http://3ns2r9.v.vote8.cn/m/Rank',
    'Accept-Language': 'zh-cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Upgrade-Insecure-Requests': '1',
    'Content-Length': '109',
    'Connection': 'keep-alive',
    'Host': '3ns2r9.v.vote8.cn'
}
print data
r1 = requests.post(url0, headers=headers1, data=data)
print r1.content

url = 'http://3ns2r9.v.vote8.cn/m/Rank'


# r.encoding = 'utf-8'
# print r.content;
# r = requests.post(url, headers=headers)
# 
# soup = BeautifulSoup(r.text, 'lxml')
# list = soup.find_all(text=re.compile("129"))
# print soup