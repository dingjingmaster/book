#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")


#################################    共有    ####################################
# 解析获取的hadoop信息
def parse_info(logPath, logList):
    gid = ""
    name = ""
    author = ""
    maskLevel = ""
    feeFlag = ""
    by = ""
    tf = ""
    ncp = ""
    fc = ""
    userNum = ""
    chapterNum = ""
    bysByuUserNum = ""
    bysByuChapterNum = ""
    bysFbyuUserNum = ""
    bysFbyuChapterNum = ""
    fR = open(logPath, "r")
    for line in fR.readlines():
        line = line.strip()
        arr = line.split("\t")
        gid = arr[0]
        name = arr[1]
        author = arr[2]
        maskLevel = arr[3]
        feeFlag = arr[4]
        by = arr[5]
        tf = arr[6]
        ncp = arr[7]
        fc = arr[8]
        userNum = arr[9]
        chapterNum = arr[10]
        bysByuUserNum = arr[11]
        bysByuChapterNum = arr[12]
        bysFbyuUserNum = arr[13]
        bysFbyuChapterNum = arr[14]
        logList.append((gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum))
    return logList


# 开始
def mask_level_list(logList, ifmaskList):
    maskBookNum = 0
    maskBookUserNum = 0             # 购买用户数
    maskChargeChapterNum = 0        # 章节购买量
    unmaskBookNum = 0
    unmaskBookUserNum = 0
    unmaskChargeChapterNum = 0
    allBookNum = 0
    allBookUserNum = 0
    allChargeChapterNum = 0
    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        allBookNum += 1
        allBookUserNum += int(usernumTemp)
        allChargeChapterNum += int(userChargeTemp)
        if maskLevel == u'1':
            maskBookNum += 1
            maskBookUserNum += int(usernumTemp)
            maskChargeChapterNum += int(userChargeTemp)
        elif maskLevel == u'0':
            unmaskBookNum += 1
            unmaskBookUserNum += int(usernumTemp)
            unmaskChargeChapterNum += int(userChargeTemp)
    if allBookNum == 0:
        allBookNum = 1
    if allBookUserNum == 0:
        allBookUserNum = 1
    if allChargeChapterNum == 0:
        allChargeChapterNum = 1
    # 输出(屏蔽否， 书籍量， 购买量， 购买章节)
    ifmaskList.append(("屏蔽书", maskBookNum, float(maskBookNum)/allBookNum * 100\
            , maskBookUserNum, float(maskBookUserNum)/allBookUserNum * 100\
            , maskChargeChapterNum, float(maskChargeChapterNum)/allChargeChapterNum * 100))
    ifmaskList.append(("非屏蔽书", unmaskBookNum, float(unmaskBookNum)/allBookNum * 100\
            , unmaskBookUserNum, float(unmaskBookUserNum)/allBookUserNum * 100\
            , unmaskChargeChapterNum, float(unmaskChargeChapterNum)/allChargeChapterNum * 100))
    ifmaskList.append(("总计", allBookNum, 100, allBookUserNum, 100, allChargeChapterNum, 100))
    return ifmaskList


# 天阅读-非屏蔽互联网书 与 付费书情况
def unmask_fee_charge(logList, unmaskFeeList):
    unmaskBookFree = 0              # 非屏蔽互联网书的量
    unmaskBookUserFree = 0          # 非屏蔽互联网用户量
    unmaskBookChapterFree = 0       # 非屏蔽互联网章节量

    unmaskBookCharge = 0            # 非屏蔽 cp正版书 书籍量
    unmaskBookUserCharge = 0        # 非屏蔽 cp正版书 用户量
    unmaskBookChapterCharge = 0     # 非屏蔽 cp正版书 章节量

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if maskLevel != u'1':
            if feeFlag == u'1':
                allBook += 1
                allBookUser += int(usernumTemp)
                allBookChapter += int(userChargeTemp)
                
                unmaskBookCharge += 1
                unmaskBookUserCharge += int(usernumTemp)
                unmaskBookChapterCharge += int(userChargeTemp)
            elif feeFlag != u'1':
                allBook += 1
                allBookUser += int(usernumTemp)
                allBookChapter += int(userChargeTemp)
                
                unmaskBookFree += 1
                unmaskBookUserFree += int(usernumTemp)
                unmaskBookChapterFree += int(userChargeTemp)
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    unmaskFeeList.append(("cp正版书", unmaskBookFree, float(unmaskBookFree)/allBook * 100\
            , unmaskBookUserFree, float(unmaskBookUserFree)/allBookUser * 100\
            , unmaskBookChapterFree, float(unmaskBookChapterFree)/allBookChapter * 100))
    unmaskFeeList.append(("互联网书", unmaskBookCharge, float(unmaskBookCharge)/allBook * 100\
            , unmaskBookUserCharge, float(unmaskBookUserCharge)/allBookUser * 100\
            , unmaskBookChapterCharge, float(unmaskBookChapterCharge)/allBookChapter * 100))
    return unmaskFeeList


