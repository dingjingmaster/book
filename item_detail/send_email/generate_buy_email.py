#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")
from function import *

## 付费相关统计 ##
if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(-1)
    logPath = sys.argv[1]
    resultPath = sys.argv[2]

    # 输出结果链表
    outBufG = ""
    logListG = []                # 日志
    ifmaskListG = []             # 是否屏蔽
    maskFeeListG = []            # 屏蔽-付费状态
    unmaskFeeListG = []          # 非苹果比-付费状态
    bysbyuListG = []             #
    bysfbyuListG = []
    monthListG = []
    chargeListG = []
    tfListG = []
    chargeTopG = []
    fcTopG= []
    monthTopG = []
    tfTopG = []
    freeTopG = []
    pubTopG = []
    cpListG = []

    ##
    parse_info(logPath, logListG)
    mask_level_list(logListG, ifmaskListG)
    mask_fee_flag(logListG, maskFeeListG)
    unmask_fee_flag(logListG, unmaskFeeListG)
    month_num(logListG, bysbyuListG, bysfbyuListG, monthListG)
    charge_num(logListG, chargeListG)
    tf_num(logListG, tfListG)
    chargeTopG, monthTopG, tfTopG, freeTopG, pubTopG, fcTopG\
            = top_list(logListG, chargeTopG, monthTopG, tfTopG, freeTopG, pubTopG)
    cpListG = cp_top(logListG, cpListG)

    outBufG += print_list(ifmaskListG,            "屏蔽情况", ("屏蔽情况", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_list(unmaskFeeListG, "非屏蔽书付费情况", ("付费情况", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_list(maskFeeListG,     "屏蔽书付费情况", ("付费情况", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_list(chargeListG,          "付费书情况", ("购买量分段", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_list(tfListG,      "限免书付费情况",     ("购买量分段", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_list(bysbyuListG,    "包月用户看包月书", ("购买量分段", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_list(bysfbyuListG, "非包月用户看包月书", ("购买量分段", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))
    #outBufG += print_list(monthListG,           "包月书情况", ("购买量分段", "书籍量", "付费章节阅读人数", "阅读的付费章节数"))

    outBufG += print_book_top(chargeTopG, "付费排行榜", ("排名", "书籍ID", "书籍名", "作者名", "付费章节阅读人数", "阅读的付费章节数"))
    #outBufG += print_book_top(fcTopG, "全免排行榜", ("排名", "书籍ID", "书籍名", "作者名", "付费章节阅读人数", "阅读的付费章节数"))
    outBufG += print_book_top(monthTopG,  "包月排行榜", ("排名", "书籍ID", "书籍名", "作者名", "付费章节阅读人数", "阅读的付费章节数"))

    outBufG += print_cp_top(cpListG, "各cp购买量top-10", ("排名", "cp名", "付费章节阅读人数及占比", "阅读的付费章节数及占比"))

    save_file(resultPath, outBufG)
 
    exit(0)
