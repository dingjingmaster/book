#!/usr/bin/env python
#-*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

##
# 把 gid/name/author 格式 转为 gid/name/author/series
#

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit(-1)

    whiteListPath = sys.argv[1]

    resultDict = {}

    with open(whiteListPath, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('{]')
            if len(arr) == 4:
                exit(0)
            gid = arr[0]
            name = arr[1]
            author = arr[2]
            resultDict[gid] = (name, author, name)
    with open(whiteListPath, 'w') as fw:
        for ik, iv in resultDict.items():
            fw.write(ik + '{]' + iv[0] + '{]' + iv[1] + '{]' + iv[2] + '\n')

    exit(0)