# 天阅读-非屏蔽正版书 与 付费情况
def unmask_charge_info(logList, unmaskFeeList):
    unmaskBookCharge = 0            # 非屏蔽 cp正版书 书籍量
    unmaskBookUserCharge = 0        # 非屏蔽 cp正版书 用户量
    unmaskBookChapterCharge = 0     # 非屏蔽 cp正版书 章节量

    unmaskByBookCharge = 0          # 非屏蔽 包月书 书籍量
    unmaskByBookUserCharge = 0      # 非屏蔽 包月书 用户量
    unmaskByBookChapterCharge = 0   # 非屏蔽 包月书 章节量

    unmaskTfBookCharge = 0          # 非屏蔽 限免书 书籍量
    unmaskTfBookUserCharge = 0      # 非屏蔽 限免书 用户量
    unmaskTfBookChapterCharge = 0   # 非屏蔽 限免书 章节量

    unmaskFcBookCharge = 0          # 非屏蔽 按章付费书 书籍量
    unmaskFcBookUserCharge = 0      # 非屏蔽 按章付费书 用户量
    unmaskFcBookChapterCharge = 0   # 非屏蔽 按章付费书 章节量

    unmaskOBookCharge = 0          # 非屏蔽 全免书 书籍量
    unmaskOBookUserCharge = 0      # 非屏蔽 全免书 用户量
    unmaskOBookChapterCharge = 0   # 非屏蔽 全免书 章节量

    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc \
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if maskLevel != u'1' and feeFlag == u'1':
            unmaskBookCharge += 1
            unmaskBookUserCharge += usernumTemp
            unmaskBookChapterCharge += userChargeTemp
            # 包月
            if by != u'000':
                unmaskByBookCharge += 1
                unmaskByBookUserCharge += int(usernumTemp)
                unmaskByBookChapterCharge += int(userChargeTemp)
            # 限免
            elif tf != u'000':
                unmaskTfBookCharge += 1
                unmaskTfBookUserCharge += int(usernumTemp)
                unmaskTfBookChapterCharge += int(userChargeTemp)
            # 按章付费
            elif fc != u'000':
                unmaskFcBookCharge += 1
                unmaskFcBookUserCharge += int(usernumTemp)
                unmaskFcBookChapterCharge += int(userChargeTemp)
            else:
                unmaskOBookCharge += 1
                unmaskOBookUserCharge += int(usernumTemp)
                unmaskOBookChapterCharge += int(userChargeTemp)
    if unmaskBookCharge == 0:
        unmaskBookCharge = 1
    if unmaskBookUserCharge == 0:
        unmaskBookUserCharge = 1
    if unmaskBookChapterCharge == 0:
        unmaskBookChapterCharge = 1
    unmaskFeeList.append(("包月书", unmaskByBookCharge, float(unmaskByBookCharge)/unmaskBookCharge * 100\
                              , unmaskByBookUserCharge, float(unmaskByBookUserCharge)/unmaskBookUserCharge * 100\
                              , unmaskByBookChapterCharge, float(unmaskByBookChapterCharge)/unmaskBookChapterCharge * 100))
    unmaskFeeList.append(("限免书", unmaskTfBookCharge, float(unmaskTfBookCharge) / unmaskBookCharge * 100 \
                              , unmaskTfBookUserCharge, float(unmaskTfBookUserCharge) / unmaskBookUserCharge * 100 \
                              , unmaskTfBookChapterCharge, float(unmaskTfBookChapterCharge) / unmaskBookChapterCharge * 100))
    unmaskFeeList.append(("按章付费书", unmaskFcBookCharge, float(unmaskFcBookCharge) / unmaskBookCharge * 100 \
                              , unmaskFcBookUserCharge, float(unmaskFcBookUserCharge) / unmaskBookUserCharge * 100 \
                              , unmaskFcBookChapterCharge, float(unmaskFcBookChapterCharge) / unmaskBookChapterCharge * 100))
    unmaskFeeList.append(("其它(付费书免费读)", unmaskOBookCharge, float(unmaskOBookCharge) / unmaskBookCharge * 100 \
                              , unmaskOBookUserCharge, float(unmaskOBookUserCharge) / unmaskBookUserCharge * 100 \
                              , unmaskOBookChapterCharge, float(unmaskOBookChapterCharge) / unmaskBookChapterCharge * 100))
    return unmaskFeeList


# 天阅读-屏蔽书情况
def mask_fee_flag(logList, maskFeeList):
    maskBookFree = 0            # 屏蔽免费书的量
    maskBookUserFree = 0        # 屏蔽免费用户量
    maskBookChapterFree = 0     # 屏蔽免费章节量

    maskBookCharge = 0
    maskBookUserCharge = 0
    maskBookChapterCharge = 0

    maskBookMonthus = 0         # 包月用户包月书
    maskBookUserMonthus = 0
    maskBookChapterMonthus = 0

    maskBookMonth = 0           # 包月书非包月用户
    maskBookUserMonth = 0
    maskBookChapterMonth = 0

    maskBookPublic = 0
    maskBookUserPublic = 0
    maskBookChapterPublic = 0

    maskBooktf = 0
    maskBookUsertf = 0
    maskBookChaptertf = 0

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if maskLevel == u'1':
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)
            if int(bysByuUserNum) > 0 and int(bysFbyuUserNum) > 0:
                allBook += 1
            if tf != "000":
                maskBooktf += 1
                maskBookUsertf += int(usernumTemp)
                maskBookChaptertf += int(userChargeTemp)
            elif by != "000" and tf == "000":
                if int(bysByuUserNum) > 0:
                    maskBookMonthus += 1
                    maskBookUserMonthus += int(bysByuUserNum)
                    maskBookChapterMonthus += int(bysByuChapterNum)
                if int(bysFbyuUserNum) > 0:
                    maskBookMonth += 1
                    maskBookUserMonth += int(bysFbyuUserNum)
                    maskBookChapterMonth += int(bysFbyuChapterNum)
            elif feeFlag == "0":      # 免费
                maskBookFree += 1
                maskBookUserFree += int(usernumTemp)
                maskBookChapterFree += int(userChargeTemp)
            elif feeFlag == "1":    # 付费
                maskBookCharge += 1
                maskBookUserCharge += int(usernumTemp)
                maskBookChapterCharge += int(userChargeTemp)
            elif feeFlag == "10":
                maskBookPublic += 1
                maskBookUserPublic += int(usernumTemp)
                maskBookChapterPublic += int(userChargeTemp)
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    maskFeeList.append(("限免书", maskBooktf, float(maskBooktf)/allBook * 100\
            , maskBookUsertf, float(maskBookUsertf)/allBookUser * 100\
            , maskBookChaptertf, float(maskBookChaptertf)/allBookChapter * 100))
    maskFeeList.append(("免费书", maskBookFree, float(maskBookFree)/allBook * 100\
            , maskBookUserFree, float(maskBookUserFree)/allBookUser * 100\
            , maskBookChapterFree, float(maskBookChapterFree)/allBookChapter * 100))
    maskFeeList.append(("付费书", maskBookCharge, float(maskBookCharge)/allBook * 100\
            , maskBookUserCharge, float(maskBookUserCharge)/allBookUser * 100\
            , maskBookChapterCharge, float(maskBookChapterCharge)/allBookChapter * 100))
    maskFeeList.append(("包月书（包月用户读）", maskBookMonthus, float(maskBookMonthus)/allBook * 100\
            , maskBookUserMonthus, float(maskBookUserMonthus)/allBookUser * 100\
            , maskBookChapterMonthus, float(maskBookChapterMonthus)/allBookChapter * 100))
    maskFeeList.append(("包月书（非包月用户读）", maskBookMonth, float(maskBookMonth)/allBook * 100\
            , maskBookUserMonth, float(maskBookUserMonth)/allBookUser * 100\
            , maskBookChapterMonth, float(maskBookChapterMonth)/allBookChapter * 100))
    maskFeeList.append(("公版", maskBookPublic, float(maskBookPublic)/allBook * 100\
            , maskBookUserPublic, float(maskBookUserPublic)/allBookUser * 100\
            , maskBookChapterPublic, float(maskBookChapterPublic)/allBookChapter * 100))
    return maskFeeList


