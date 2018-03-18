from bs4 import BeautifulSoup
import json
import requests
import sys
import re
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

html = requests.get('https://zhongchou.modian.com/item/11168.html')
html.encoding = 'utf-8'

mainSoup = BeautifulSoup(html.text, 'lxml')

currentMount = re.sub('\D', "", mainSoup.find("div", class_="project-goal").find('h3').get_text())
totalMount = re.sub('\D', "", mainSoup.find("span", class_="goal-money").get_text());
endTime = datetime.datetime.strptime(mainSoup.find("div", class_="remain-time").find('h3')['end_time'], '%Y-%m-%d %H:%M:%S')
nowTime = datetime.datetime.now()
print endTime - nowTime;

print currentMount
print totalMount
