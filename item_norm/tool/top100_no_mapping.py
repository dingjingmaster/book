#!/usr/bin/env python
#-*- encoding=utf8 -*-


if __name__ == '__main__':

    freeTop100 = "./free_top500.txt"
    freeNoMapping = './free_no_mapping.txt'
    chargeTop100 = "./charge_top500.txt"
    chargeNoMapping = './charge_no_mapping.txt'
    normResult = "../resource/finally_result.txt"

    normDict = {}

    fwf = open(freeNoMapping, 'w')
    fwc = open(chargeNoMapping, 'w')
    with open(normResult, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            gid = arr[0]
            name = arr[1]
            author = arr[2]

            key = name + '|' + author
            if not normDict.has_key(key):
                s = set()
                s.add(gid)
                normDict[key] = s
            else:
                s = normDict[key]
                s.add(gid)
                normDict[key] = s

    with open(freeTop100, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            gid = arr[0]
            name = arr[1]
            author = arr[2]
            key = name + '|' + author

            if normDict.has_key(key):
                continue
            fwf.write(gid + '\t' + name + '\t' + author + '\n')

    with open(chargeTop100, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            gid = arr[0]
            name = arr[1]
            author = arr[2]
            key = name + '|' + author

            if normDict.has_key(key):
                continue
            fwc.write(gid + '\t' + name + '\t' + author + '\n')
    fwf.close()
    fwc.close()





