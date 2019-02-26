#!/usr/bin/env python3
# -*- coding: utf8 -*-

import re

"""
    提取章节名中的 章节信息、章节序号信息、无用章节信息
    1. 提取章节序号信息
        ① 检查 第 xxx 章|节|幕
        ② xxx 章
"""


class GetChapterName:
    """ 第xxx章|节|幕 提取 """
    step1 = ['章', '节', '辑']
    __step1_re = None
    """ xxx章|节|幕 + 空白字符 提取 """
    step2 = ['章']
    __step2_re = None

    def __init__(self):
        self.__step1_re = re.compile('第\\S+' + '(' + '|'.join(self.step1) + ')', re.U)

    def chapter_index_str(self, cn: str)->str:
        val = ''
        tp1 = self.__step1_re.search(cn)
        if tp1:
            val = tp1.group()
            val = val.replace('第', '')
            val = val.replace('章', '')
        return val


if __name__ == '__main__':
    exit(0)
