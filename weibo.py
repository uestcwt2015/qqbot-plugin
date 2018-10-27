import requests
import json
import re
import time

headers = {
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
  'Referer': 'https://m.weibo.cn/p/2304136330232870',
  'X-Requested-With': 'XMLHttpRequest'
}

url = 'https://m.weibo.cn/api/container/getIndex?containerid=2304136330232870'  

curr_id = 0

def getRecentWeibo():
  res = requests.get(url, headers = headers)
  cards = json.loads(res.text)['data']['cards']
  print ('waiting')
  def filterCondition(val):
    return val['card_type'] == 9

  # 遍历cards
  for card in filter(filterCondition, cards):
      blog = card['mblog']
      # 判断是否为新微博
      if blog['created_at'] == '刚刚':
        global curr_id
        if (curr_id != blog['id']):
          curr_id = blog['id']
        else:
          continue

        weibo = blogHandle(blog)
        sendMessage(weibo)
        break
      
def getTextFromHtml(str):
  reg = re.compile('<[^>]*>')
  return reg.sub('', str).replace('\n','').replace(' ','')

def blogHandle(blog):
  # 获取微博id
  weibo_id = blog['id']

  # 判断是转发还是原创,  0 -> 原创， 1 -> 转发
  weibo_type = 0
  if 'retweeted_status' in blog:
    weibo_type = 1
  else:
    weibo_type = 0
  
  #获取被转发人
  retweeted_name = ''
  if weibo_type == 1:
    retweeted_name = blog['retweeted_status']['user']['screen_name']

  # 获取微博正文
  text = getTextFromHtml(blog['text'])

  return {
    'id': weibo_id,
    'type': weibo_type,
    'text': text,
    'retweeted_name': retweeted_name
  }

def sendMessage(weibo):
  type = '发布' if weibo['type'] == 0 else '转发'
  tpl = "李梓%s了%s一条微博\n%s" % (type, weibo['retweeted_name'], weibo['text'])
  print (tpl)

while True:
  getRecentWeibo()
  time.sleep(5)