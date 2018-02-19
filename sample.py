# -*- coding: utf-8 -*-

# 插件加载方法：
# 1. 启动 qqbot
# 2. 将本文件保存至 ~/.qqbot-tmp/plugins 目录 （或 c:\user\xxx\.qqbot-tmp\plugins ）
# 3. 在命令行窗口输入： qq plug sample
import sys,urllib,urllib2,httplib,json,os,time,random
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')

isRollOpen = False #roll点 开启/guan关闭属性
isReceiveYYHmessage = True #是否开启YYH聊天反馈
isAIopen = False #是否开启AI聊天
tiaojiaoDic = {}
#控制指令
setNstructionsI = ['-roll stop','-roll open','-yyh open','-yyh stop','-AI open','-AI stop']

#链接返回功能
noticeDic = {"公告" : "单独输入前面的字 展示后面的内容\n"
                    "集资 奇幻加冕礼·千秋乐集资\n"
                    "集资奖励 集资奖励详情\n"
                    "安利 安利链接\n"
                    "新人须知 一些饭圈常识\n"
                    "公告五 暂无\n"
                    "公告六 暂无\n"
                    "公告七 暂无\n"
                    "公告八 暂无\n"
                    "公告九 暂无\n",
           "集资":"「流淌的热血凝聚在心间照亮那长夜」\n"
		 " 奇幻加冕礼·千秋乐集资\n"
		 " 给落幕以完美，为更好的明天！\n"
		 "  微打赏链接：https://wds.modian.com/show_weidashang_pro/10577?mdsf=1090311_share_sms_ios_wdsxiangmu_10577\n"
		 "本次集资支出结余依旧全部用于今后的应援及总选活动\n"
                 "集资奖励请随时关注应援会公告～",
           "集资奖励": "待定",
		   #"第四期金曲大赏集资奖励：\n"
                  #"在第五弹微打赏项目中\n"
                   #"满1000元将会获赠 2017年李梓应援会秋冬应援服一件\n"
                   #"(印制ID的特殊版本)\n"
                   #"应援服购买链接：http://t.cn/Rj6aVuC (网页)",
                   # "满183元获赠一套书签\n"
                   # "满283元获赠鼠标垫两个（Q版和真人）\n"
                   # "满383元获赠两个鼠标垫加一套书签。\n"
                   # "（书签和鼠标垫奖励不包邮）\n"
                   # "胶卷相册奖励：\n"
                   # "满183元，获得一次抽奖机会，283元2次机会，以此类推，抽奖机会上限为每人5次，抽三个人。（每个id不可重复中奖）\n"
                   # "集资前三名不参与抽奖，直接获得胶卷相册奖励\n"
                   # "本期集资第一名可获得有言在仙绝版单人签名海报一张",
           "安利": "欢迎您加入BEJ48-李梓应援会！\n"
                 "李梓，BEJ48 TeamE成员，昵称为荔枝，梓宝。2000年8月30日出生于四川内江，是一位元气十足，帅酷可爱的少女。应援色是充满了光芒与活力的黄色。\n"
                 "以下为补档链接\n"
                 "偶像本人B站主页http://t.cn/RCNqa1H\n"
                 "应援会B站主页http://t.cn/RCN5wq7\n"
                 "微博超级话题http://t.cn/RCN5D6V\n"
                 "◆她跳舞真好看◆\n"
                 "经典→纯情主义http://t.cn/RCNf6Co?\n"
                 "酷炫→UZA http://t.cn/ROZnPOi\n"
                 "热血→无尽旋转http://t.cn/RCNfWgp\n"
                 "唯美→锦鲤抄http://t.cn/RCNfDT1\n"
                 "甜蜜→巧克力糖果http://t.cn/RCNIbtI\n"
                 "帅气→爱的加速器http://t.cn/RCNIxD4\n"
                 "燃炸→RIVERhttp://t.cn/RCNI8AW\n"
                 "女王→lay downhttp://t.cn/RCNMAmk",
           "新人须知": "1、李梓所属团体“BEJ48”，是中国最大的女团 “SNH48”在北京的姐妹团。\n"
                   "取自于“BeiJing”缩写，目前分为team B、team  E（李梓所在）和team J三支队伍。\n"
                   "2、BEJ48有专属的剧场，地址在朝阳区的悠唐购物中心\n"
                   "每周末会在剧场举办演出，演出内容为精心编排的 歌舞（即“公演”）\n"
                   "通过公演，粉丝可以每周都见到李梓！\n"
                   "同时，公演也通过斗鱼直播、bilibili直播等平台对外同步直播。\n"
                   "3、李梓官方认证的对外平台只有新浪微博。下载APP“ 口袋48”，可以看到李梓平时的直播。\n"
                   "4、作为流行乐组合，BEJ48一直在推出自己的歌曲与专辑。李梓参与了BEJ48推出的全部4张专辑的录制 。\n"
                   "5、SNH48 Group 每年有两次盛会：仲夏的【总选】&年末的【金曲大赏】。\n"
                   "“总选”就像是对团内小偶像们的期末考试，成绩取决于粉丝们的投票，是粉丝们对偶像一年来努力的最大肯定与支持。成绩好，会得到更好的资源。李梓第一年参加总选，取得27名的好成绩。说不定电影《有言在仙》选她做主演，也是受到这个因素的影响！\n"
                   "“金曲大赏”是年底的一场大型演唱会，表演的歌曲由粉丝投票决定。去年李梓与林思意、杨韫玉两位前辈演唱的《巧克力糖果》，取得了第8名的好成绩！\n"
                   "6:成员是不允许私下和粉丝联系的 ,也不允许在微博上回复粉丝。可以在口袋48直播的时回答粉丝问题,可以在口袋房间里回复粉丝.\n"
                   "7： q群里询问个人隐私 QQ 微信 等 在群里会被视为挑事的。\n"
                   "所以切忌这样做，也不要开和成员相关的玩笑。",
           "公告五": "暂无",
           "公告六": "暂无",
           "公告七": "暂无",
           "公告八": "暂无",
           "公告九": "暂无"}


