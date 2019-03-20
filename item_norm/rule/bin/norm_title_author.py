#!/bin/env python
#-*- coding=utf-8 -*-

import re
import os
import thread
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from langconv import *

# 字符全角转半角
def str_Q2B(ustring):
    '''把字符串全角转半角'''
    rstring = ""
    for uchar in ustring.decode("utf-8"):
        inside_code = ord(uchar)
        if inside_code == 12288:        # 空格全角转半角
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:
            inside_code -= 65284
        #if inside_code < 0x0020 or inside_code > 0x7e:
        #    rstring += uchar
        else:
            rstring += unichr(inside_code)
    return rstring.encode('utf-8')

# 字符串大写转小写
def str_u2l(ustring):
    return ustring.lower()

# 中文繁体转简体
def str_f2j(ustring):
    line = Converter('zh-hans').convert(ustring.decode('utf-8'))
    return line.encode('utf-8')

# 汉字替换数字
def str_h2s(ustring):
    mdict = {"一":"1", "二":"2", "三":"3", "四": "4", "五":"5", "六":"6", "七":"7", "八": "8", "九":"9", "十":"10","①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9", "⑩": "10","Ⅺ":"11","Ⅹ":"10","Ⅸ":"9", "Ⅷ ": "8", "Ⅶ ": "7", "Ⅵ": "6", "Ⅴ": "5", "Ⅳ": "4", "Ⅲ": "3", "Ⅱ": "2", "Ⅰ": "1", "xx": "20", "xix": "19", "xviii": "18", "xvii": "17", "xvi": "16", "xv": "15", "xiv": "14", "xiii": "13", "xii": "12", "xi": "11", "ix": "9", "x": "10", "viii": "8", "vii": "7", "vi": "6", "iv": "4", "v": "5", "iii": "3", "ii": "2", "i": "1"}
    arr = re.findall(r'(一|二|三|四|五|六|七|八|九|十|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|Ⅺ|Ⅹ|Ⅸ|Ⅷ|Ⅶ|Ⅵ|Ⅴ|Ⅳ|Ⅲ|Ⅱ|Ⅰ|xx|xix|xviii|xvii|xvi|xv|xiv|xiii|xii|xi|ix|x|viii|vii|vi|iv|v|iii|ii|i)', ustring)
    for i in arr:
        if mdict.has_key(i):
            ustring = ustring.replace(i, mdict[i])
    return ustring

# 检测 第xx章 第xx篇
def str_chap(ustring):
    arr = re.findall(r'(第\S+?章|第\S+?集|第\S+?部|第\S+?卷|第\S+?版|第\S+?辑|第\S+?季|第\S+?篇|第\S+?册)', ustring)
    for i in arr:
        temp = str(i[3:len(i) - 3])
        ustring = ustring.replace(i, temp)
    return ustring
            
# 字符串保留可用字符(字母、数字、汉字)
def str_filtc(ustring):
    ustring = ustring.strip()
    if ustring == None or ustring == "":
        return ""
    try:
        ustring = ustring.decode('utf-8')
        outstr = ""
        for i in ustring:
            if (i >= u'\u4e00' and i <= u'\u9fa5') or (i >= u'\u0030' and i <= u'\u0039') or (i >= u'\u0041' and i <= u'\u005a') or (i >= u'\u0061' and i <= u'\u007a'):
                outstr = outstr + i
    except:
        print ("过滤非法字符错误:" + ustring + "\n")
        return ustring
    return outstr.encode('utf-8')


