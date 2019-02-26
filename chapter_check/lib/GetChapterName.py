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
    step1 = ['章', '节', '辑', ' ']
    __step1_re = None
    """ 特殊字符 """
    step21 = ['【']
    step22 = ['】']
    __step2_re = None
    """ xxx.xxx(数字)章|节|幕 + 空白字符 提取 """
    step3 = ['章', '节']
    __step3_re = None
    """ 第 xxx(数字) 提取 """
    step4 = ['第']
    __step4_re = None

    def __init__(self):
        self.__step1_re = re.compile('第.?\\S+.?' + '(' + '|'.join(self.step1) + ')', re.U)
        self.__step2_re = re.compile('(' + '|'.join(self.step21) + ')' + '.+\\S+.?' + '(' + '|'.join(self.step22) + ')', re.U)
        self.__step3_re = re.compile('\\d?\\.\\d?.?' + '(' + '|'.join(self.step3) + ')', re.U)
        self.__step4_re = re.compile('(' + '|'.join(self.step4) + ')' + '.?\\d?', re.U)

    def chapter_index_str(self, cn: str)->str:
        val = ''
        flag = False
        """ 去除第一种情况 """
        tp1 = self.__step1_re.search(cn)
        if not flag and tp1:
            flag = True
            val = tp1.group()
            val = val.replace('第', '')
            for i in self.step1:
                val = val.replace(i, '')

        """ 去除第二种情况 """
        tp2 = self.__step2_re.search(cn)
        if not flag and tp2:
            flag = True
            val = tp2.group()
            for i in self.step21:
                val = val.replace(i, '')
            for i in self.step22:
                val = val.replace(i, '')

        """ 去除第三种情况 """
        tp3 = self.__step3_re.search(cn)
        if not flag and tp3:
            flag = True
            val = tp3.group()
            for i in self.step3:
                val = val.replace(i, '')
            arr = val.split('.')
            if len(arr) >= 2:
                val = arr[len(arr) - 1]
            else:
                val = arr[0]
        """ 去除第四种情况 """
        tp4 = self.__step4_re.search(cn)
        if not flag and tp4:
            flag = True
            val = tp4.group()
            for i in self.step4:
                val = val.replace(i, '')
        return val


if __name__ == '__main__':
    exit(0)