#收到消息回调
def onQQMessage(bot, contact, member, content):
    # print bot,content,contact,member.name

    global isReceiveYYHmessage
    global setNstructionsI
    global isAIopen
    global noticeDic
    global tiaojiaoDic
    setTiaojiaoDic()
    # 判断是否处理消息
    if  not isReceiveYYHmessage and "养成" != contact.name:return

    print content
    if '@ME' in content:
        if "-roll" in content:
            rollNember(bot,contact,member,content)
        else:

            if isAIopen:
                askString = content.replace("[@ME]", "")
                while (askString.startswith(" ")):
                    askString = askString[1:]
                print  askString
                print  tiaojiaoDic
                if askString in tiaojiaoDic.keys():
                    bot.SendTo(contact, '@' + member.name + " " + tiaojiaoDic[askString])
                else:
                    aiRobot(bot, contact, member, content)
    elif content == '-stop' and "养成" == contact.name:
        bot.SendTo(contact, '机器人关闭')
        bot.Stop()

    elif content == '-help' and "养成" == contact.name:
        bot.SendTo(contact, ("@ME  获取是否运行\n"
                             + "-stop 关闭机器人\n"
                             + "-help 获取帮助\n"
                             + "-liveList 获取最近的视频列表\n"
                             + "@ME -roll 获取0-100之间的随机数\n"
                             + "-roll open/stop YYH随机数开启/关闭\n"
                             + "-yyh open/stop YYH反馈开启/关闭\n"
                             + "-AI open/stop AI聊天开启/关闭\n"
                             + "公告 获取公告类提醒消息的指令\n"
                             + "-调教#问题#答案 调教机器人对话功能\n"
                             + "-----------功能状态-----------\n"
                             + "roll功能状态：" + str(isRollOpen) + "\n"
                             + "应援会反馈：" + str(isReceiveYYHmessage) + "\n"
                             + "AI聊天状态：" + str(isAIopen) + "\n"))

    elif content == '-liveList' and "养成" == contact.name:
        getLiveList(bot)
    elif content in  setNstructionsI  and "养成" == contact.name: #开关类控制指令
        setToolOpen(content,bot)
    # elif content in noticeDic.keys():   #公告提醒功能
      #  time.sleep(0.1)
      #  bot.SendTo(contact, noticeDic[content])
    elif  content.startswith("-调教")  and "养成" == contact.name:#调教功能
        tiaoJiaoAI(bot, contact, member, content)
    # elif "吉祥" in content and ("女朋友" in content or "媳妇" in content):
    #     bot.SendTo(contact, '@' + member.name + " " + "人家和吉祥没有关系了啦，人家其实是喜欢你的，" + member.name + "我喜欢你，好喜欢你")




from qqbot import qqbotsched