# 删除author中的信息
def str_delauthor(line):

    # 保留佚名
    arr = re.findall(r'佚名|文宁|文舟|文落|文涯|文房四宝|青年文库', line)
    for i in arr:
        line = i
        return line

    # ^删除[明]
    arr = re.findall(r'^[\[\(\<\{]\S+?[\]\)\>\}]', line)
    if len(arr) > 0:
        line = line.replace(arr[0], '')
    line = re.sub(r'(（\S+?）)', '', line)
    
    # ^删除 明. 
    arr = re.findall(r'^(\S+?·|\S+?\.|耕林)', line)
    if len(arr) > 0 and len(arr[0]) <= 6:
        line = line.replace(arr[0], '')

    # 删除 文~
    lineTemp = line
    line = re.sub(r'^文', '', line)
    if len(line) < 6:
        line = lineTemp

    # 去 结尾
    arr = re.findall(r'(|经济法研究|等著|编译组|主编|编著|著|编|博易创为|塔读文\S+|逐浪小说\S+|逐浪小说|时阅东方|好小说月刊|红豆文化|飞象红豆|凤鸣轩|凤凰网|书海|中润|蔷薇书院|宏文|一千零一页|红豆文化|飞象红豆|凤鸣轩|幻文\S+|幻文|二层楼|起点中文\S+|起点中文|书坊\S+|书坊|黑岩\S+|黑岩|TXT)$',line)
    for i in arr:
        line = line.replace(i, '')

    # 删除关键字
    arr = re.findall(r'(n1un1u|丶|灬|丿|^黑岩网|^黑岩|正文|全文免费阅读|最新章节免费在线阅读|出版|出版书|出书版|网络版|作者)', line)
    for i in arr:
        line = line.replace(i, '')
    return line

# 删除name中的信息
def str_delname(line):

    # 保留名字
    arr = re.findall(r'血之罪|仙剑奇侠传|科普故事|申论|鬼话连篇|星辰变后传|寓言故事|童话故事|励志故事|感人故事|营销策略|营销法则', line)
    for i in arr:
        line = i
        return line

    # 去 开头
    arr = re.findall(r'^(同人[\S+?]主|网王同人|网王之|作者:|冰蓝纱10|序曲∶|综)', line)
    for i in arr:
        line = line.replace(i, '')

    # 去 结尾
    arr = re.findall(r'(|修正篇|正版|网配|感悟\S+故事|探索与发现|中小学\S+文库|神算系列|导读|后续|半穿越|经典\S+?小说\S|青少年\S+书系|长篇|中篇|短篇|终篇|主编|前\S+?篇|故事大全|选载|作品|色女系列|河北党的\S+$|异域风格小说|已出版|其\d+|纪实|游戏大全|精选家常菜系列|5200|之番外合集|草稿|免费|新番外|番外\S+?|完|（完）|冬日暖阳mk|冰蓝纱10著|动漫同人|重制版|大结局|未删节)$',line)
    for i in arr:
        line = line.replace(i, '')

    # 提取书名号中间的信息
    arr = re.findall(r'《\S+?》', line)
    if len(arr) > 0:
        line = arr[0][3:len(arr[0]) - 3]

    # 替换
    line = re.sub(r'(上$|上部|上卷|上册)', "上", line)
    line = re.sub(r'(中$|中部|中卷|中册)', "中", line)
    line = re.sub(r'(下$|下部|下卷|下册)', "下", line)
    line = re.sub(r'(中下卷)', "中下", line)
    line = re.sub(r'(大全集$|全本$|全集$|全传$|全$|上下$|上下全$|上下部$|上\S+下$)', "全", line)

    # 删除关键字
    arr = re.findall(r'(小书房世界经典文库|新农村\S+系|公共政策\S+丛书|启蒙\S+系列|美文\S+小说|出版上市|新农村建设\S+组|企鹅口袋\S+思想|非包月|包月|小学生\S+?名著|快穿之|快穿|网文\S+?人|精读|传书|经典\S+?集|现代生活技巧丛书|基础版|抢先版|读本|学生\S+?知识|网络版|共\S+?卷|高职高专|^网王|高干宠文|世界成功励志故事|中华人名共和国\S+?中华人名共和国|中华人名共和国|启迪孩子心灵的\S+$|山海经故事丛书|美男当道|8226|总集|现代卷|出版$|\S+?力作|综漫\S+?同人|综\S+?之|综漫之|综\S+?漫|综漫|番外之\S+$|奥德修篇|番外篇|番外|丶|免费|大结局|开更|完整版|苗疆版|暂停更新|更新|网王同人|黑执事同人|浮世绘之经典\S+|合订|珍藏版|修订版|遗稿|遗著|下载|作者桑,同人本|作者都梁最新力作|作者顾漫|眉姐作者新作:|amp|nbsp|mdash|ldquo|rdquo|lt|gt|middot|middot|deg|bull|nsp|全文閱讀$)', line)
    for i in arr:
        line = line.replace(i, '')

    return line


