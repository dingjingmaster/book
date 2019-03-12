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
    outBufG = ''
    logListG = []                                           # 日志
    ifmaskListG = []                                        # 是否屏蔽
    unmaskFeeChargeListG = []                               # 非屏蔽 互联网书 与 cp 正版书情况
    unmaskChargeListG = []                                  # 非屏蔽 付费书 个付费情况占比
    unmaskChargeStepListG = []                              # 非屏蔽 按章付费书 阅读量
    unmaskFreeStepListG = []                                # 非屏蔽 免费书 阅读量

    parse_info(logPath, logListG)

    mask_level_list(logListG, ifmaskListG)
    unmask_fee_charge(logListG, unmaskFeeChargeListG)
    unmask_charge_info(logListG, unmaskChargeListG)
    unmask_charge_step(logListG, unmaskChargeStepListG)
    unmask_free_step(logListG, unmaskFreeStepListG)

    outBufG += print_list(ifmaskListG, "屏蔽情况", ("屏蔽/非屏蔽", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskFeeChargeListG, "非屏蔽互联网书与cp正版书", ("阅读情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskChargeListG, "非屏蔽cp正版书各占比", ("阅读情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskChargeStepListG, "非屏蔽按章付费书", ("阅读情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskFreeStepListG, "非屏蔽互联网书", ("阅读情况", "书籍量", "阅读量", "阅读章节数"))
    save_file(resultPath, outBufG)
 
    exit(0)