#集资链接定时发送
@qqbotsched(minute='30')
def sendJiZiMessage(bot):
    nowTimeValue = time.time()
    defferTime = int(1508583000 - nowTimeValue)
    timeString = ""
    if defferTime > 0:
        day = defferTime / (24 * 60 * 60)
        print day
        hour = (defferTime - day * 24 * 60 * 60) / (60 * 60)
        print hour
        minutes = (defferTime - day * 24 * 60 * 60 - hour * 60 * 60) / 60
        print minutes
        if day > 0:
            timeString = str(day) + "天" + str(hour) + "小时" + str(minutes) + "分"
        elif hour > 0:
            timeString = str(hour) + "小时" + str(minutes) + "分"
        else:
            timeString = str(minutes) + "分"
        print timeString

    messageString = "B50金曲大赏已经结束，第五届SNH48group总选举新的赛季已悄悄打响。\n你的每一份支持，都将是对李梓的鼓励。\n新年到，一起来为小孩梓包份红包吧！\n打赏地址：\nhttp://suo.im/44rZ41"
    if timeString:
        messageString = messageString + '\n距离公演倒计时: ' + timeString
    gl = bot.List('group', 'BEJ48-李梓应援会')
    if gl is not None:
        for group in gl:
            bot.SendTo(group, messageString)


#微博测试代码
# @qqbotsched(second ='0-40/20')
def weiboPool2(bot):
    httpsConn = httplib.HTTPSConnection("m.weibo.cn")
    headers = {"Content-type": "application/json; charset=utf-8"}
    httpsConn.request("GET",
                      'https://m.weibo.cn/api/container/getIndex?uid=1573330832&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%90%89%E7%A5%A5%E6%98%AF%E4%B8%87%E8%83%BD%E7%9A%84&featurecode=20000320&type=uid&value=1573330832&containerid=1076031573330832',
                      '', headers)
    res = httpsConn.getresponse()
    if res.status != 200 : print '1 微博数据 status！= 200'; return
    if res.reason != 'OK': print '1 微博数据 reason！= OK '; return

    data = res.read()
    hjson = json.loads(data)
    list = hjson["cards"]
    # 文件操作
    currentpath = os.getcwd()
    path = currentpath + '/weibo.txt'
    writeType = "w+"
    if os.path.isfile(path):
        writeType = "r+"
    writefile = open("weibo.txt", writeType)  # 创建文件
    fileText = writefile.read()

    if fileText == "":
        print  '2 新写文件'
        for weiboDic in list:
            writefile.seek(0,2)
            itemid = weiboDic['itemid']
            writefile.write(itemid + "|")
    else:
        itemIDList = fileText.split("|")
        for weiboDic in list:
            itemid = weiboDic['itemid']
            if itemid not in itemIDList:
                print '3 发送消息-新微博'
                #取数据
                mblog = weiboDic["mblog"]
                scheme = weiboDic["scheme"]
                messageString = ""
                if mblog: #为空判断
                    text = mblog['text']

                    if text:
                        add = True #判断字符串是否添加
                        for c in text:
                            if c == "<":
                                add = False
                            elif c == ">":
                                add = True
                                continue
                            if  add:
                                messageString = messageString + c
                    else: print "4 微博内容为空"; return

                #发送消息操作
                gl = bot.List('group', '养成')
                if gl is not None:
                    for group in gl:
                        sendMessage = "梓民吉祥发布了一条微博：" +  messageString + '\n' + scheme
                        bot.SendTo(group, sendMessage)
                #文件操作
                writefile.seek(0,2)
                writefile.write(itemid + "|")  # 新消息加入文件记录 最后一条
                # fileText = itemid + "|" + fileText
                # fileText = fileText[:-36]
                # writefile.truncate()
                # writefile.write(fileText)
            #else:
                #print " 5 没有新微博"

    writefile.close()