# 删除多余字符
def str_author(line):
    line_src = line
    while True:
        line_tmp = re.sub(r'(下载|来源|类别)(.*?)$|^(.*?)(全集免费在线阅读|最新章节免费在线阅读|全文免费阅读)|(\()(书坊|纵横|黑岩|意大利法|美|俄|希腊|凯|英|明|元|挪|清|日|瑞士|宋|奥|韩|法|德|波兰|苏|隋|民国|澳|澳大利亚|意大利|北齐|南朝梁|意|周|唐|土|丹麦|春秋|晋|西汉|西晋|西班牙|隋|荷兰|TXT|塔读|3g|花火|熊猫|嬉闹异域二|战国|当代|美国|汉|完结|父子|台|合作|古穿今|黑|快本|创世|清穿|出版|出书版|网络版|阅|作者|一不小心潜了总裁|上|中|下|上部|下部|一|二|三|四|五|出书版结局|最强弃少|(重生名门|绝世风华|全本|诱欢|婚宠撩人|娇妻难养)(.*?))(\))', '', line)
        line_tmp = re.sub(r'^法国文豪|^黑岩网_|^黑岩_|^黑岩网|^黑岩|品书网$|起点中文网$|_京东|_掌阅$|^若初文学网|_hongxiu$|hongxiu$|_91$|_91x$|17k|网\(|专栏$|非包月作品$|作品集$|作品$|^文\/|\(塔\.\.\.$|^作者:|^作者|^作家|编著$|等著$|著$|TXT$|非包月$|无弹窗$|jufgh2018$|_qd22$|qd22$|_hx\d{0,2}$|_xs8$|_rn$|\.qd$|\.0$|wechatno$|cah$|^by|^诡行天下', '', line_tmp)
        line_tmp = re.sub(r'(em|#|h2)?&?[a-z]*;|[,]?unitprice(\d|&quo)?$', '', line_tmp)

        if line_tmp != line:
            line = line_tmp
        else:
            break
    if len(line) == 0 or line.isspace():
        line = line_src
    line_tmp = re.search(r'^(.*?)(\W{2,})(t|z|x|s|y|i|n|hx|gzx|/|0|1|2|3|4|5|6|7|8|01|06|_1|_9|_11)$', line, re.I)
    if line_tmp :
        line = line_tmp.group(1) + line_tmp.group(2)
    return line