# 天阅读-非屏蔽书情况
def unmask_fee_flag(logList, unmaskFeeList):
    unmaskBookFree = 0            # 屏蔽免费书的量
    unmaskBookUserFree = 0        # 屏蔽免费用户量
    unmaskBookChapterFree = 0     # 屏蔽免费章节量

    unmaskBookCharge = 0
    unmaskBookUserCharge = 0
    unmaskBookChapterCharge = 0

    unmaskBookMonthus = 0         # 包月用户包月书
    unmaskBookUserMonthus = 0
    unmaskBookChapterMonthus = 0

    unmaskBookMonth = 0           # 包月书非包月用户
    unmaskBookUserMonth = 0
    unmaskBookChapterMonth = 0

    unmaskBookPublic = 0
    unmaskBookUserPublic = 0
    unmaskBookChapterPublic = 0

    unmaskBooktf = 0
    unmaskBookUsertf = 0
    unmaskBookChaptertf = 0

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if maskLevel != u'1':
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)
            if int(bysByuUserNum) > 0 and int(bysFbyuUserNum) > 0:
                allBook += 1
            if tf != u'000' and by == u'000':
                unmaskBooktf += 1
                unmaskBookUsertf += int(usernumTemp)
                unmaskBookChaptertf += int(userChargeTemp)
            elif by != u'000' and tf == u'000':       # 包月
                if int(bysByuUserNum) > 0:
                    unmaskBookMonthus += 1
                    unmaskBookUserMonthus += int(bysByuUserNum)
                    unmaskBookChapterMonthus += int(bysByuChapterNum)
                if int(bysFbyuUserNum) > 0:
                    unmaskBookMonth += 1
                    unmaskBookUserMonth += int(bysFbyuUserNum)
                    unmaskBookChapterMonth += int(bysFbyuChapterNum)
            elif feeFlag == u'10':
                unmaskBookPublic += 1
                unmaskBookUserPublic += int(usernumTemp)
                unmaskBookChapterPublic += int(userChargeTemp)
            elif feeFlag == u'1':    # 付费
                unmaskBookCharge += 1
                unmaskBookUserCharge += int(usernumTemp)
                unmaskBookChapterCharge += int(userChargeTemp)
            elif feeFlag == u'0':                   # 免费
                unmaskBookFree += 1
                unmaskBookUserFree += int(usernumTemp)
                unmaskBookChapterFree += int(userChargeTemp)
            else:
                print gid
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    unmaskFeeList.append(("限免书", unmaskBooktf, float(unmaskBooktf)/allBook * 100\
            , unmaskBookUsertf, float(unmaskBookUsertf)/allBookUser * 100\
            , unmaskBookChaptertf, float(unmaskBookChaptertf)/allBookChapter * 100))
    unmaskFeeList.append(("免费书", unmaskBookFree, float(unmaskBookFree)/allBook * 100\
            , unmaskBookUserFree, float(unmaskBookUserFree)/allBookUser * 100\
            , unmaskBookChapterFree, float(unmaskBookChapterFree)/allBookChapter * 100))
    unmaskFeeList.append(("付费书", unmaskBookCharge, float(unmaskBookCharge)/allBook * 100\
            , unmaskBookUserCharge, float(unmaskBookUserCharge)/allBookUser * 100\
            , unmaskBookChapterCharge, float(unmaskBookChapterCharge)/allBookChapter * 100))
    unmaskFeeList.append(("包月书（包月用户读）", unmaskBookMonthus, float(unmaskBookMonthus)/allBook * 100\
            , unmaskBookUserMonthus, float(unmaskBookUserMonthus)/allBookUser * 100\
            , unmaskBookChapterMonthus, float(unmaskBookChapterMonthus)/allBookChapter * 100))
    unmaskFeeList.append(("包月书（非包月用户读）", unmaskBookMonth, float(unmaskBookMonth)/allBook * 100\
            , unmaskBookUserMonth, float(unmaskBookUserMonth)/allBookUser * 100\
            , unmaskBookChapterMonth, float(unmaskBookChapterMonth)/allBookChapter * 100))
    unmaskFeeList.append(("公版书", unmaskBookPublic, float(unmaskBookPublic)/allBook * 100\
            , unmaskBookUserPublic, float(unmaskBookUserPublic)/allBookUser * 100\
            , unmaskBookChapterPublic, float(unmaskBookChapterPublic)/allBookChapter * 100))
    return unmaskFeeList