#微博轮询
@qqbotsched(second ='0-50/10')
def weiboPool(bot):
    httpsConn = httplib.HTTPSConnection("m.weibo.cn")
    headers = {"Content-type": "application/json; charset=utf-8"}
    httpsConn.request("GET",
                      'https://m.weibo.cn/api/container/getIndex?uid=5880066726&luicode=10000011&lfid=100103type%3D3%26q%3D%E6%9D%8E%E6%A2%93&featurecode=20000320&type=uid&value=5880066726&containerid=1076035880066726',
                      '', headers)
    res = httpsConn.getresponse()
    if res.status != 200 : print '6 微博数据 status！= 200'; return
    if res.reason != 'OK': print '7 微博数据 reason！= OK '; return

    data = res.read()
    hjson = json.loads(data)
    data = hjson["data"]
    list = data["cards"]
    # 文件操作
    currentpath = os.getcwd()
    path = currentpath + '/weibo.txt'
    writeType = "w+"
    if os.path.isfile(path):
        writeType = "r+"
    writefile = open("weibo.txt", writeType)  # 创建文件
    fileText = writefile.read()

    if fileText == "":
        print  '8 新写文件'
        for weiboDic in list:
            itemid = weiboDic['itemid']
            writefile.seek(0,2)
            writefile.write(itemid + "|")
    else:
        itemIDList = fileText.split("|")
        for weiboDic in list:
            itemid = weiboDic['itemid']
            if itemid not in itemIDList:
                print '9 发送消息-新微博'
                #取数据
                mblog = weiboDic["mblog"]
                scheme = weiboDic["scheme"]
                messageString = ""
                if mblog: #为空判断
                    text = mblog['text']

                    if text:
                        add = True #判断字符串是否添加
                        text = text.replace("<br/>","\n")
                        for c in text:
                            if c == "<":
                                add = False
                            elif c == ">":
                                add = True
                                continue
                            if  add:
                                messageString = messageString + c
                    else: print " 10 微博内容为空"; return

                #发送消息操作
                gl = bot.List('group', 'BEJ48-李梓应援会')
                if gl is not None:
                    for group in gl:
                        sendMessage = "小偶像发布了一条微博：" +  messageString + '\n' + scheme
                        bot.SendTo(group, sendMessage)
                #文件操作
                itemid = itemid + "|"
                writefile.seek(0,2)#f.seek(offset [, whence]) whence 为0表示当前文件位置在文件开头，1表示在上次read后的地方，2表示文件末尾。offset为偏移量。
                writefile.write(itemid)  # 新消息加入列表
                # fileText = itemid + "|" + fileText
                # fileText = fileText[:-36]
                # writefile.truncate()
                # writefile.write(fileText)
            #else:
               # print "11 没有新微博"

    writefile.close()

#口袋房间轮询
#@qqbotsched(second ='0-50/10')
def koudaiRoom(bot):
    httpsConn = httplib.HTTPSConnection("pjuju.48.cn")
    bodyDic = "{\"roomId\":5777247,\"chatType\":0,\"lastTime\":0,\"limit\":10}"
    headers = {"Content-type": "application/json; charset=utf-8","token":"tf2hZI8N9ZPEKK4jzfFma95QcGQaVU9clJfvZ7hTo9MM7gu4az05RU86iSrUWVg6OY4eAF9ifbM="}
    httpsConn.request("POST",
                      'https://pjuju.48.cn/imsystem/api/im/v1/member/room/message/mainpage',
                      bodyDic, headers)
    res = httpsConn.getresponse()
    if res.status != 200:  print '12 口袋房间 status != 200'; return
    if res.reason != 'OK': print '13 口袋房间 reason !=  OK'; return

    data = res.read()
    hjson = json.loads(data)
    if hjson["status"] != 200:
        print '14 口袋房间数据错误'
        return
    list = hjson["content"]["data"]
    if not list:
        print "15 口袋无数据"
        return
    # 文件操作
    currentpath = os.getcwd()
    path = currentpath + '/koudaiRoom.txt'
    writeType = "w+"
    if os.path.isfile(path):
        writeType = "r+"
    writefile = open("koudaiRoom.txt", writeType)  # 创建文件
    fileText = writefile.read()

    if fileText == "":
        print  '16 口袋新写文件'
        for messageDic in list:
            writefile.seek(0,2)
            itemid = messageDic['msgidClient']
            writefile.write(itemid + "|")
    else:
        itemIDList = fileText.split("|")
        for messageDic in list:
            itemid = messageDic['msgidClient']
            time = messageDic['msgTimeStr']
            if itemid not in itemIDList:
                print '17 发送消息-口袋房间'
                # 取数据
                messageTime = messageDic["msgTimeStr"]
                extInfo = messageDic["extInfo"]
                extDic = eval(extInfo) #字符串转字典
                messageString = ""
                print extDic
                if extDic:  # 为空判断
                    messageObject = extDic['messageObject'] #类型 live text
                    if messageObject == 'live':
                        title = extDic['referenceTitle']  # 房间名字
                        contentName = extDic['referenceContent']  # 标题
                        # streamPath = extDic['streamPath'] #直播地址
                        # messageString = "小偶像-直播：" + title + "\n" + contentName + '\n' + "不一定能看的地址：" + streamPath +'\n' + time
                        messageString = "小偶像-直播：" + title + "\n" + contentName + '\n' + time
                    elif messageObject == "text":
                        text = extDic['text']
                        messageString = "小偶像-口袋房间消息：\n" + text + '\n' + time
                    elif messageObject == "faipaiText":
                        lzMessage = extDic['messageText']
                        faipaiName = extDic['faipaiName']
                        faipaiContent = extDic['faipaiContent']
                        senderName = extDic['senderName']
                        messageString = senderName + "：" + lzMessage + "\n---------------\n" + faipaiName + "这个梓民被翻牌：" + faipaiContent + '\n' + time
                    else:
                        writefile.seek(0,2)
                        writefile.write(itemid + "|")
                        writefile.close()
                        return
                        text = extDic['text']
                        messageString = "小偶像-口袋房间-测试消息：\n" + text + '\n' + time

                # 发送消息操作
                gl = bot.List('group', 'BEJ48-李梓应援会')
                if gl is not None:
                    for group in gl:
                        sendMessage = messageString
                        bot.SendTo(group, sendMessage)
                # 文件操作
                writefile.seek(0,2)
                writefile.write(itemid + "|")  # 新消息id加入列表

    writefile.close()
    return

