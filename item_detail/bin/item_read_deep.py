#!/usr/bin/env python2
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")
import time
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

cpName = {\
        '0'  : '免费书',\
        '1'  : '盛大',\
        '6'  : '纵横',\
        '8'  : '掌阅',\
        '9'  : '3G书城',\
        '10' : '书海',\
        '11' : '畅读',\
        '12' : '逐浪',\
        '13' : '凤栖梧小说网',\
        '14' : '九库文学',\
        '15' : '一千零一页',\
        '17' : '云阅文学',\
        '18' : '品阅',\
        '19' : '绝版中文网',\
        '20' : '大麦中金',\
        '21' : '哎呦互娱',\
        '22' : '阅明中文网',\
        '24' : '阅路小说网',\
        '25' : '酷匠网',\
        '26' : '咪咕阅读',\
        '27' : '永正',\
        '28' : '纸尚',\
        '29' : '万众中文网',\
        '30' : '凤凰书城',\
        '31' : '果维文化',\
        '33' : '网易云阅读',\
        '34' : '点众',\
        '44' : '景象文学',\
        '45' : '趣阅小说网',\
        '46' : '蔷薇书院',\
        '47' : '米汤中文网',\
        '48' : '神起中文网',\
        '49' : '锦瑟文学',\
        '50' : '书香文府',\
        '51' : '丹鼎四海',\
        '52' : '聚点艺盛',\
        '54' : '鼎甜科技',\
        '55' : '原创书殿',\
        '56' : '塔读',\
        '57' : '逸云书院',\
        '58' : '悦客中文网',\
        '59' : '落尘文学',\
        '60' : '作客文学网',\
        '61' : '凤鸣轩',\
        '62' : '幻想工场',\
        '63' : '文博',\
        '64' : '恺兴',\
        '65' : '创酷中文网',\
        '66' : '龙阅读',\
        '67' : '青春说',\
        '68' : '鬼姐姐',\
        '69' : '大鱼中文网',\
        '70' : '奇文阅读',\
        '71' : '艾月乐美',\
        '72' : '藤痕书院',\
        '73' : '天阅书城',\
        '74' : '幻想中文网',\
        '75' : '圣诞文学网',\
        '76' : '不可能的世界',\
        '77' : '青果阅读',\
        '78' : '玄娱中文网',\
        '79' : '有乐中文网',\
        '80' : '寒武纪年原创网',\
        '81' : '起创文学',\
        '82' : '四月天',\
        '83' : '0度小说',\
        '84' : '黑岩阅读',\
        '85' : '天下书盟',\
        '86' : '古阅读',\
        '87' : '老虎发威',\
        '88' : '风起中文网',\
        '89' : '恒言中文网',\
        '90' : '书丛网',\
        '91' : '长江中文网',\
        '92' : '华夏天空',\
        '93' : '豆读言情',\
        '94' : '阅书中文网',\
        '95' : '中天和信',\
        '96' : '公版书籍',\
        '97' : '梧桐中文',\
        '98' : '起承中文网',\
        '99' : '品阅文学网',\
        '100': '大唐中文网',\
        '101': '安夏书院',\
        '102': '触阅文化传媒',\
        '103': '恋小说',\
        '104': '星汇传媒',\
        '105': '雁北堂',\
        '106': '中文在线',\
        '107': '北京红阅科技',\
        '108': '磨铁中文网',\
        '109': '书影阅读',\
        '110': '四喜文学',\
        '111': '飞扬文学网',\
        '1000012': '2000000035',\
        '1000002': '云起',\
        '1000001': '阅文',\
        '1056029': '小说阅读网',\
        '1047626': '潇湘书院',\
        '1000023': '红袖添香',\
        '1000024': '言情小说吧',\
        '1000003': '起点女生', \
        '1000009': '起点文学网',\
        '1000005': '起点男生'\
        }


