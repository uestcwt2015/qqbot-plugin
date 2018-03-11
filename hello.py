# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import re
import csv
import sys
from qqbot import qqbotsched
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf-8')
today = 0
yesterday = 0

@qqbotsched(hour='23', minute="59", second="59")
def clearToday(bot):
    today = 0

#集资链接定时发送
@qqbotsched(hour="8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23", minute='30')
def sendJiZiMessage(bot):
    currentTime = datetime.datetime.now()
    zongxuan = datetime.datetime.strptime('2018-07-28 16:00:00', '%Y-%m-%d %H:%M:%S')
    delat = zongxuan - currentTime
    date = delat.days + 1
    todayJizi = today - yesterday
    messageString = '第五届总选举日常打卡VOL.1\n三月份，新的一年总选战役已经打响了。希望她能站在更大的舞台上发光、希望她能被更多人了解，希望成为她引以为傲的底气。您的每一份支持，都是对李梓的最大肯定!\n聚沙成塔、积水成渊，让我们一起加油吧\n打赏链接：https://mourl.cc/WHWz58' + '\n距离总选还有'+date+'天' + '\n今日已集资:' + str(todayJizi) + '元'
    gl = bot.List('group', 'BEJ48-李梓应援会')
    if gl is not None:
        for group in gl:
            bot.SendTo(group, messageString)

@qqbotsched(second ='0-59/10')
def modian(bot):
    gl = bot.List('group', 'BEJ48-李梓应援会')
    def getModianData(pageId):
        def getCsvFile(fileSrc):
            dict = {}
            global yesterday
            reader = csv.DictReader(open(fileSrc, "r"))

            for row in reader:
                obj = row
                key = obj['name'].encode('utf-8')
                if key == 'liziToday':
		    yesterday = float("".join(obj["money"].split(",")))
		    continue
                value = obj['money']
                dict[key] = value
            return dict

        def computeChange(name, value, dict):
            if dict.has_key(name):
                oldValue = dict[name]
                dict[name] = value
                return float(value) - float(oldValue)
            else:
                dict[name] = value
                return float(value)


        r = requests.get("https://zhongchou.modian.com/realtime/ajax_dialog_user_list?jsonpcallback=jQuery1111012500599667616874_1520115037871&origin_id=11887&type=backer_list&page=" + str(pageId) + "&page_size=20&cate=2&_=1520115037875")
        r.encoding = 'utf-8'
        pattern = re.compile(r'<ul[\s\S]*<[\s\S]*>')
        str1 = r.text.encode('utf-8').decode('string_escape')
        content = re.sub(r'\\n', '', pattern.findall(str1)[0])
        contentStr = re.sub(r'\\/', '/', content);
        soup = BeautifulSoup(contentStr, 'lxml')
        items = soup.find_all("div", class_="item_cont")
        dict1 = getCsvFile("./test.csv")
        now = time.localtime(time.time())
    	hour = time.strftime('%H', now)
    	minute = time.strftime('%M', now)
    	second = time.strftime('%S', now)
    	if hour == '17' and minute == '45':
	    dict1['liziToday'] = currentMoney
        hasChange = False
        
	# 获取总信息
	
        # dict2 = {}
        for item in items:
            p = item.find_all('p')
            key = p[0].get_text()
            value = p[1].get_text().decode('unicode_escape')[1:]

            # dict2[key] = value
            
            change = computeChange(key, value, dict1)

            if change != 0:
                hasChange = True
		todayJizi = today - yesterday
                sendMessage = '感谢'+ key.decode('unicode_escape') + '集资了' + str(change) + '元\n' + '当前集资进度：' + str(currentMoney) + '元\n' + '目标金额：' + str(totalMoney) + '元\n' + '剩余时间：' + str(date) + '天\n' + '支持人数：' + str(personNum) + '\n请一起为小偶像助力:\nhttps://mourl.cc/WHWz58\n' + '距离总选还有' + str(zxDate) + '天' + '\n今日已集资:' + str(todayJizi) + '元'  
                if gl is not None:
                    for group in gl:
                        bot.SendTo(group, sendMessage)
        # csvFile = open("./test.csv", 'w')
        # fieldnames = ['name', 'money']
        # writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        # writer.writeheader()
        # for key, value in dict2.items():
        #     print key,value
        #     writer.writerow({'name': key.decode('utf-8'), 'money': value})

        if hasChange:
            csvFile = open("./test.csv", 'w')
            fieldnames = ['name', 'money']
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in dict1.items():
                writer.writerow({'name': key.decode('utf-8'), 'money': value})
        else:
            return;
    mainPage = requests.get("https://zhongchou.modian.com/realtime/get_simple_product?jsonpcallback=jQuery111100022240854852233483_1520115134069&ids=11887&if_all=1&_=1520115134070")
    mainPage.encoding = 'utf-8'
    pattern = re.compile(r'\{"id"[\s\S]*\}');
    mainData = json.loads(pattern.findall(mainPage.text)[0])
    currentTime = datetime.datetime.now()
    endTime = datetime.datetime.strptime('2018-03-31 23:59:59', '%Y-%m-%d %H:%M:%S')
    zongxuan = datetime.datetime.strptime('2018-07-28 16:00:00', '%Y-%m-%d %H:%M:%S')
    delat = endTime - currentTime
    zxDelat = zongxuan - currentTime
    date = delat.days + 1
    zxDate = zxDelat.days + 1
    personNum = mainData["backer_count"]
    currentMoney = mainData["backer_money"]
    global today
    today = float("".join(currentMoney.split(",")))
    totalMoney = mainData["goal"]
    pageCount = personNum / 20 + 1
    for i in range(1, pageCount+1):
        getModianData(i)


# reader = csv.DictReader(open("./test.csv", "r"))
# for row in reader:
    # print row['name'].decode('unicode_escape'), row['money']