#获取视频列表
def getLiveList(bot):
    httpsConn = httplib.HTTPSConnection("plive.48.cn")
    bodyDic = "{\"lastTime\":0,\"groupId\":0,\"type\":1,\"memberId\":327591,\"limit\":20,\"giftUpdTime\":0}"
    headers = {"Content-type": "application/json; charset=utf-8","version":'5.0.1',"os":"android",
               "token":"Y2G+5alzSPPEKK4jzfFma95QcGQaVU9cP8Jb43PVOdOU/sDohdPftAHKr726rLLTOY4eAF9ifbM="}
    httpsConn.request("POST",
                      'https://plive.48.cn/livesystem/api/live/v1/memberLivePage',
                      bodyDic, headers)
    res = httpsConn.getresponse()
    messageString = ""
    if res.status != 200:  messageString = '列表获取失败 status != 200'
    if res.reason != 'OK': messageString = '列表获取失败 reason !=  OK'

    data = res.read()
    hjson = json.loads(data)
    reviewList = hjson['content']['reviewList']
    if reviewList:
        for messageDic in reviewList:
            subTitle = messageDic['subTitle']
            streamPath = messageDic['streamPath'] #视频地址
            startTime = messageDic['startTime']
            startTime = startTime/1000
            timeloa = time.localtime(startTime)
            messageTime = time.strftime("%Y-%m-%d %H:%M:%S", timeloa)
            messageString = messageString + messageTime + "\n" + subTitle + "\n" + streamPath + "\n"

    gl = bot.List('group', '养成')
    if gl is not None:
        for group in gl:
            sendMessage = messageString
            bot.SendTo(group, sendMessage)

    return

#获取随机数
def rollNember(bot, contact, member, content):
    global isRollOpen
    number = random.randint(0, 100)
    numberStr = str(number)
    if contact.name == "养成" and isRollOpen == True:
        gl = bot.List('group', '养成')
        if gl is not None:
            for group in gl:
                sendMessage = member.name + ':'  + numberStr
                bot.SendTo(group, sendMessage)

    elif contact.name == "BEJ48-李梓应援会" and isRollOpen == True:
        gl = bot.List('group', 'BEJ48-李梓应援会')
        if gl is not None:
            for group in gl:
                sendMessage = member.name + ':' + numberStr
                bot.SendTo(group, sendMessage)

    return

#设置参数
def setToolOpen(content,bot):
    global isRollOpen
    global isReceiveYYHmessage
    global isAIopen
    if content == "-roll stop":
        isRollOpen = False

    elif content == "-roll open":
        isRollOpen = True

    elif content == "-yyh open":
        isReceiveYYHmessage = True

    elif content == "-yyh stop":
        isReceiveYYHmessage = False
    elif content == "-AI open":
        isAIopen = True
    elif content == "-AI stop":
        isAIopen = False

    gl = bot.List('group', '养成')
    if gl is not None:
        for group in gl:
            sendMessage ="roll功能状态：" + str(isRollOpen) + "\n"\
            + "应援会反馈：" + str(isReceiveYYHmessage) + "\n"\
            + "AI聊天状态：" + str(isAIopen) + "\n"
            bot.SendTo(group, sendMessage)

