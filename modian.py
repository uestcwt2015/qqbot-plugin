# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import re
import csv
import sys
from qqbot import qqbotsched

reload(sys)
sys.setdefaultencoding('utf-8')
@qqbotsched(second ='0-59/10')
def modian(bot):
    gl = bot.List('group', 'BEJ48-李梓应援会')
    def getModianData(pageId):
        def getCsvFile(fileSrc):
            dict = {}
            reader = csv.DictReader(open(fileSrc, "r"))

            for row in reader:
                obj = row
                key = obj['name'].encode('utf-8')
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


        r = requests.get("https://zhongchou.modian.com/realtime/ajax_dialog_user_list?jsonpcallback=jQuery1111007096074430665023_1518192432338&origin_id=11168&type=backer_list&page=" + str(pageId) + "&page_size=20&cate=2&_=1518192432343")
        r.encoding = 'utf-8'
        pattern = re.compile(r'<ul[\s\S]*<[\s\S]*>')
        str1 = r.text.encode('utf-8').decode('string_escape')
        content = re.sub(r'\\n', '', pattern.findall(str1)[0])
        contentStr = re.sub(r'\\/', '/', content);
        soup = BeautifulSoup(contentStr, 'lxml')
        items = soup.find_all("div", class_="item_cont")
        dict1 = getCsvFile("./test.csv")
        hasChange = False
        # dict2 = {}
        for item in items:
            p = item.find_all('p')
            key = p[0].get_text()
            value = p[1].get_text().decode('unicode_escape')[1:]
            
            # dict2[key] = value
            
            change = computeChange(key, value, dict1)
            
            if change != 0:
                hasChange = True
                print key.decode('unicode_escape'), change
                sendMessage = '感谢'+ key.decode('unicode_escape') + '集资了' + str(change) + '元'
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
    mainPage = requests.get("https://zhongchou.modian.com/realtime/get_simple_product?jsonpcallback=jQuery111109347054952963518_1518455206519&ids=11168&if_all=1&_=1518455206520")
    mainPage.encoding = 'utf-8'
    pattern = re.compile(r'\{"id"[\s\S]*\}');
    mainData = json.loads(pattern.findall(mainPage.text)[0])
    personNum = mainData["backer_count"]
    currentMoney = mainData["backer_money"]
    pageCount = personNum / 20 + 1

    for i in range(1, pageCount+1):
        getModianData(i)


# reader = csv.DictReader(open("./test.csv", "r"))
# for row in reader:
    # print row['name'].decode('unicode_escape'), row['money']