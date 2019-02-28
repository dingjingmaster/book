#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from function import spark_init
from function import get_data
from function import get_white_gid
from function import get_white_substr
from function import get_white_pair
from function import dispose_free
from function import dispose_charge

#chapterPath = "hdfs://10.26.24.165:9090/rs/appsinfo/data/item_norm/chapter_info/"
gidWhiteListPath = "gid_white_list.txt"                                                                 # 书籍白名单



if __name__ == '__main__':

    if len(sys.argv) != 8:
        exit (-1)
    whiteListGidPath = sys.argv[1]
    whiteListPairPath = sys.argv[2]
    whiteListSubStrPath = sys.argv[3]
    chargeChapterPath = sys.argv[4]
    freeChapterPath = sys.argv[5]
    itemInfoPath = sys.argv[6]
    savePath = sys.argv[7]

    whiteDict = {}
    strList = []
    pairList = []

    #sc = spark_init("local", "20g", "dispose_chapter")
    sc = spark_init("spark://qd01-tech2-spark001:7077,qd01-tech2-spark002:7077", "20g", "dispose_chapter")
    #sc = spark_init("", "20g", "content_similarity")
    gidChapter = sc.parallelize([])

    # 白名单
    get_white_gid(whiteListGidPath, whiteDict)

    # 要删除的关键字链表
    get_white_substr(whiteListSubStrPath, strList)

    # 要删除的字符对
    get_white_pair(whiteListPairPath, pairList)

    whiteDictG = sc.broadcast(whiteDict)
    strListG = sc.broadcast(strList)
    pairListG= sc.broadcast(pairList)

    # 处理付费书
    chargeChapters = get_data(sc, chargeChapterPath)\
            .map(lambda x: dispose_charge(x, whiteDictG.value, strListG.value, pairListG.value))\
            .filter(lambda x: x != "")

    # 处理免费书
    freeChapters = get_data(sc, freeChapterPath)\
            .map(lambda x: dispose_free(x, whiteDictG.value, strListG.value, pairListG.value))\
            .filter(lambda x: x != "")

    gidChapter = gidChapter.union(freeChapters)
    gidChapter = gidChapter.union(chargeChapters)

    gidChapter.map(lambda x: x[0] + "\t" + str(x[1]) + "\t" + x[2])\
            .repartition(1)\
            .saveAsTextFile(savePath)


