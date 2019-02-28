#!/usr/bin/env python
#-*- encoding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')


'''
  产生评估算法的中间数据
      1. 拉取相似结果    &&  计算仅相似的去重率
      2. 拉取规则结果    &&  计算仅规则的去重率

      3. 拉取 top100 互联网书 以及对应付费书  &&  仅规则多少对   仅相似度多少对

      获取 规则 和 相似 的相交 gid
'''
if __name__ == '__main__':

    '''
      规则、相似: gid normName normAuthor fee
    '''
    allGids = '../resource/all_gids.txt'                # 有章节信息的 gid
    ruleResult = '../resource/rule_result.txt'          # 规则结果
    simResult = '../resource/sim_result.txt'            # 相似度结果
    #finallyResult = '../resource/finally_result.txt'    # 最后结果的 免费书top100
    finallyResult = './item_info.txt'    # 最后结果的 免费书top100
    ruleResultCheck = './rule_result.txt'

    top100FreeSim = './top100_free_mapping_charge.txt'


    allGidDict = {}
    ruleDict = {}
    simDict = {}
    simDictTemp = {}
    '''

    # 有章节信息的 gid
    with open(allGids, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            allGidDict[line] = 0

    # 获取规则计算结果
    #fw = open(ruleResultCheck, 'w')
    with open(ruleResult, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) != 6:
                continue
            if allGidDict.has_key(arr[0]):
                ruleDict[arr[3] + '|' + arr[4]] = arr[0]
                #fw.write(arr[0] + '\t' + arr[3] + '\t' + arr[4] + '\n')
    #fw.close()
    print ('rule + sim 涉及数量: ' + str(len(allGidDict)))

    # 规则去重率计算
    print ('规则去重率: ' + str(float(len(allGidDict) - len(ruleDict)) / len(allGidDict)))
    del ruleDict

    # 相似度计算的结果
    with open(simResult, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) != 3 or float(arr[2]) < 0.5:
                continue
            for i in arr[:2]:
                if simDictTemp.has_key(i):
                    simDictTemp[i] = simDictTemp[i] | set(arr[:2])
                else:
                    simDictTemp[i] = set(arr[:2])
    def gid_cmp(x, y):
        return int(x[2:]) - int(y[2:])
    for ik, iv in simDictTemp.items():
        m = list(iv)
        m.sort(cmp=gid_cmp)
        simDict['|'.join(m)] = 0
    for ik, iv in allGidDict.items():
        if not simDictTemp.has_key(ik):
            simDict[ik] = 0
    print ('相似度去重率: ' + str(float(len(allGidDict) - len(simDict)) / len(allGidDict)))
    del simDictTemp
    del simDict
    del allGidDict

    '''

    ###################### 不依赖上边的变量 ########################
    # 获取免费书 top100 对应付费书情况
    freeTopNum = 100
    freeTop = []
    finallyPair = {}
    gidFee = {}
    with open(ruleResult, 'r') as fr:
        index = 0
        def free_cmp(x, y):
            return int(x[1]) - int(y[1])
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) != 6:
                continue
            gid = arr[0]
            fee = arr[1]
            view = arr[2]
            name = arr[3]
            author = arr[4]
            if name == '' or author == '':
                continue
            if finallyPair.has_key(name + '|' + author):
                finallyPair[name + '|' + author] += '|' + gid
            else:
                finallyPair[name + '|' + author] = gid
            if int(fee) == 1:
                gidFee[gid] = int(fee)
                continue
            freeTop.append((gid, view, name, author))
            if len(freeTop) > freeTopNum:
                freeTop.sort(cmp = free_cmp, reverse=True)
                freeTop = freeTop[:freeTopNum]
    # top100 对应付费书
    fw = open(top100FreeSim, 'w')
    for ele in freeTop:
        gid, view, name, author = ele
        flag = 'no'
        key = ''
        if finallyPair.has_key(name + '|' + author):
            arr = finallyPair[name + '|' + author].split('|')
            for i in arr:
                if gidFee.has_key(i):
                    flag = 'yes'
            key = finallyPair[name + '|' + author]
        fw.write(gid + '\t' + key + '\t' + flag + '\n')
    fw.close()









