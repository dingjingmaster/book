#!/usr/bin/env python
#-*- encoding=utf-8 -*-


def read_file(path, itemDict):
    item = 0
    pair = 0

    mdict = {}

    with open(path, "r") as fr:
        for line in fr.readlines():
            line = line.strip("\n")
            arr = line.split("\t")
            gid = ""
            normName = ""
            normAuthor = ""
            if len(arr) == 4:
                gid = arr[0]
                normName = arr[1]
                normAuthor = arr[2]
            else:
                gid = arr[0]
                normName = arr[3]
                normAuthor = arr[4]
            if "" == normName or "" == normAuthor:
                continue
            if not itemDict.has_key(gid):
                itemDict[gid] = 0
                continue

            if mdict.has_key(normName + normAuthor):
                m = mdict[normName + normAuthor]
                m.add(gid)
                mdict[normName + normAuthor] = m
            else:
                m = set()
                m.add(gid)
                mdict[normName + normAuthor] = m
    for ik, iv in mdict.items():
        if len(iv) <= 1:
            continue
        pair += 1
        item += len(iv)
    return (pair, item)





if __name__ == '__main__':

    rulePath = "../resource/rule_result1.txt"
    finallyPath = "../resource/finally_result.txt"

    ruleItem = 0
    finallyItem = 0

    rulePair = 0
    finallyPair = 0

    itemDict = {}

    with open(finallyPath, "r") as fr:
        for line in fr.readlines():
            line = line.strip("\n")
            arr = line.split("\t")
            itemDict[arr[0]] = 0
    finallyPair, finallyItem = read_file(finallyPath, itemDict)
    rulePair, ruleItem = read_file(rulePath, itemDict)

    print rulePair
    print ruleItem
    print "---------------"
    print finallyPair
    print finallyItem





    