#AI聊天
def aiRobot(bot, contact, member, content):
    print  "18 AI聊天"
    key = "7929e064b34d445e8c13a1b25735ac38"
    info = content.replace("[@ME]", "")
    userid = member.qq
    name = member.name
    bodyDic = "{\"key\":\"%s\",\"info\":\"%s\",\"userid\":\"%s\"}" % (key, info, userid)
    print  bodyDic
    headers = {"Content-type": "application/json; charset=utf-8"}

    httpConn = httplib.HTTPConnection("www.tuling123.com")
    httpConn.request("POST",
                      'http://www.tuling123.com/openapi/api',
                      bodyDic, headers)
    res = httpConn.getresponse()

    if res.status != 200 : messageString = 'AI聊天 status != 200'
    if res.reason != 'OK': messageString = 'AI聊天  reason !=  OK'
    data = res.read()
    hjson = json.loads(data)
    code = hjson["code"]

    print code
    messageString = "@" + name + " " #发送的消息
    print data
    # 100000
    # 文本类
    # 200000
    # 链接类
    # 302000
    # 新闻类
    # 308000
    # 菜谱类
    if code == 100000:
        messageString = messageString + hjson["text"]
    elif code == 200000:
        messageString = messageString + hjson["text"] + "\n" + hjson["url"]
    elif code == 302000:
        list = hjson["list"]
        messageString = messageString + hjson["text"] + "\n"
        for dic in list:
            messageString = messageString + hjson["article"] + "\n" + hjson["detailurl"] + "\n"
    elif code == 308000:
        messageString = hjson["text"] + "\n"
        list = hjson["list"]
        for dic in list:
            messageString = messageString + hjson["name"] + "\n" + hjson["info"] + "\n" + hjson["detailurl"] + "\n"
    else:
        messageString = messageString + "AI错误"

    global isAIopen

    if contact.name == "养成" :
        gl = bot.List('group', '养成')
        if gl is not None:
            for group in gl:
                bot.SendTo(group, messageString)

    elif contact.name == "BEJ48-李梓应援会":
        gl = bot.List('group', 'BEJ48-李梓应援会')
        if gl is not None:
            for group in gl:
                bot.SendTo(group, messageString)