# 删除多于字符
def str_name(line):
    line_src = line
    while True:
        # 删除
        line_tmp = re.sub(r'下载(.*?)$|作者桑,同人本|配国标苏教版$|作者都梁最新力作|作者顾漫|眉姐作者新作:|(作者:)(.*?)$|&amp;|amp;|&nbsp;|nbsp;|&mdash;|mdash;|&ldquo;|ldquo;|&rdquo;|rdquo;|&lt;|lt;|&gt;|gt;|&middot;|middot;|&deg;|&bull;|nsp;|丶|全文閱讀$', '', line)
        if line_tmp != line:
            line = line_tmp
        else:
            break
    if len(line) == 0 or line.isspace():
        return line
    #
    line = re.sub(r't10t(.*?)$', '', line)
    if len(line) == 0 or line.isspace():
        return line

    #去by，过滤出后边的(上|中|下|一|二|三|四|五|六|七|八|九)
    line_src = line
    line_tmp = re.search(r'^(.*?)by(.*?)(\()(上|中|下|一|二|三|四|五|六|七|八|九)', line, re.I)
    if line_tmp:
        line = line_tmp.group(1) + line_tmp.group(4)
    else:
        line_tmp = re.search(r'^(.*?)(\W+)by(.*?)$', line, re.I)
        if line_tmp:
            line = line_tmp.group(1) + line_tmp.group(2)

    #去掉结尾处的(*)，过滤掉后边包含(0|1|2|3|4|5|6|7|8|9|上|中|下|一|二|三|四|五|六|七|八|九|十)的情况
    line_src = line
    line_tmp = re.search(r'^(.*?)(\()((.*?)(0|1|2|3|4|5|6|7|8|9|上|中|下|一|二|三|四|五|六|七|八|九|十)(.*?))(\))$', line, re.I)
    if line_tmp:
        line_src = line
    else :
        line = re.sub(r'(\()(.*?)(\))$', '', line)
        if len(line) == 0 or line.isspace():
            line = line_src

    line_src = line
    while True:
        line_tmp = re.sub(r'出书版|免费$|朝小诚|全文$|全本|gl|gd$|17k$|耽美$|耳雅|完本|(\()(明星|日30更|大结局|结局|免费|书穿|乱穿|fz|黑帮重生|sk1p|lol\+妖尾|k|进击的巨人|未穿今|末世|机甲|空间|犯罪心理|空间|瓶邪|清|艾佟|风云同人|\+番外|军文|银魂|家教|重生未来|古穿今|女尊|完|完结|高干|完本|穿越|网游|红楼|重生种田|重生穿|重生|修仙|(.*?)(e10o|人鱼|言情|星星|无限恐怖|明星|暮光|空间|犬夜叉|花样|美男|继承者|乾隆|还珠|恶作剧|速|鼠猫|韩|娱乐|军|全文|反|古|兽人|修真|剑3|洪荒|火影|猎人|数码宝贝|兄弟战争|综|耽美|东方不败|快穿|系统|韩娱|陆小凤|黑篮|穿书|已上市|黑子|书包网|gl|gd|abo|17k|晋江|网配|清穿|网王|仙剑)(.*?))(\))|完结番外$|完结篇|完结版|全本完结$|未完结|已完结|完结|\(\)|\($|wwwd1da10scom$|作者陆观澜|最新章节(.*?)$|经典之作$|全文阅读(.*?)$|总裁文$|又名(.*?)$|原名(.*?)|将完$|\(全$|\(出版(.*?)$|\(修改版(.*?)$|皇城花嫁之5\)|\(结局$|\(撒如也$|\(\+出版上市$|两部$|之卷$|月下蝶影$|np经典$|最新$|星楼月影$', '', line)
        if line_tmp != line:
            line = line_tmp
        else:
            break
        if len(line) == 0 or line.isspace():
            return line
    line_src = line
    line_tmp = re.search(r'^(.*?)(全集)$', line, re.I)
    if line_tmp:
        line_tmp = re.search(r'^(.*?)大$', line_tmp.group(1), re.I)
        if line_tmp:
            line_src = line
        else:
            line = re.sub(r'全集$', '', line)

    #(.*?\d+-\d+.*?) 提取\d+-\d+
    line_tmp = re.search(r'^(.*?)(\()([^\(^\)]*?)(\d+-\d+)(.*?)(\))(.*?)$', line, re.I)
    if line_tmp:
        line = line_tmp.group(1) + line_tmp.group(4) + line_tmp.group(7)
    line = re.sub(r'(\()(1部2部3部集合|123部全)(\))', '全', line)

    #(.*?第|生子|共\d+.*?) 提取\d+
    line_tmp = re.search(r'^(.*?)(\()(.*?)(第|生子|共)(\d+)(.*?)(\))(.*?)$', line, re.I)
    if line_tmp:
        line = line_tmp.group(1) + line_tmp.group(5) + line_tmp.group(8)

    #(\d+) 去括号
    line_tmp = re.search(r'^(.*?)(\()(\d+)(\))(.*?)$', line, re.I)
    if line_tmp:
        line = line_tmp.group(1) + line_tmp.group(3) + line_tmp.group(5)

    #(\d+版|卷|神算) 提取\d+
    line_tmp = re.search(r'^(.*?)(\()(\d+)(版|卷|神算)(.*?)(\))(.*?)$', line, re.I)
    if line_tmp:
        line = line_tmp.group(1) + line_tmp.group(3) + line_tmp.group(7)

    #(番外|续传\d+) 去括号
    line_tmp = re.search(r'^(.*?)(\()(番外|续传|续)(\d+)(\))(.*?)$', line, re.I)
    if line_tmp:
        line = line_tmp.group(1) + line_tmp.group(3) + line_tmp.group(4) + line_tmp.group(6)
    line_tmp = re.search(r'^(.*?)(\()(.*?)(\)上)(.*?)$', line, re.I)
    if line_tmp :
        line = line_tmp.group(1) + "上" + line_tmp.group(5)
    line_tmp = re.search(r'^(.*?)(\()(.*?)(\)下)(.*?)$', line, re.I)
    if line_tmp :
        line = line_tmp.group(1) + "下" + line_tmp.group(5)
    line_src = line
    line = re.sub(r'\([^\(\)]*?\)$', '', line)
    return line


