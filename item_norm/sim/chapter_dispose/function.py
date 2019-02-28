#!/usr/bin/env python
#coding=utf-8
import sys
import re
reload(sys)
sys.setdefaultencoding("utf8")
sys.path.append("./jieba")
import re
import jieba
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

def is_chinese(mchar):
    if mchar >= u'\u4e00' and mchar <= u'\u9fa5':
        return True
    else:
        return False

def delete_no_chinese(mstr):
    newStr = ""
    for i in mstr:
        if True == is_chinese(i):
            newStr = newStr + i
    return newStr

def str_find_word(mstr, substr, start):
    for i in range(start, len(mstr)):
        if mstr[i] == substr:
            return i
    return -1

def delete_str_pair(oneChapter, pairList):
    line = oneChapter.strip()
    for i in pairList:
        startStr, endStr = i
        subStr = ""
        startIndex = -1
        endIndex = -1

        startIndex = str_find_word(line, startStr, 0)
        endIndex = str_find_word(line, endStr, startIndex + 1)

        if (-1 != startIndex) and (-1 != endIndex):
            subStr = line[startIndex: endIndex + 1]
        line = line.replace(subStr, '')
    return line.strip()

def delete_substr (oneChapter, strList):

    line = oneChapter.strip()
    for i in strList:
        line = line.replace(i, '')
    return line.strip()


def spark_init(master, memory, programName):
    conf = SparkConf()\
            .setMaster(master)\
            .set("spark.executor.memory", memory)\
            .set("spark.cores.max", "30")\
            .setAppName(programName)
    sc = SparkContext(conf = conf)

    return sc

def get_white_gid(path, whiteDict):
    fRead = open(path, "r")
    for i in fRead.readlines():
        i = i.strip("\n")
        if "" == i:
            continue
        whiteDict[i] = 0
    fRead.close()
    return whiteDict

def get_white_substr(path, strList):
    fRead = open(path, "r")
    for i in fRead.readlines():
        i = i.strip("\n")
        if "" == i:
            continue
        strList.append(i)
    fRead.close()
    return strList

def get_white_pair(path, pairList):
    fRead = open(path, "r")
    for i in fRead.readlines():
        i = i.strip("\n")
        if "" == i:
            continue
        arr = i.split("|")
        pairList.append((arr[0], arr[1]))
    fRead.close()
    return pairList

def get_data(sc, path):
    
    return sc.textFile(path)

# flag free 是免费书的章节处理
def dispose_charge(line, whiteDict, strList, pairList):
    line = line.strip('\n')
    arr = line.split('{]')                      # 切割，获得章节信息
    chapterNum = len(arr)
    gid = arr[1]

    chapters = []                               # 取 20 章
    lastChapter = ""                            # 上一章暂存
    thisChapter = ""                            # 本章
    chapterBuf = ""

    # 去除白名单中和章节数少的数据
    if len(gid) < 4 or whiteDict.has_key(gid) or len(arr) < 5:
        return ""

    # 删除 xxx开头 yyy 结尾的字符春
    for i in range(3, len(arr)):
        if arr[i] == "":
            continue
        thisChapter = delete_str_pair(arr[i], pairList)
        thisChapter = delete_no_chinese(thisChapter)
        thisChapter = delete_substr(thisChapter, strList)
        thisChapter = re.sub(r'^章', "", thisChapter)
        if thisChapter != "" and thisChapter != lastChapter:
            chapters.append(thisChapter)
        lastChapter = thisChapter
        if len(chapters) >= 20:
            break
    if len(chapters) < 5:
        return ""
    for i in chapters:
        # 分词
        word = jieba.cut(i, cut_all=False)
        # 章节信息相加
        for j in word:
            if len(j) <= 1:
                continue
            chapterBuf = chapterBuf + j + '{]'
    chapterBuf = chapterBuf[:-2]

    return (gid, chapterNum, chapterBuf)



# flag free 是免费书的章节处理
def dispose_free(line, whiteDict, strList, pairList):
    line = line.strip('\n')
    arr = line.split('{]')
    chapterNum = len(arr) - 3

    gid = 'i_' + arr[0]
    chapters = []                               # 取 20 章
    lastChapter = ""                            # 上一章暂存
    thisChapter = ""                            # 本章
    chapterBuf = ""

    # 去除白名单中和章节数少的数据
    if len(gid) < 4 or whiteDict.has_key(gid) or len(arr) < 4:
        return ""

    # 删除 xxx开头 yyy 结尾的字符春
    for i in range(3, len(arr)):
        if arr[i] == "":
            continue
        thisChapter = delete_str_pair(arr[i], pairList)
        thisChapter = delete_no_chinese(thisChapter)
        thisChapter = delete_substr(thisChapter, strList)
        thisChapter = re.sub(r'^章', '', thisChapter)
        if thisChapter != "" and thisChapter != lastChapter:
            chapters.append(thisChapter)
        lastChapter = thisChapter
        if len(chapters) >= 20:
            break
    if len(chapters) < 5:
        return ""
    for i in chapters:
        # 分词
        word = jieba.cut(i, cut_all=False)
        # 章节信息相加
        for j in word:
            if len(j) <= 1:
                continue
            chapterBuf = chapterBuf + j + '{]'
    chapterBuf = chapterBuf[:-2]
    return (gid, chapterNum, chapterBuf)
