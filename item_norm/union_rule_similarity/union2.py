#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

# 读取相似度结果 并合并
def read_sim_result(path, mdict):
    with open(path, 'r') as fr:
        for line in fr.readlines():
            line = line.strip()
            arr = line.split('\t')
            simresult = float(arr[2])
            if simresult < 0.5:
                continue
            for gid in arr[:2]:
                if mdict.has_key(gid):
                    mdict[gid] = set(arr[:2]) | mdict[gid]
                else:
                    mdict[gid] = set(arr[:2])
    #print ("相似度涉及书籍: %d" % (len(mdict)))
    return

# 读取规则结果
def read_rule_result(path, mdict):
    naGids = {}
    with open(path, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) != 6 or '' == arr[0] or '' == arr[3] or '' == arr[4]:
                #print ("规则结果错误行: " + line)
                continue
            gid = arr[0]
            normName = arr[3]
            normAuthor = arr[4]
            key = normName + normAuthor 
            if naGids.has_key(key):
                v = naGids[key]
                v.add(gid)
                naGids[key] = v
            else:
                v = set()
                v.add(gid)
                naGids[key] = v
    # 整理成和相似度结果相同的形式
    for ik, igs in naGids.items():
        if len(igs) < 2:
            continue
        for gid in igs:
            mdict[gid] = igs
    del naGids
    #print ("规则涉及书籍: %d" % (len(mdict)))
    return

# 规则结果和相似度结果合并
def union_sim_rule(simDict, ruleDict, resultDict):
    outDict = {}
    # 共有
    for ik, iv in simDict.items():
        if ruleDict.has_key(ik):
            resultDict[ik] = iv | ruleDict[ik]
    print ("整合规则+相似-共有的完成")

    # 以规则独有
    for ik, iv in ruleDict.items():
        if not simDict.has_key(ik):
            resultDict[ik] = iv
    print ("整合规则+相似-规则独有完成")

    # 相似度独有
    for ik, iv in simDict.items():
        if not ruleDict.has_key(ik):
            resultDict[ik] = iv
    print ("整合规则+相似-相似独有完成")
    return

def out_result(itemInfo, resultDict, outResultPath):
    fw = open(outResultPath, 'w')
    ii = {}
    with open(itemInfo, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) != 6 or '' == arr[0]:
                print ("错误行:" + line)
                continue
            gid = arr[0]
            feeFlag = arr[1]
            viewCount = arr[2]
            name = arr[3]
            author = arr[4]
            series = arr[5]
            if '' == feeFlag:
                feeFlag = "0"
            if '' == viewCount:
                viewCount = "0"
            ii [gid] = (feeFlag, viewCount, name, author, series)
        print ("读取物品信息 " + str(len(ii)) + "条")
    # 过滤并输出
    filter = {}
    def gid_cmp(x, y):
        return int(x[2:]) - int(y[2:])
    # 有归一化结果的 去重
    for ik, iv in resultDict.items():
        ll = list(iv)
        ll.sort(cmp=gid_cmp)
        filter['|'.join(ll)] = 0

    # 选择合适的输出
    outGid = {}
    for ik, iv in filter.items():
        arr = ik.split('|')
        chargeGid = ("", 0)
        freeGid = ("", 0)
        for gid in arr:
            if not ii.has_key(gid):
                continue
            feeFlagt, viewCountt, namet, authort, seriest = ii[gid]
            if int(feeFlagt) == 1:
                tgid, tv = chargeGid
                if tv <= int(viewCountt):
                    chargeGid = (gid, int(viewCountt))
            else:
                fgid, fv = freeGid
                if fv <= int(viewCountt):
                    freeGid = (gid, int(viewCountt))
        if chargeGid[0] != '':
            for gid in arr:
                if outGid.has_key(gid):
                    continue
                outGid[gid] = 0
                feeFlagt, viewCountt, namet, authort, seriest = ii[chargeGid[0]]
                fw.write(gid + "\t" + namet + "\t" + authort + "\t" + seriest + "\n")
        elif freeGid[0] != '':
            for gid in arr:
                if outGid.has_key(gid):
                    continue
                outGid[gid] = 0
                feeFlagt, viewCountt, namet, authort, seriest = ii[freeGid[0]]
                fw.write(gid + "\t" + namet + "\t" + authort + "\t" + seriest + "\n")
        else:
            print ('错误的gid: ' + '-------->')
    # 输出未成对的
    for ik, iv in ii.items():
        if outGid.has_key(ik):
            continue
        outGid[ik] = 0
        feeFlagt, viewCountt, name, author, series = iv
        fw.write(ik + "\t" + name + "\t" + author + "\t" + series + "\n")
    fw.close()


if __name__ == '__main__':

    rulePath = sys.argv[1]
    simPath = sys.argv[2]
    outPath = sys.argv[3] + '_debug'

    ruleDict = {}
    simDict = {}
    resultDict = {}

    read_rule_result(rulePath, ruleDict)
    print ("规则结果读取完成")


    read_sim_result(simPath, simDict)
    print ("相似结果读取完成")
    union_sim_rule(simDict, ruleDict, resultDict)

    print ("相似和规则组合完成")
    del ruleDict
    del simDict

    # 结果整合
    out_result(rulePath, resultDict, outPath)
    print ("最终结果输出完成")







    pass