def str_series(line):
    # 系列名按关键字提取内容

    line = re.sub(r'(上$|中$|下$|中下$|全$|\d+?)', "", line)
    
    return line

def read_white_list(path, mdict):
    fr = open(path)
    for i in fr.readlines():
        i = i.strip('\n')
        arr = i.split('{]')
        if len(arr) != 4:
            print ('error: ' + i)
            continue
        gid = arr[0].strip('\n')
        normName = arr[1].strip('\n')
        normAuthor = arr[2].strip('\n')
        normSeries = arr[3].strip('\n')
        mdict[gid] = "" + normName + "\t" + normAuthor + "\t" + normSeries
    fr.close()
    return mdict


def main():

    global fr
    global fw

    while True:
        temp = []
        mutex_fr.acquire()
        while True:
            temp.append(fr.readline())
            if len(temp) >= 1000:
                break
        mutex_fr.release()

        if len(temp) <= 0:
            break

        for line in temp:
            outBuf = ''
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) != 5:
                print("错误行:" + line)
                if line == "" or line == None:
                    print ("执行完毕-开始退出")
                    return
                continue
            gid = arr[0]
            feeFlag = arr[1]
            viewCount = arr[2]
            name = arr[3]
            author = arr[4]
            normName = name                                                 # 归一书名
            normAuthor = author                                             # 归一作者名
            normSeries = name

            # 白名单
            if wdict.has_key(gid):
                infoArr = wdict[gid].split('\t')
                outBuf = gid + '\t' + feeFlag + '\t' + viewCount + '\t' + wdict[gid]
            else:
                # 处理name数据
                normName = str_Q2B(normName)                                # 全角转半角
                normName = str_u2l(normName)                                # 大写转小写
                normName = str_h2s(normName)                                # 汉字换数字
                normName = str_chap(normName)                               # 第 xx 部处理
                normName = str_name(normName)                               # 正则替换
                normName = str_delname(normName)                            # 删除名字中的一些数据
                normName = str_filtc(normName)                              # 过滤非法字符

                # 处理author数据
                normAuthor = str_Q2B(normAuthor)                            # 全角转半角
                normAuthor = str_u2l(normAuthor)                            # 大写转小写
                normAuthor = str_author(normAuthor)                         # 正则替换
                normAuthor = str_delauthor(normAuthor)                      # 删除名字中的一些数据
                normAuthor = str_filtc(normAuthor)                          # 过滤非法字符

                normAuthorTmp = normAuthor
                normAuthor = normAuthor.replace(normName, '')
                if (normAuthor == ""):
                    normAuthor = normAuthorTmp

                # 处理series数据
                normSeries = str_series(normName)
                outBuf = gid + "\t" + feeFlag + "\t" + viewCount + "\t" + normName + "\t" + normAuthor + "\t" + normSeries

            mutex_fw.acquire()
            fw.writelines(outBuf + "\n")
            mutex_fw.release()
    return

if __name__ == '__main__':

    if len(sys.argv) != 4:
        exit(-1)
    titleAuthor = sys.argv[1]
    whitePath = sys.argv[2]
    resultPath = sys.argv[3]

    threads = []
    wdict = {}                                  # 白名单


    # 创建两把锁
    mutex_fr = threading.Lock()
    mutex_fw = threading.Lock()

    # 读取白名单
    read_white_list(whitePath, wdict)

    fr = open(titleAuthor, 'r')
    fw = open(resultPath, 'w')

    # 多线程
    for i in range(100):
        t = threading.Thread(target=main)
        threads.append(t)
    for i in threads:
        i.setDaemon(True)
        i.start()
        i.join()

    fr.close()
    fw.close()

    exit(0)

