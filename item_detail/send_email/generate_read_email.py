#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from function import *

if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(-1)
    logPath = sys.argv[1]
    resultPath = sys.argv[2]

    # 输出结果链表
    outBufG = ""
    logListG = []                # 日志
    ifmaskListG = []             # 是否屏蔽
    maskFeeListG = []            # 屏蔽-状态
    unmaskFeeListG = []          # 非苹果比-状态
    bysbyuListG = []
    bysfbyuListG = []
    monthListG = []
    chargeListG = []
    freeListG = []
    tfListG = []
    chargeTopG = []
    fcTopG = []
    monthTopG = []
    tfTopG = []
    freeTopG = []
    pubTopG = []
    cpListG = []
    
    # 去掉屏蔽书，免费书的情况
    freeListNoMaskG = []

    ##
    parse_info(logPath, logListG)

    mask_level_list(logListG, ifmaskListG)
    mask_fee_flag(logListG, maskFeeListG)
    unmask_fee_flag(logListG, unmaskFeeListG)
    month_num(logListG, bysbyuListG, bysfbyuListG, monthListG)
    charge_num(logListG, chargeListG)                           # 付费情况
    free_num(logListG, freeListG)                               # 免费书情况
    free_nomask_num(logListG, freeListNoMaskG)                  # 去除屏蔽的免费书阅读情况
    tf_num(logListG, tfListG)                                   # 付费情况

    chargeTopG, monthTopG, tfTopG, freeTopG, pubTopG, fcTopG \
            = top_list(logListG, chargeTopG, monthTopG, tfTopG, freeTopG, pubTopG)
    cpListG = cp_top(logListG, cpListG)

    outBufG += print_list(ifmaskListG,            "屏蔽情况", ("屏蔽/非屏蔽", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskFeeListG, "非屏蔽书付费情况", ("付费情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(maskFeeListG,     "屏蔽书付费情况", ("付费情况", "书籍量", "阅读量", "阅读章节数"))

    outBufG += print_list(chargeListG,          "付费书情况", ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(freeListG,          "免费书情况", ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(freeListNoMaskG,          "去除屏蔽后免费书情况", ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(tfListG,      "限免书阅读情况",     ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(bysbyuListG,    "包月用户看包月书", ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(bysfbyuListG, "非包月用户看包月书", ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))

    outBufG += print_book_top(chargeTopG, "付费书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(fcTopG, "全免书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(monthTopG,  "包月书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(tfTopG,     "限免书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(freeTopG,   "免费书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(pubTopG,    "公版书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))

    outBufG += print_cp_top(cpListG,  "各cp阅读量top-10", ("排名", "cp名", "阅读量及占比", "阅读章节数及占比"))

    save_file(resultPath, outBufG)
 
    exit(0)