# 判断是否为数字
def is_num(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


# spark 初始化
def spark_init(master, memory, programName):
    conf = SparkConf().setMaster(master)\
            .set("spark.executor.memory", memory)\
            .set("spark.cores.max", "30")\
            .setAppName(programName)
    sc = SparkContext(conf = conf)
    return sc


# 获取物品信息
def get_data(sc, path):
    return sc.textFile(path)


def get_flag(mstr):
    if len(mstr) >= 3:
        mstr = mstr[:3]
    return mstr


def parse_item_info(x):
    name = ""
    author = ""
    maskLevel = ""
    freeFlag = ""
    by = ""
    tf = ""
    ncp = ""
    gid = ""
    fc = ""
    
    data = x.split("\t")
    gid = data[0]
    
    for i in range(1, len(data)):
        if data[i] == "name":
            name = data[i + 1]
            continue
        elif data[i] == "author":
            author = data[i + 1]
            continue
        elif data[i] == "mask_level":
            maskLevel = data[i + 1]
            continue
        elif data[i] == "fee_flag":
            freeFlag = data[i + 1]
            continue
        elif data[i] == "by":
            by = data[i + 1]
            continue
        elif data[i] == "tf":
            tf = data[i + 1]
            continue
        elif data[i] == "ncp":
            ncp = data[i + 1]
            continue
        elif data[i] == "fc":
            fc = data[i + 1]
            continue
    if len(gid) <= 4 or name == "" or freeFlag == "0" or freeFlag == "10":
        return ""
    if ncp != "" and cpName.has_key(ncp):
        ncp = cpName[ncp]


    mt = "0"
    maskLevel = get_flag(maskLevel)
    for i in maskLevel:
        if int(i) == 1:
            mt = "1"
    maskLevel = mt

    by = get_flag(by)
    tf = get_flag(tf)
    fc = get_flag(fc)


    return (gid, (name, author, maskLevel, freeFlag, by, tf, ncp.decode('utf8'), fc))


# 解析日志，获取需要数据
def parse_log(x):
    x = x.strip('\n')
    uid = ""
    curChap = ""
    appUdid = ""
    bookType = ""
    userType = ""
    gid = ""
    isCharge = ""
    chargeBegin = ""
    entrance = ""
    infos = x.split("\001")
    phoneUdid = infos[12]
    arrs = infos[21].split("\002")
    for i in arrs:
        arr = i.split("\003")
        if arr[0] == "uid":
            uid = arr[1]
            continue
        elif arr[0] == "sort":
            curChap = arr[1]
            continue
        elif arr[0] == "appudid":
            appUdid = arr[1]
            continue
        elif arr[0] == "gid":
            gid = arr[1]
            continue
        elif arr[0] == "ischapterincharged":
            isCharge = arr[1]
            continue
        elif arr[0] == "chargebeginsort":
            chargeBegin= arr[1]
            continue
        elif arr[0] == "booktype":
            bookType = arr[1]
            continue
        elif arr[0] == "usertype":
            userType = arr[1]
            continue
        elif arr[0] == "entrance":
            entrance = arr[1]
            continue
        else:
            continue
    gid = "i_" + str(gid)
    appUdid = phoneUdid
    # 滤除没有书籍 id 的日志信息
    if len(gid) <= 4 or appUdid == "" or entrance != u'书架' or curChap == "" or chargeBegin == ""\
            or isCharge != u'付费'\
            or (not is_num(curChap)) or (not is_num(chargeBegin)) or int(curChap) < int(chargeBegin):
        return ""
    return (gid, (appUdid, curChap, userType, bookType))


def detail_info(x):
    gid, info = x
    infos, itemInfo = info
    
    name, author, maskLevel, freeFlag, by, tf, ncp, fc = itemInfo

    filter = {}
    # 非包月书
    userNum = 0                             # 用户数(去重)
    chapterNum = 0                          # 章节数次(无去重)
    appudidDict = {}
    curChapDict = {}

    # 包月书 - 包月用户
    bysByuUserNum = 0
    bysByuChapterNum = 0
    bysByuAppudidDict = {}
    bysByuCurChapDict = {}

    # 包月书 - 非包月用户
    bysFbyuUserNum = 0
    bysFbyuChapterNum = 0
    bysFbyuAppudidDict = {}
    bysFbyuCurChapDict = {}


    for i in infos:
        appUdid, curChap, userType, bookType = i
        if not filter.has_key(appUdid):
            filter[appUdid] = 1
        else:
            continue
        if by != u'000':
            if userType == u'包月':
                bysByuAppudidDict[appUdid] = 1
            else:
                bysFbyuAppudidDict[appUdid] = 1
        else:
            appudidDict [appUdid] = 1
    filter = {}

    for i in infos:
        appUdid, curChap, userType, bookType = i
        if not filter.has_key(str(curChap) + str(appUdid)):
            filter[str(curChap) + str(appUdid)] = 1
        else:
            continue
        if by != u'000':
            if userType == u'包月':
                bysByuCurChapDict[str(curChap) + str(appUdid)] = 1
            else:
                bysFbyuCurChapDict[str(curChap) + str(appUdid)] = 1
        else:
            curChapDict[str(curChap) + str(appUdid)] = 1

    # 包月书
    bysByuUserNum = len(bysByuAppudidDict)
    bysFbyuUserNum = len(bysFbyuAppudidDict)

    bysByuChapterNum = len(bysByuCurChapDict)
    bysFbyuChapterNum = len(bysFbyuCurChapDict)

    # 非包月书统计
    userNum = len(appudidDict)
    chapterNum = len(curChapDict)             # 涉及到的付费章节数

    outBuf = "" + gid + "\t" + name + "\t" + author\
            + "\t" + maskLevel + "\t" + freeFlag + "\t" + by + "\t" + tf + "\t" + ncp + "\t" + fc\
            + "\t" + str(userNum) + "\t" + str(chapterNum)\
            + "\t" + str(bysByuUserNum) + "\t" + str(bysByuChapterNum)\
            + "\t" + str(bysFbyuUserNum) + "\t" + str(bysFbyuChapterNum)

    return outBuf


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-1)
    itemInfoPath = sys.argv[1]
    logPath = sys.argv[2]
    savePath = sys.argv[3]
    
    sc = spark_init("spark://qd01-tech2-spark001:7077,qd01-tech2-spark002:7077", "20g", "item_buy")

    # 获取日志并解析
    itemInfo = get_data(sc, itemInfoPath)\
            .map(lambda x: parse_item_info(x))\
            .filter(lambda x: x != "")
    
    # 获取日志并解析得到购买量
    readLog = get_data(sc, logPath)\
            .map(lambda x: parse_log(x))\
            .filter(lambda x: x != "")\
            .groupByKey()

    buyInfo = readLog.join(itemInfo)
    buyResult = buyInfo.map(lambda x: detail_info(x))

    # 输出
    buyResult.repartition(1)\
            .filter(lambda x: x != "")\
            .saveAsTextFile(savePath)

    sc.stop()
    exit(0)