def jxzhuanyong(bot,contact,member):
    string = "@" + member.name + " 吉祥："
    strlist = ["英俊潇洒","风流倜傥","玉树临风","神勇威武",
               "天下无敌","宇内第一","寂寞高手","唯你独尊",
               "玉面郎君","仁者无敌","勇者无惧","英明神武",
               "侠义非凡","义薄云天","古往今来","无与伦比",
               "谦虚好学","简直是前不见古人后不见来者","玉树临风",
               "风度翩翩","器宇轩昂","万人敬仰","无人能及",
               "玉树临风","内外谦备","才华横溢","情操高尚",
               "超级无敌","炉火纯青","登峰造极","人间人爱 树见花开",
               "烛照天下","明见万里","雨露苍生","泽被万方",
               "龙行虎步","才比宋玉","是世界上最棒","最给力的人",
               "你简直就是No.1","我对你的敬仰犹如滔滔不绝延绵不绝",
               "又如黄河泛滥,一发不可收拾","你是人中之龙",
               "细长的眉毛，高挑的鼻梁，尖细的下颚，加上一双明亮得像钻石般的眼眸，时而闪着睥睨万物的神彩，让他看起来像只趾高气扬的波斯猫，优美的粉红色薄唇有些刻薄的上扬，带了点嚣张的味道，所有的五官在他脸上组合成了完美的长相，一身名牌的高级衣服，包裹着纤细却不失阳刚的身子，那不将任何人放在眼里的傲慢模样，在人群中特别显著。","只见那人俊美绝伦，脸如雕刻般五官分明，有棱有角的脸俊美异常。外表看起来好象放荡不拘，但眼里不经意流露出的精光让人不敢小看。一头乌黑茂密的头发，一双剑眉下却是一对细长的桃花眼，充满了多情，让人一不小心就会沦陷进去。高挺的鼻子，厚薄适中的红唇这时却漾着另人目眩的笑容。",
               "如黑曜石般澄亮耀眼的黑瞳，闪着凛然的英锐之气，在看似平静的眼波下暗藏着锐利如膺般的眼神，配在一张端正刚强、宛如雕琢般轮廓深邃的英俊脸庞上，更显气势逼人，令人联想起热带草原上扑向猎物的老虎，充满危险性",
               "一个浑身散发着淡淡冷漠气息的男孩背光而站。他低着头，碎碎的刘海盖下来，遮住了眉目。在日光灯的照耀下，男孩那层次分明的茶褐色头发顶上居然还映着一圈儿很漂亮的亮光。凛冽桀骜的眼神，细细长长的单凤眼，高挺的鼻梁下是两瓣噙着骄傲的薄唇。最引人注目的是他左眉骨上那一排小小的闪着彩色光芒的彩虹黑曜石眉钉，和他的眼神一样闪着犀利的光芒。",
               "这样的外貌和神情，第一眼，就让人觉得他太锋利，有一种涉世已久的尖锐和锋芒。",
               "白衣黑发，衣和发都飘飘逸逸，不扎不束，微微飘拂，衬着悬在半空中的身影，直似神明降世。他的肌肤上隐隐有光泽流动，眼睛里闪动着一千种琉璃的光芒。容貌如画，漂亮得根本就不似真人 这种容貌，这种风仪，根本就已经超越了一切人类的美丽。他只是随便穿件白色的袍子，觉得就算是天使，也绝对不会比他更美。这种超越的男女，超越了世俗的美态，竟是已不能用言词来形容","他肤色白皙,五官清秀中带着一抹俊俏,帅气中又带着一抹温柔!他身上散发出来的气质好复杂,像是各种气质的混合,但在那些温柔与帅气中,又有着他自己独特的空灵与俊秀! 他的个头少说也在一米八以上,一袭略...",
               "他拥有仿佛精雕细琢般的脸庞，英挺、秀美的鼻子和樱花般的唇色。他嘴唇的弧角相当完美，似乎随时都带着笑容。这种微笑，似乎能让阳光猛地从云层里拨开阴暗，一下子就照射进来，温和而又自若。他欣长优雅，穿着得体的米色休闲西服，手上一枚黑金闪闪的戒指显示着非凡贵气，整个人都带着天生高贵不凡的气息。",
               "男孩俊美的脸庞曲线像古希腊神话传说中的美少年纳喀索斯一样圆润完美。长长的睫毛在眼睛下方打上了一层厚厚的阴影，斜飞入鬓的眉毛在凌乱刘海的遮盖下若隐若现，高而挺的鼻梁下是一张微显饱满的嘴唇，粉粉的，像海棠花瓣的颜色。只见他的嘴角含着一丝玩味的笑容，透着点坏坏的味道。男孩歪了歪头，笑容在脸上漾开，美得让人心惊。当他歪头的时候，露出他戴着白色狼牙耳钉的漂亮耳朵。真是一个妖精般美丽的男子，有着介乎于男人与女人之间的美，危险而又邪恶。",
               "一双温柔得似乎要滴出水来的澄澈眸子钳在一张完美俊逸的脸上，细碎的长发覆盖住他光洁的额头，垂到了浓密而纤长的睫毛上，一袭白衣下是所有人都不可比的细腻肌肤。 在午后的阳光下，没有丝毫红晕，清秀的脸上只显出了一种病态的苍白，却无时不流露出高贵淡雅的气质，配合他颀长纤细的身材。","光洁白皙的脸庞，透着棱角分明的冷俊；乌黑深邃的眼眸，泛着迷人的色泽；那浓密的眉，高挺的鼻，绝美的唇形，无一不在张扬着高贵与优雅，这，这哪里是人，这根本就是童话中的白马王子嘛！","浓密的眉毛叛逆地稍稍向上扬起，长而微卷的睫毛下，有着一双像朝露一样清澈的眼睛，英挺的鼻梁，像玫瑰花瓣一样粉嫩的嘴唇，还有白皙的皮肤……","一张坏坏的笑脸，连两道浓浓的眉毛也泛起柔柔的涟漪，好像一直都带着笑意，弯弯的，像是夜空里皎洁的上弦月。白皙的皮肤衬托着淡淡桃红色的嘴唇，俊美突出的五官，完美的脸型，特别是左耳闪着炫目光亮的钻石耳钉，给他的阳光帅气中加入了一丝不羁……","只见那人俊美绝伦，脸如雕刻般五官分明，有棱有角的脸俊美异常。外表看起来好象放荡不拘，但眼里不经意流露出的精光让人不敢小看。一头乌黑茂密的头发，一双剑眉下却是一对细长的桃花眼，充满了多情，让人一不小心就会沦陷进去。高挺的鼻子，厚薄适中的红唇这时却漾着另人目眩的笑容。","只见他身材伟岸，肤色古铜，五官轮廓分明而深邃，犹如希腊的雕塑，幽暗深邃的冰眸子，显得狂野不拘，邪魅性感。他的立体的五官刀刻般俊美，整个人发出一种威震天下的王者之气，邪恶而俊美的脸上此时噙着一抹放荡不拘的微笑。","俊秀非凡，风迎于袖，纤细白皙的手执一把扇，嘴角轻钩，美目似水，未语先含三分笑，说风流亦可，说轻佻也行","白皙的皮肤，一双仿佛可以望穿前世今生的耀眼黑眸，笑起来如弯月，肃然时若寒星。直挺的鼻梁，唇色绯然，轻笑时若鸿羽飘落，甜蜜如糖，静默时则冷峻如冰。侧脸的轮廓如刀削一般，棱角分明却又不失柔美，真是让人心动啊。","光洁白皙的脸庞，透着棱角分明的冷俊；乌黑深邃的眼眸，泛着迷人的色泽；那浓密的眉，高挺的鼻，绝美的唇形，无一不在张扬着高贵与优雅","浓密的眉毛叛逆地稍稍向上扬起，长而微卷的睫毛下，有着一双像朝露一样清澈的眼睛，英挺的鼻梁，像玫瑰花瓣一样粉嫩的嘴唇，还有白皙的皮肤……","一张坏坏的笑脸，连两道浓浓的眉毛也泛起柔柔的涟漪，好像一直都带着笑意，弯弯的，像是夜空里皎洁的上弦月。白皙的皮肤衬托着淡淡桃红色的嘴唇，俊美突出的五官，完美的脸型，特别是左耳闪着炫目光亮的钻石耳钉，给他的阳光帅气中加入了一丝不羁……","只见那人俊美绝伦，脸如雕刻般五官分明，有棱有角的脸俊美异常。外表看起来好象放荡不拘，但眼里不经意流露出的精光让人不敢小看。一头乌黑茂密的头发，一双剑眉下却是一对细长的桃花眼，充满了多情，让人一不小心就会沦陷进去。高挺的鼻子，厚薄适中的红唇这时却漾着另人目眩的笑容。","一个半跪在地面上的紫发男子。那是一个极美的男子，长眉若柳，身如玉树，上身纯白的衬衣微微有些湿，薄薄的汗透过衬衣渗出来，将原本绝好的身体更是突显的玲珑剔透。长长的紫发披在雪白颈后，简直可以用娇艳欲滴来形容。一个男子能长成这样，也是天下少有。"]
    number = random.randint(0, len(strlist))
    string = string + strlist[number]
    gl = bot.List('group', contact.name)
    if gl is not None:
        for group in gl:
            bot.SendTo(group, string)
