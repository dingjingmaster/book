#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

# 读取相似度计算范围的 gid
def read_sim_gid(path, mdict):
    fr = open(path, 'r')
    for line in fr.readlines():
        line = line.strip()
        mdict[line] = 0
    fr.close()
    return

# 读取相似度结果 取大于 2 的组数
def read_sim_pair(path, mdict):
    fr = open(path, 'r')
    for line in fr.readlines():
        line = line.strip('\n')
        arr = line.split('\t')
        if len(arr) < 2:
            continue
        for gidk in arr:
            if mdict.has_key(gidk):
                ml = list(mdict[gidk])
                for gk in arr:
                    ml.append(gk)
                mdict[gidk] = set(ml)
            else:
                mdict[gidk] = set(arr)
    fr.close()
    return

# 读取规则结果 与 相似度计算范围取交集 输出归一结果
def read_rule_pair(rulePath, simGid, ruleDict):
    ruleResult = {}
    ruleTmp = {}
    fr = open(rulePath, 'r')
    for line in fr.readlines():
        line = line.strip('\n')
        arr = line.split('\t')
        if len(arr) < 4:
            print('error line:' + line)
            continue
        gid = arr[0]
        info = arr[1:]
        if simGid.has_key(gid):
            ruleResult[gid] = info
    for gid, info in ruleResult.items():
        if len(info) != 3:
            print(info)
            continue
        key = info[0] + '|' + info[1]
        if ruleTmp.has_key(key):
            ml = list(ruleTmp[key])
            ml.append(gid)
            ruleTmp[key] = set(ml)
        else:
            ruleTmp[key] = set([gid])
    for key, gids in ruleTmp.items():
        if len(gids) < 2:
            # 规则独有
            continue
        for gid in gids:
            ruleDict[gid] = gids
    return

def compare_rule_sim(simDict, ruleDict, osimPath, orulePath, ahavePath):
    fosim = open(osimPath, 'w')
    fahave = open(ahavePath, 'w')
    forule = open(orulePath, 'w')

    for ik, iv in simDict.items():
        tmp = list(iv)
        tmp.sort()
        if ruleDict.has_key(ik):
            fahave.write(','.join(tmp) + '\n')
        else:
            fosim.write(','.join(tmp) + '\n')
    for ik, iv in ruleDict.items():
        tmp = list(iv)
        tmp.sort()
        if simDict.has_key(ik):
            fahave.write(','.join(tmp) + '\n')
        else:
            forule.write(','.join(tmp) + '\n')
    return


if __name__ == '__main__':
    #rulePath = "data/rule.txt"
    #simGidPath = "data/sim_gid.txt"
    #simPath = "data/sim.txt"

    if len(sys.argv) < 7:
        exit(-1)

    rulePath = sys.argv[1]
    simGidPath = sys.argv[2]
    simPath = sys.argv[3]

    osimPath = sys.argv[4]
    orulePath = sys.argv[5]
    ahavePath = sys.argv[6]

    simGidDict = {}
    simDict = {}
    ruleDict = {}

    # 读取相似度计算范围内的 gid
    read_sim_gid(simGidPath, simGidDict)
    print(len(simGidDict))

    # 读取相似度计算结果
    read_sim_pair(simPath, simDict)
    print (len(simDict))

    # 读取规则计算的结果
    read_rule_pair(rulePath, simGidDict, ruleDict)
    print (len(ruleDict))

    # 比较规则 和 相似度计算结果
    compare_rule_sim(simDict, ruleDict, osimPath, orulePath, ahavePath)




