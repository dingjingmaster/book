#!/bin/env python
#encoding "utf8"
import re
import sys
reload(sys)
sys.setdefaultencoding("utf8")

def write_file(path, mdict):
    fWrite = open(path, "w")
    for i in mdict.items():
        fWrite.write(str(i[0]) + "\t" + str(i[1]) + "\n")
    fWrite.close()
    return None

def read_res_dict(path, mdict):
    fRead = open(path, "r")
    for i in fRead.readlines():
        i = i.strip("\n")
        temp = ""
        # gid, normName, normAuthor
        arr = i.split("\t")
        if(len(arr) != 6):
            continue
        if not mdict.has_key(arr[0]) and arr[1] != arr[4]:
            tmp = arr[1]
            l2 = len(tmp)
            l1 = len(tmp.replace(arr[2], ''))
            if l1 != l2:
                continue
            mdict[arr[0]] = arr[1] + "\t" + arr[2] + "\t" + arr[4] + "\t" + arr[5]
        else:
            continue
    fRead.close()
    return


if __name__ == '__main__':

    if len(sys.argv) != 2:
        exit(-1)

    spath = sys.argv[1]
    save = "./res.txt"

    mdict = {}

    read_res_dict(spath, mdict)
    write_file(save, mdict)