#机器人调教
def tiaoJiaoAI(bot, contact, member, content):
    # 文件操作
    global tiaojiaoDic
    currentpath = os.getcwd()
    path = currentpath + '/tiaojiao.txt'
    writeType = "w+"
    if os.path.isfile(path):
        writeType = "r+"
    writefile = open("tiaojiao.txt", writeType)  # 创建文件
    fileText = writefile.read()
    if fileText == "":
        print  '17 AI调教开始'
        startMessage = "\"你的主人是谁\":\"吉祥\""
        writefile.seek(0,2)
        writefile.write(startMessage)
    else:
        list = content.split("#")
        if len(list) == 3:
            if list[1] in tiaojiaoDic:
                bot.SendTo(contact, "内容已存在，暂时不支持修改")
                return
            writeStr =  "," + '\"' + list[1] + '\"' + ":" + '\"'+ list[2] + '\"'
            writefile.seek(0,2)
            writefile.write(writeStr)
            tiaojiaoDic[list[1]] = list[2]
            bot.SendTo(contact,member.name + "谢谢指导，已添加")
        else:
            bot.SendTo(contact, "设置调教内容失败，可能符号错误")
            return

    writefile.close()



#机器人调教字典初始化
def setTiaojiaoDic():
    global tiaojiaoDic
    if  tiaojiaoDic: return #如果字典有值不用初始化
    currentpath = os.getcwd()
    path = currentpath + '/tiaojiao.txt'
    writeType = "w+"
    if os.path.isfile(path):
        writeType = "r+"
    writefile = open("tiaojiao.txt", writeType)  # 创建文件
    fileText = writefile.read()
    if fileText == "":
        print  '20 AI调教开始'
        startMessage = "\"你的主人是谁\":\"吉祥\""
        writefile.seek(0,2)
        writefile.write(startMessage)
    else:
        fileText = fileText + "}"
        tiaojiaoDic = eval(fileText)
    writefile.close()
