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
    step1 = ['章', '节', '辑', ' ', '\\s', ',', '，']
    __step1_re = None
    """ 特殊字符 """
    step21 = ['【']
    step22 = ['】']
    __step2_re = None
    """ xxx.xxx(数字)章|节|幕 + 空白字符 提取 """
    step3 = ['章', '节', '幕', ':', '：', ',', '，', '、', '\\d+', '\\S+ ']
    __step3_re = None
    """ 第 xxx(数字) 提取 """
    step4 = ['第', '章']
    __step4_re = None
    """ 直接提取 """
    step5 = [
        '〇', '一', '二', '三', '四', '五', '六', '七', '八', '九',
        '零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖',
        '两',
        '十', '拾', '百', '佰', '千', '仟', '万', '萬', '亿', '億',
    ]
    __step5_re = None

    def __init__(self):
        self.__step1_re = re.compile('第.?\\S+.?' + '(' + '|'.join(self.step1) + ')', re.U)
        self.__step2_re = re.compile('(' + '|'.join(self.step21) + ')' + '.?\\S+.?' + '(' + '|'.join(self.step22) + ')', re.U)
        self.__step3_re = re.compile('\\d+\\.(\\d+\\.|\\d+.?|.?\\S+.?)' + '(' + '|'.join(self.step3) + ')', re.U | re.DOTALL)
        self.__step4_re = re.compile('(' + '|'.join(self.step4) + ')' + '(.?\\d+|\\S+ )', re.U)
        self.__step5_re = re.compile('(' + '\\S+|'.join(self.step5) + '\\S+)\\.', re.U)

    def chapter_index_str(self, cn: str)->str:
        val = ''
        flag = False
        """ 去除第一种情况 """
        tp1 = self.__step1_re.search(cn)
        if not flag and tp1:
            flag = True
            val = tp1.group()

        """ 去除第二种情况 """
        tp2 = self.__step2_re.search(cn)
        if not flag and tp2:
            flag = True
            val = tp2.group()

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
        """ 第五种请情况 """
        tp5 = self.__step5_re.search(cn)
        if not flag and tp5:
            flag = True
            val = tp5.group()
        """ 去除关键字 """
        val = val.replace('第', '')
        for i in set(self.step1) | set(self.step21) | set(self.step22) | set(self.step4) | set('.'):
            val = val.replace(i, '')
        return val.strip()


if __name__ == '__main__':
    test = [
        '11. 第九百九十九章 测试', '11.第 九百九十九 章 测试', '11. 第九百九十九 测试', '22. 第九百九十九　',
        '11. 【九百九十九】 测试', '11.【999】测试',
        '11.999章测试', '11.999 章 测试', '248.九百九十九章 真假观沧海', '7.007 大当家的', '85.085.杀鸡儆猴', '444.第九百九十九.疑点重重',
        '11.第 999 测试', '11.第 999测试', '369.章九百九十九 偶遇'
    ]

    cn = GetChapterName()
    for i in test:
        res = cn.chapter_index_str(i)
        print('%-60s\t------>\t%-20s' % (i, res))
    
    exit(0)