# 天阅读-cp正版书籍阅读分段
def true_charge__num(loglist, truechargelist):
    truechargebt0t10b = 0                   # 书籍数
    truechargebt10t100b = 0
    truechargebt100t1000b = 0
    truechargebt1000t10000b = 0
    truechargegt10000b = 0
    truechargebt0t10u = 0                   # 用户数
    truechargebt10t100u = 0
    truechargebt100t1000u = 0
    truechargebt1000t10000u = 0
    truechargegt10000u = 0
    truechargebt0t10c = 0                   # 付费章节
    truechargebt10t100c = 0
    truechargebt100t1000c = 0
    truechargebt1000t10000c = 0
    truechargegt10000c = 0

    allbook = 0
    allbookuser = 0
    allbookchapter = 0

    for i in loglist:
        gid, name, author, masklevel, feeflag, by, tf, ncp, fc\
                , usernum, chapternum\
                , bysbyuusernum, bysbyuchapternum\
                , bysfbyuusernum, bysfbyuchapternum = i
        usernumtemp = int(usernum) + int(bysbyuusernum) + int(bysfbyuusernum)
        usertruechargetemp = int(chapternum) + int(bysbyuchapternum) + int(bysfbyuchapternum)
        if feeflag == u'1':
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(usertruechargetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                truechargebt0t10b += 1
                truechargebt0t10u += int(usernumtemp)
                truechargebt0t10c += int(usertruechargetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                truechargebt10t100b += 1
                truechargebt10t100u += int(usernumtemp)
                truechargebt10t100c += int(usertruechargetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                truechargebt100t1000b += 1
                truechargebt100t1000u += int(usernumtemp)
                truechargebt100t1000c += int(usertruechargetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                truechargebt1000t10000b += 1
                truechargebt1000t10000u += int(usernumtemp)
                truechargebt1000t10000c += int(usertruechargetemp)
            else:
                truechargegt10000b += 1
                truechargegt10000u += int(usernumtemp)
                truechargegt10000c += int(usertruechargetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    truechargelist.append(("(0,10)", truechargebt0t10b, float(truechargebt0t10b)/allbook * 100\
            , truechargebt0t10u, float(truechargebt0t10u)/allbookuser * 100\
            , truechargebt0t10c, float(truechargebt0t10c)/allbookchapter * 100))
    truechargelist.append(("[10,100)", truechargebt10t100b, float(truechargebt10t100b)/allbook * 100\
            , truechargebt10t100u, float(truechargebt10t100u)/allbookuser * 100\
            , truechargebt10t100c, float(truechargebt10t100c)/allbookchapter * 100))
    truechargelist.append(("[100,1000)", truechargebt100t1000b, float(truechargebt100t1000b)/allbook * 100\
            , truechargebt100t1000u, float(truechargebt100t1000u)/allbookuser * 100\
            , truechargebt100t1000c, float(truechargebt100t1000c)/allbookchapter * 100))
    truechargelist.append(("[1000,10000)", truechargebt1000t10000b, float(truechargebt1000t10000b)/allbook * 100\
            , truechargebt1000t10000u, float(truechargebt1000t10000u)/allbookuser * 100\
            , truechargebt1000t10000c, float(truechargebt1000t10000c)/allbookchapter * 100))
    truechargelist.append(("[10000, ...)", truechargegt10000b, float(truechargegt10000b)/allbook * 100\
            , truechargegt10000u, float(truechargegt10000u)/allbookuser * 100\
            , truechargegt10000c, float(truechargegt10000c)/allbookchapter * 100))
    return truechargelist


def tf_num(logList, tfList):
    tfBt0t10b = 0                   # 书籍数
    tfBt10t100b = 0
    tfBt100t1000b = 0
    tfBt1000t10000b = 0
    tfgt10000b = 0
    tfBt0t10u = 0                   # 用户数
    tfBt10t100u = 0
    tfBt100t1000u = 0
    tfBt1000t10000u = 0
    tfgt10000u = 0
    tfBt0t10c = 0                   # 付费章节
    tfBt10t100c = 0
    tfBt100t1000c = 0
    tfBt1000t10000c = 0
    tfgt10000c = 0

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if tf != u'000' and tf != u'' and tf != u'0':
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)
            if int(usernumTemp) > 0 and int(usernumTemp) < 10:
                tfBt0t10b += 1
                tfBt0t10u += int(usernumTemp)
                tfBt0t10c += int(userChargeTemp)
            elif int(usernumTemp) >= 10 and int(usernumTemp) < 100:
                tfBt10t100b += 1
                tfBt10t100u += int(usernumTemp)
                tfBt10t100c += int(userChargeTemp)
            elif int(usernumTemp) >= 100 and int(usernumTemp) < 1000:
                tfBt100t1000b += 1
                tfBt100t1000u += int(usernumTemp)
                tfBt100t1000c += int(userChargeTemp)
            elif int(usernumTemp) >= 1000 and int(usernumTemp) < 10000:
                tfBt1000t10000b += 1
                tfBt1000t10000u += int(usernumTemp)
                tfBt1000t10000c += int(userChargeTemp)
            elif int(usernumTemp) >= 10000:
                tfgt10000b += 1
                tfgt10000u += int(usernumTemp)
                tfgt10000c += int(userChargeTemp)
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    tfList.append(("[0,10)", tfBt0t10b, float(tfBt0t10b)/allBook * 100\
            , tfBt0t10u, float(tfBt0t10u)/allBookUser * 100\
            , tfBt0t10c, float(tfBt0t10c)/allBookChapter * 100))
    tfList.append(("[10,100)", tfBt10t100b, float(tfBt10t100b)/allBook * 100\
            , tfBt10t100u, float(tfBt10t100u)/allBookUser * 100\
            , tfBt10t100c, float(tfBt10t100c)/allBookChapter * 100))
    tfList.append(("[100,1000)", tfBt100t1000b, float(tfBt100t1000b)/allBook * 100\
            , tfBt100t1000u, float(tfBt100t1000u)/allBookUser * 100\
            , tfBt100t1000c, float(tfBt100t1000c)/allBookChapter * 100))
    tfList.append(("[1000,10000)", tfBt1000t10000b, float(tfBt1000t10000b)/allBook * 100\
            , tfBt1000t10000u, float(tfBt1000t10000u)/allBookUser * 100\
            , tfBt1000t10000c, float(tfBt1000t10000c)/allBookChapter * 100))
    tfList.append(("[10000, ...)", tfgt10000b, float(tfgt10000b)/allBook * 100\
            , tfgt10000u, float(tfgt10000u)/allBookUser * 100\
            , tfgt10000c, float(tfgt10000c)/allBookChapter * 100))
    return tfList


def month_num(logList, bysbyuList, bysfbyuList, monthList):
    bysbyuBt0t10b = 0                   # 书籍数
    bysbyuBt10t100b = 0
    bysbyuBt100t1000b = 0
    bysbyuBt1000t10000b = 0
    bysbyugt10000b = 0

    bysbyuBt0t10u = 0                   # 用户数
    bysbyuBt10t100u = 0
    bysbyuBt100t1000u = 0
    bysbyuBt1000t10000u = 0
    bysbyugt10000u = 0

    bysbyuBt0t10c = 0                   # 付费章节
    bysbyuBt10t100c = 0
    bysbyuBt100t1000c = 0
    bysbyuBt1000t10000c = 0
    bysbyugt10000c = 0

    bysfbyuBt0t10b = 0
    bysfbyuBt10t100b = 0
    bysfbyuBt100t1000b = 0
    bysfbyuBt1000t10000b = 0
    bysfbyugt10000b = 0

    bysfbyuBt0t10u = 0
    bysfbyuBt10t100u = 0
    bysfbyuBt100t1000u = 0
    bysfbyuBt1000t10000u = 0
    bysfbyugt10000u = 0

    bysfbyuBt0t10c = 0
    bysfbyuBt10t100c = 0
    bysfbyuBt100t1000c = 0
    bysfbyuBt1000t10000c = 0
    bysfbyugt10000c = 0

    monthBt0t10b = 0                   # 书籍数
    monthBt10t100b = 0
    monthBt100t1000b = 0
    monthBt1000t10000b = 0
    monthgt10000b = 0

    monthBt0t10u = 0                   # 用户数
    monthBt10t100u = 0
    monthBt100t1000u = 0
    monthBt1000t10000u = 0
    monthgt10000u = 0

    monthBt0t10c = 0                   # 付费章节
    monthBt10t100c = 0
    monthBt100t1000c = 0
    monthBt1000t10000c = 0
    monthgt10000c = 0

    allbyusbook = 0
    allbyusbookuser = 0
    allbyusbookchapter = 0

    allbyufsbook = 0
    allbyufsbookuser = 0
    allbyufsbookchapter = 0
    
    for i in logList:
        gid, name, author, masklevel, feeflag, by, tf, ncp, fc\
                , usernum, chapternum\
                , bysbyuusernum, bysbyuchapternum\
                , bysfbyuusernum, bysfbyuchapternum = i
        monthusernumtemp = int(bysbyuusernum) + int(bysfbyuusernum)
        monthchapternumtemp = int(bysbyuchapternum) + int(bysfbyuchapternum)
        #
        if by != u'000' and tf == u'000':

            if int(bysbyuusernum) >= 0 and int(bysbyuusernum) < 10:
                bysbyuBt0t10b += 1
                bysbyuBt0t10u += int(bysbyuusernum)
                bysbyuBt0t10c += int(bysbyuchapternum)
                allbyusbook += 1
                allbyusbookuser += int(bysbyuusernum)
                allbyusbookchapter += int(bysbyuchapternum)
            elif int(bysbyuusernum) >= 10 and int(bysbyuusernum) < 100:
                bysbyuBt10t100b += 1
                bysbyuBt10t100u += int(bysbyuusernum)
                bysbyuBt10t100c += int(bysbyuchapternum)
                allbyusbook += 1
                allbyusbookuser += int(bysbyuusernum)
                allbyusbookchapter += int(bysbyuchapternum)
            elif int(bysbyuusernum) >= 100 and int(bysbyuusernum) < 1000:
                bysbyuBt100t1000b += 1
                bysbyuBt100t1000u += int(bysbyuusernum)
                bysbyuBt100t1000c += int(bysbyuchapternum)
                allbyusbook += 1
                allbyusbookuser += int(bysbyuusernum)
                allbyusbookchapter += int(bysbyuchapternum)
            elif int(bysbyuusernum) >= 1000 and int(bysbyuusernum) < 10000:
                bysbyuBt1000t10000b += 1
                bysbyuBt1000t10000u += int(bysbyuusernum)
                bysbyuBt1000t10000c += int(bysbyuchapternum)
                allbyusbook += 1
                allbyusbookuser += int(bysbyuusernum)
                allbyusbookchapter += int(bysbyuchapternum)
            else:
                bysbyugt10000b += 1
                bysbyugt10000u += int(bysbyuusernum)
                bysbyugt10000c += int(bysbyuchapternum)
                allbyusbook += 1
                allbyusbookuser += int(bysbyuusernum)
                allbyusbookchapter += int(bysbyuchapternum)

            if int(bysfbyuusernum) >= 0 and int(bysfbyuusernum) < 10:
                bysfbyuBt0t10b += 1
                bysfbyuBt0t10u += int(bysfbyuusernum)
                bysfbyuBt0t10c += int(bysfbyuchapternum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysfbyuusernum)
                allbyufsbookchapter += int(bysfbyuchapternum)
            elif int(bysfbyuusernum) >= 10 and int(bysfbyuusernum) < 100:
                bysfbyuBt10t100b += 1
                bysfbyuBt10t100u += int(bysfbyuusernum)
                bysfbyuBt10t100c += int(bysfbyuchapternum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysfbyuusernum)
                allbyufsbookchapter += int(bysfbyuchapternum)
            elif int(bysfbyuusernum) >= 100 and int(bysfbyuusernum) < 1000:
                bysfbyuBt100t1000b += 1
                bysfbyuBt100t1000u += int(bysfbyuusernum)
                bysfbyuBt100t1000c += int(bysfbyuchapternum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysfbyuusernum)
                allbyufsbookchapter += int(bysfbyuchapternum)
            elif int(bysfbyuusernum) >= 1000 and int(bysfbyuusernum) < 10000:
                bysfbyuBt1000t10000b += 1
                bysfbyuBt1000t10000u += int(bysfbyuusernum)
                bysfbyuBt1000t10000c += int(bysfbyuchapternum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysfbyuusernum)
                allbyufsbookchapter += int(bysfbyuchapternum)
            else:
                bysfbyugt10000b += 1
                bysfbyugt10000u += int(bysfbyuusernum)
                bysfbyugt10000c += int(bysfbyuchapternum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysfbyuusernum)
                allbyufsbookchapter += int(bysfbyuchapternum)

    if allbyusbook == 0:
        allbyusbook = 1
    if allbyusbookuser == 0:
        allbyusbookuser = 1
    if allbyusbookchapter == 0:
        allbyusbookchapter = 1
    if allbyufsbook == 0:
        allbyufsbook = 1
    if allbyufsbookuser == 0:
        allbyufsbookuser = 1
    if allbyufsbookchapter == 0:
        allbyufsbookchapter = 1

    bysbyuList.append(("(0,10)", bysbyuBt0t10b, float(bysbyuBt0t10b)/allbyusbook * 100\
            , bysbyuBt0t10u, float(bysbyuBt0t10u)/allbyusbookuser * 100\
            , bysbyuBt0t10c, float(bysbyuBt0t10c)/allbyusbookchapter * 100))
    bysbyuList.append(("[10,100)", bysbyuBt10t100b, float(bysbyuBt10t100b)/allbyusbook * 100\
            , bysbyuBt10t100u, float(bysbyuBt10t100u)/allbyusbookuser * 100\
            , bysbyuBt10t100c, float(bysbyuBt10t100c)/allbyusbookchapter * 100))
    bysbyuList.append(("[100,1000)", bysbyuBt100t1000b, float(bysbyuBt100t1000b)/allbyusbook * 100\
            , bysbyuBt100t1000u, float(bysbyuBt100t1000u)/allbyusbookuser * 100\
            , bysbyuBt100t1000c, float(bysbyuBt100t1000c)/allbyusbookchapter * 100))
    bysbyuList.append(("[1000,10000)", bysbyuBt1000t10000b, float(bysbyuBt1000t10000b)/allbyusbook * 100\
            , bysbyuBt1000t10000u, float(bysbyuBt1000t10000u)/allbyusbookuser * 100\
            , bysbyuBt1000t10000c, float(bysbyuBt1000t10000c)/allbyusbookchapter * 100))
    bysbyuList.append(("[10000, ...)", bysbyugt10000b, float(bysbyugt10000b)/allbyusbook * 100\
            , bysbyugt10000u, float(bysbyugt10000u)/allbyusbookuser * 100\
            , bysbyugt10000c, float(bysbyugt10000c)/allbyusbookchapter * 100))

    bysfbyuList.append(("[0,10)", bysfbyuBt0t10b, float(bysfbyuBt0t10b)/allbyufsbook * 100\
            , bysfbyuBt0t10u, float(bysfbyuBt0t10u)/allbyufsbookuser * 100\
            , bysfbyuBt0t10c, float(bysfbyuBt0t10c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[10,100)", bysfbyuBt10t100b, float(bysfbyuBt10t100b)/allbyufsbook * 100\
            , bysfbyuBt10t100u, float(bysfbyuBt10t100u)/allbyufsbookuser * 100\
            , bysfbyuBt10t100c, float(bysfbyuBt10t100c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[100,1000)", bysfbyuBt100t1000b, float(bysfbyuBt100t1000b)/allbyufsbook * 100\
            , bysfbyuBt100t1000u, float(bysfbyuBt100t1000u)/allbyufsbookuser * 100\
            , bysfbyuBt100t1000c, float(bysfbyuBt100t1000c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[1000,10000)", bysfbyuBt1000t10000b, float(bysfbyuBt1000t10000b)/allbyufsbook * 100\
            , bysfbyuBt1000t10000u, float(bysfbyuBt1000t10000u)/allbyufsbookuser * 100\
            , bysfbyuBt1000t10000c, float(bysfbyuBt1000t10000c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[10000, ...)", bysfbyugt10000b, float(bysfbyugt10000b)/allbyufsbook * 100\
            , bysfbyugt10000u, float(bysfbyugt10000u)/allbyufsbookuser * 100\
            , bysfbyugt10000c, float(bysfbyugt10000c)/allbyufsbookchapter * 100))
    return (bysbyuList, bysfbyuList, monthList)


def charge_num(loglist, chargelist):
    chargebt0t10b = 0                   # 书籍数
    chargebt10t100b = 0
    chargebt100t1000b = 0
    chargebt1000t10000b = 0
    chargegt10000b = 0
    chargebt0t10u = 0                   # 用户数
    chargebt10t100u = 0
    chargebt100t1000u = 0
    chargebt1000t10000u = 0
    chargegt10000u = 0
    chargebt0t10c = 0                   # 付费章节
    chargebt10t100c = 0
    chargebt100t1000c = 0
    chargebt1000t10000c = 0
    chargegt10000c = 0

    allbook = 0
    allbookuser = 0
    allbookchapter = 0

    for i in loglist:
        gid, name, author, masklevel, feeflag, by, tf, ncp, fc\
                , usernum, chapternum\
                , bysbyuusernum, bysbyuchapternum\
                , bysfbyuusernum, bysfbyuchapternum = i
        usernumtemp = int(usernum) + int(bysbyuusernum) + int(bysfbyuusernum)
        userchargetemp = int(chapternum) + int(bysbyuchapternum) + int(bysfbyuchapternum)
        if feeflag == u'1' and by == u'000' and tf == u'000':
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(userchargetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                chargebt0t10b += 1
                chargebt0t10u += int(usernumtemp)
                chargebt0t10c += int(userchargetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                chargebt10t100b += 1
                chargebt10t100u += int(usernumtemp)
                chargebt10t100c += int(userchargetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                chargebt100t1000b += 1
                chargebt100t1000u += int(usernumtemp)
                chargebt100t1000c += int(userchargetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                chargebt1000t10000b += 1
                chargebt1000t10000u += int(usernumtemp)
                chargebt1000t10000c += int(userchargetemp)
            else:
                chargegt10000b += 1
                chargegt10000u += int(usernumtemp)
                chargegt10000c += int(userchargetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    chargelist.append(("(0,10)", chargebt0t10b, float(chargebt0t10b)/allbook * 100\
            , chargebt0t10u, float(chargebt0t10u)/allbookuser * 100\
            , chargebt0t10c, float(chargebt0t10c)/allbookchapter * 100))
    chargelist.append(("[10,100)", chargebt10t100b, float(chargebt10t100b)/allbook * 100\
            , chargebt10t100u, float(chargebt10t100u)/allbookuser * 100\
            , chargebt10t100c, float(chargebt10t100c)/allbookchapter * 100))
    chargelist.append(("[100,1000)", chargebt100t1000b, float(chargebt100t1000b)/allbook * 100\
            , chargebt100t1000u, float(chargebt100t1000u)/allbookuser * 100\
            , chargebt100t1000c, float(chargebt100t1000c)/allbookchapter * 100))
    chargelist.append(("[1000,10000)", chargebt1000t10000b, float(chargebt1000t10000b)/allbook * 100\
            , chargebt1000t10000u, float(chargebt1000t10000u)/allbookuser * 100\
            , chargebt1000t10000c, float(chargebt1000t10000c)/allbookchapter * 100))
    chargelist.append(("[10000, ...)", chargegt10000b, float(chargegt10000b)/allbook * 100\
            , chargegt10000u, float(chargegt10000u)/allbookuser * 100\
            , chargegt10000c, float(chargegt10000c)/allbookchapter * 100))
    return chargelist


# 纯互联网书阅读量
def free_num(loglist, freelist):
    freebt0t10b = 0  # 书籍数
    freebt10t100b = 0
    freebt100t1000b = 0
    freebt1000t10000b = 0
    freegt10000b = 0
    freebt0t10u = 0  # 用户数
    freebt10t100u = 0
    freebt100t1000u = 0
    freebt1000t10000u = 0
    freegt10000u = 0
    freebt0t10c = 0  # 付费章节
    freebt10t100c = 0
    freebt100t1000c = 0
    freebt1000t10000c = 0
    freegt10000c = 0
    
    allbook = 0
    allbookuser = 0
    allbookchapter = 0
    
    for i in loglist:
        gid, name, author, masklevel, feeflag, by, tf, ncp, fc \
            , usernum, chapternum \
            , bysbyuusernum, bysbyuchapternum \
            , bysfbyuusernum, bysfbyuchapternum = i
        usernumtemp = int(usernum) + int(bysbyuusernum) + int(bysfbyuusernum)
        userfreetemp = int(chapternum) + int(bysbyuchapternum) + int(bysfbyuchapternum)
        if feeflag != u'1': # 纯粹的免费书
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(userfreetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                freebt0t10b += 1
                freebt0t10u += int(usernumtemp)
                freebt0t10c += int(userfreetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                freebt10t100b += 1
                freebt10t100u += int(usernumtemp)
                freebt10t100c += int(userfreetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                freebt100t1000b += 1
                freebt100t1000u += int(usernumtemp)
                freebt100t1000c += int(userfreetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                freebt1000t10000b += 1
                freebt1000t10000u += int(usernumtemp)
                freebt1000t10000c += int(userfreetemp)
            else:
                freegt10000b += 1
                freegt10000u += int(usernumtemp)
                freegt10000c += int(userfreetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    freelist.append(("(0,10)", freebt0t10b, float(freebt0t10b) / allbook * 100 \
                           , freebt0t10u, float(freebt0t10u) / allbookuser * 100 \
                           , freebt0t10c, float(freebt0t10c) / allbookchapter * 100))
    freelist.append(("[10,100)", freebt10t100b, float(freebt10t100b) / allbook * 100 \
                           , freebt10t100u, float(freebt10t100u) / allbookuser * 100 \
                           , freebt10t100c, float(freebt10t100c) / allbookchapter * 100))
    freelist.append(("[100,1000)", freebt100t1000b, float(freebt100t1000b) / allbook * 100 \
                           , freebt100t1000u, float(freebt100t1000u) / allbookuser * 100 \
                           , freebt100t1000c, float(freebt100t1000c) / allbookchapter * 100))
    freelist.append(("[1000,10000)", freebt1000t10000b, float(freebt1000t10000b) / allbook * 100 \
                           , freebt1000t10000u, float(freebt1000t10000u) / allbookuser * 100 \
                           , freebt1000t10000c, float(freebt1000t10000c) / allbookchapter * 100))
    freelist.append(("[10000, ...)", freegt10000b, float(freegt10000b) / allbook * 100 \
                           , freegt10000u, float(freegt10000u) / allbookuser * 100 \
                           , freegt10000c, float(freegt10000c) / allbookchapter * 100))
    return freelist


# 去掉屏蔽的互联网书阅读量
def free_nomask_num(loglist, freenomasklist):
    freebt0t10b = 0  # 书籍数
    freebt10t100b = 0
    freebt100t1000b = 0
    freebt1000t10000b = 0
    freegt10000b = 0
    freebt0t10u = 0  # 用户数
    freebt10t100u = 0
    freebt100t1000u = 0
    freebt1000t10000u = 0
    freegt10000u = 0
    freebt0t10c = 0  # 付费章节
    freebt10t100c = 0
    freebt100t1000c = 0
    freebt1000t10000c = 0
    freegt10000c = 0
    
    allbook = 0
    allbookuser = 0
    allbookchapter = 0
    
    for i in loglist:
        gid, name, author, masklevel, feeflag, by, tf, ncp, fc \
            , usernum, chapternum \
            , bysbyuusernum, bysbyuchapternum \
            , bysfbyuusernum, bysfbyuchapternum = i
        # 去掉屏蔽书
        if '1' == masklevel:
            continue
        usernumtemp = int(usernum) + int(bysbyuusernum) + int(bysfbyuusernum)
        userfreetemp = int(chapternum) + int(bysbyuchapternum) + int(bysfbyuchapternum)
        if feeflag == u'0':  # 纯粹的付费书
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(userfreetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                freebt0t10b += 1
                freebt0t10u += int(usernumtemp)
                freebt0t10c += int(userfreetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                freebt10t100b += 1
                freebt10t100u += int(usernumtemp)
                freebt10t100c += int(userfreetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                freebt100t1000b += 1
                freebt100t1000u += int(usernumtemp)
                freebt100t1000c += int(userfreetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                freebt1000t10000b += 1
                freebt1000t10000u += int(usernumtemp)
                freebt1000t10000c += int(userfreetemp)
            else:
                freegt10000b += 1
                freegt10000u += int(usernumtemp)
                freegt10000c += int(userfreetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    freenomasklist.append(("(0,10)", freebt0t10b, float(freebt0t10b) / allbook * 100 \
                         , freebt0t10u, float(freebt0t10u) / allbookuser * 100 \
                         , freebt0t10c, float(freebt0t10c) / allbookchapter * 100))
    freenomasklist.append(("[10,100)", freebt10t100b, float(freebt10t100b) / allbook * 100 \
                         , freebt10t100u, float(freebt10t100u) / allbookuser * 100 \
                         , freebt10t100c, float(freebt10t100c) / allbookchapter * 100))
    freenomasklist.append(("[100,1000)", freebt100t1000b, float(freebt100t1000b) / allbook * 100 \
                         , freebt100t1000u, float(freebt100t1000u) / allbookuser * 100 \
                         , freebt100t1000c, float(freebt100t1000c) / allbookchapter * 100))
    freenomasklist.append(("[1000,10000)", freebt1000t10000b, float(freebt1000t10000b) / allbook * 100 \
                         , freebt1000t10000u, float(freebt1000t10000u) / allbookuser * 100 \
                         , freebt1000t10000c, float(freebt1000t10000c) / allbookchapter * 100))
    freenomasklist.append(("[10000, ...)", freegt10000b, float(freegt10000b) / allbook * 100 \
                         , freegt10000u, float(freegt10000u) / allbookuser * 100 \
                         , freegt10000c, float(freegt10000c) / allbookchapter * 100))
    return freenomasklist


def cp_top(loglist, cplist):
    alluser = 0
    allchap = 0
    othuser = 0
    othchap = 0
    cpdict = {}
    for i in loglist:
        gid, name, author, masklevel, feeflag, by, tf, ncp, fc\
                , usernum, chapternum\
                , bysbyuusernum, bysbyuchapternum\
                , bysfbyuusernum, bysfbyuchapternum = i
        usernumtemp = int(usernum) + int(bysbyuusernum) + int(bysfbyuusernum)
        userchargetemp = int(chapternum) + int(bysbyuchapternum) + int(bysfbyuchapternum)
        if ncp == u'免费书':
            continue
        if cpdict.has_key(ncp):
            user, chapter = cpdict[ncp]
            user += int(usernumtemp)
            chapter += int(userchargetemp)
            cpdict[ncp] = (user, chapter)
        else:
            cpdict[ncp] = (int(usernumtemp), int(userchargetemp))
    for cp, value in cpdict.items():
        usernum, chapternum = value
        alluser += int(usernum)
        allchap += int(chapternum)
        cplist.append((cp, int(usernum), int(chapternum)))
    cplist.sort(key = lambda x: int(x[1]), reverse = True)
    cplisttop = cplist
    '''
    cplisttop = cplist[:10]
    for i in range(10, len(cplist)):
        cp, usernum, chapnum = cplist[i]
        othuser += usernum
        othchap += chapnum
    cplisttop.append((u'其它', int(othuser), int(othchap)))
    '''
    cplist = []
    for i in cplisttop:
        cp, user, chap = i
        cplist.append((cp, user, float(user)/alluser * 100, chap, float(chap)/allchap * 100))
    return cplist


def top_list(logList, chargetop, monthTop, tfTop, freeTop, pubTop):
    chargeTop = []
    fcTop = []
    monthTop = []
    tfTop = []
    freeTop = []
    pubTop = []

    for i in logList:
        gid, name, author, maskLevel, feeFlag, by, tf, ncp, fc\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum = i
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if by != u'000' and tf == u'000' and (int(bysByuUserNum) > 0 or int(bysFbyuUserNum)):                                       # 包月
            monthTop.append((gid, name, author, usernumTemp, userChargeTemp))
        elif tf != u'000' and by == u'000':
            tfTop.append((gid, name, author, usernumTemp, userChargeTemp))
        elif feeFlag == u'1' and fc == '000':                                                # 付费书
            chargeTop.append((gid, name, author, usernumTemp, userChargeTemp))
        elif feeFlag == u'1' and fc != '000':                                                # 付费书
            fcTop.append((gid, name, author, usernumTemp, userChargeTemp))
        elif feeFlag == u'10':
            pubTop.append((gid, name, author, usernumTemp, userChargeTemp))
        elif feeFlag == u'0':
            freeTop.append((gid, name, author, usernumTemp, userChargeTemp))

    chargeTop.sort(key = lambda x: x[3], reverse = True)
    fcTop.sort(key = lambda x: x[3], reverse = True)
    monthTop.sort(key = lambda x: x[3], reverse = True)
    tfTop.sort(key = lambda x: x[3], reverse = True)
    freeTop.sort(key = lambda x: x[3], reverse = True)
    pubTop.sort(key = lambda x: x[3], reverse = True)
    chargeTop = chargeTop[:10]
    fcTop = fcTop[:10]
    monthTop = monthTop[:10]
    tfTop = tfTop[:10]
    freeTop = freeTop[:10]
    pubTop = pubTop[:10]
    return(chargeTop, monthTop, tfTop, freeTop, pubTop, fcTop)


def print_cp_top(mlist, title, titleTup):
    outBuf = ""
    outBuf += '<h4>' + title + '</h4>\n'
    outBuf += '<table width="80%">\n'
    outBuf += '<tr align="center">'
    for i in titleTup:
        outBuf += '<th align="center">' + i + '</th>\n'
    outBuf += '</tr>\n'
    rank = 1
    for i in mlist:
        outBuf += '<tr align="center">'
        for j in range(len(i)):
            if j == 0:
                outBuf += '<td align="left">' + str(rank) + '</td>\n'
                outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
                rank += 1
                continue
            if j % 2:
                outBuf += '<td align="left">' + str(i[j]) + "(" + str('%.3f' % i[j + 1]) + "%)" + '</td>\n'
        outBuf += '</tr>\n'
    outBuf += "</table>"
    return outBuf


def print_book_top(mlist, title, titleTup):
    if len(mlist) == 0:
        return ""
    outBuf = ""
    outBuf += '<h4>' + title + '</h4>\n'
    outBuf += '<table width="80%">\n'
    outBuf += '<tr align="center">'
    for i in titleTup:
        outBuf += '<th align="center">' + i + '</th>\n'
    outBuf += '</tr>\n'
    rank = 1
    for i in mlist:
        outBuf += '<tr align="center">'
        for j in range(len(i)):
            if j == 0:
                outBuf += '<td align="left">' + str(rank) + '</td>\n'
                outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
                rank += 1
                continue
            outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
        outBuf += '</tr>\n'
    outBuf += "</table>"
    return outBuf


def print_list(mlist, title, titleTup):
    outBuf = ""
    outBuf += '<h4>' + title + '</h4>\n'
    outBuf += '<table width="80%">\n'
    outBuf += '<tr align="center">'
    for i in titleTup:
        outBuf += '<th align="center">' + i + '</th>\n'
    outBuf += '</tr>\n'
    mlist.sort(key = lambda x: x[3], reverse = True)
    for i in mlist:
        outBuf += '<tr align="left">\n'
        for j in range(0, len(i), 2):
            if j == 0:
                outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
            else:
                outBuf += '<td align="left">' + str(i[j - 1]) + '(' + str("%.3f" % i[j]) + '%)' + '</td>\n'
        outBuf += "</tr>\n"
    outBuf += "</table>"
    return outBuf


def save_file(path, string):
    fW = open(path, "w")
    fW.write(string)
    fW.close()
    return

###############################################################################################################


