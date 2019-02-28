#!/bin/env python
#encoding "utf8"
import sys
reload(sys)
sys.setdefaultencoding("utf8")

def write_file(path, mdict):
    fWrite = open(path, "w")
    for i in mdict.items():
        fWrite.write(str(i[0]) + "\t" + str(i[1]) + "\n")
    fWrite.close()
    return None

def check_data(hdict, ndict, resDict):
    a = 0
    for i in hdict.items():
        if not resDict.has_key(i[0]):
            a += 1
            if  (ndict.has_key(i[0])) and (i[1] != ndict[i[0]]):
                resDict[i[0]] = i[1] + "\t----->\t" + ndict[i[0]]
    print "checked: " + str(a) + "data"
    return None

def w_data(hdict, ndict, wdict):
    for i in hdict.items():
        if not wdict.has_key(i[0]):
            if  (ndict.has_key(i[0])) and (i[1] != ndict[i[0]]):
                wdict[i[0]] = i[1].replace("\t", "{]")
    return None


def read_res_dict(path, mdict):
    fRead = open(path, "r")
    for i in fRead.readlines():
        i = i.strip("\n")
        # gid, normName, normAuthor
        arr = i.split("\t")
        if(len(arr) != 4):
            continue
        if not mdict.has_key(arr[0]):
            mdict[arr[0]] = arr[1] + "\t" + arr[2]
        else:
            continue
    fRead.close()
    return




def read_src_dict(path, mdict):
    fRead = open(path, "r")
    for i in fRead.readlines():
        i = i.strip("\n")
        # gid, normName, normAuthor
        arr = i.split("\t")
        if(len(arr) != 5):
            continue
        if not mdict.has_key(arr[0]):
            mdict[arr[0]] = arr[2] + "\t" + arr[4]
        else:
            continue
    fRead.close()
    return



if __name__ == '__main__':

    if len(sys.argv) != 3:
        exit(-1)

    srcPath = sys.argv[1]
    myPath = sys.argv[2]

    savePath = "diff_src_my.txt"
    wp = "w_p.txt"

    src_dict = {}
    my_dict = {}

    res_dict = {}
    w_dict = {}

    read_src_dict(srcPath, src_dict)
    read_res_dict(myPath, my_dict)
    check_data(src_dict, my_dict, res_dict)
    w_data(src_dict, my_dict, w_dict)
    write_file(savePath, res_dict)
    write_file(wp, w_dict)



