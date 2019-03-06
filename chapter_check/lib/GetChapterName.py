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
    """ 提取 第xx部 第xx章 """
    step1 = ['(第\\s?\\S*\\s?卷)[\\s?.?\\s?](第\\s?\\S*\\s?章)']
    __step1_re = None
    """ 提取 第xxx~xxx章   """
    step2 = ['(第.?\\d+.?)[-~_](.?\\d+.?章)']
    splited2 = ['-', '~', '_']
    keyWord2 = ['第', '章']
    __step2_re = None
    """ 第xxx章|节|幕 提取 """
    step3 = ['章', '节', '辑', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
             ',', '，', ':', '：', '.', ' ', '']
    __step3_re = None
    """ 特殊字符 """
    step41 = ['【']
    step42 = ['】']
    __step4_re = None
    """ xxx.xxx(数字)章|节|幕 + 空白字符 提取 """
    step5 = ['章', '节', '幕', '回', ':', '：', ',', '，', '、', '\\d+']
    __step5_re = None
    """ 第 xxx(数字) 提取 """
    step6 = ['第', '章', '(c|C)hapter.?', '(c|C)', '回']
    __step6_re = None
    """ 直接提取 """
    stepf = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        '〇', '一', '二', '三', '四', '五', '六', '七', '八', '九',
        '零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖',
        '两',
        '十', '拾', '百', '佰', '千', '仟', '万', '萬', '亿', '億',
    ]
    """ 类型 """
    ctype = [
        '第', '章', '节', '幕', '回', '辑', '卷', '部',
    ]
    """ 要删除的关键词 """
    deleteWord = [
        '\\.', '\\[', '\\]', '【', '】', ':', '：', '<', '>', '《', '》', '\\?', '/', '\\', '"', '“', '”',
    ]

    def __init__(self):
        self.__step1_re = re.compile('(' + '|'.join(self.step1) + ')')
        self.__step2_re = re.compile('(' + '|'.join(self.step2) + ')')
        self.__step3_re = re.compile('第\\s?\\S+\\s?' + '[' + ''.join(self.step3) + ']', re.U)
        self.__step4_re = re.compile('(' + '|'.join(self.step41) + ')' + '.?\\S+.?' + '(' + '|'.join(self.step42) + ')', re.U)
        self.__step5_re = re.compile('(\\d+\\.|\\d+.?|.?\\S+.?)' + '(' + '|'.join(self.step5) + ')', re.U | re.DOTALL)
        self.__step6_re = re.compile('(' + '|'.join(self.step6) + ')' + '(.?\\d+|\\S+ )', re.U)

    def chapter_index_str(self, cn: str)->str:
        val = ''
        flag = False
        """ 去除开始的序号 """
        cn = re.sub('^\\d+\\.', '', cn, re.DOTALL)
        """ 处理不可见字符 """
        cn = re.sub('[\t\n\f]', '', cn)
        cn = ''.join(cn.split())
        """ 去除第一种情况 """
        tp1 = self.__step1_re.search(cn)
        if not flag and tp1:
            flag = True
            val = tp1.group()
            
        """ 去除第二种情况 """
        tp2 = self.__step2_re.search(cn)
        if not flag and tp2:
            flag = True
            isRange = True
            val = tp2.group()

        """ 去除第三种情况 """
        tp3 = self.__step3_re.search(cn)
        if not flag and tp3:
            flag = True
            val = tp3.group()

        """ 去除第四种情况 """
        tp4 = self.__step4_re.search(cn)
        if not flag and tp4:
            flag = True
            val = tp4.group()

        """ 去除第五种情况 """
        tp5 = self.__step5_re.search(cn)
        if not flag and tp5:
            flag = True
            val = tp5.group()
            for i in self.step5:
                val = val.replace(i, '')
            arr = val.split('.')
            if len(arr) >= 2:
                val = arr[len(arr) - 1]
            else:
                val = arr[0]
        """ 去除第六种情况 """
        tp6 = self.__step6_re.search(cn)
        if not flag and tp6:
            flag = True
            val = tp6.group()
        """ 提取章节序号 """
        if flag is False:
            val = cn
        val = re.sub('[' + ''.join(self.deleteWord) + ']', '', val)
        return val
        # results = []
        # if isRange:
        #     results = self.get_range_index(val)
        # else:
        #     results = self.get_chapter_index(val)
        # for i in results:
        #     yield i
    
    def get_range_index(self, cn: str)->[str]:
        filter = set()
        result = []
        cn = re.sub('[' + ''.join(self.keyWord2) + ']', '', cn)
        for i in self.splited2:
            arr = cn.split(i)
            if len(arr) >= 2:
                for line in arr:
                    try:
                        filter.add(int(line))
                    except Exception as e:
                        pass
                break
        res = list(filter)
        res.sort()
        if len(res) == 2:
            for i in range(res[0], res[1] + 1):
                result.append('0_' + str(i))
        else:
            for i in res:
                result.append('0_' + str(i))
        return result

    def get_chapter_index(self, cn: str)->[str]:
        resultList = []
        numList = []
        wordList = []
        numTemp = ''
        wordTemp = ''
        canStore = False
        chapterTemp = cn
        index = 0
        for i in chapterTemp:
            if i in self.ctype:
                index += 1
        if index < 4:                                          # 第xx章
            resultList.append('0')
            for i in chapterTemp:
                if i in self.stepf:
                    canStore = True
                    try:
                        int(i)
                        numTemp += i
                    except Exception as e:
                        wordTemp += i
                else:
                    if canStore:
                        if wordTemp != '':
                            wordList.append(wordTemp)
                        elif numTemp != '':
                            numList.append(numTemp)
                        numTemp = ''
                        wordTemp = ''
                        canStore = False
            if wordTemp != '':
                wordList.append(wordTemp)
            elif numTemp != '':
                numList.append(numTemp)
            if len(wordList) > 0:
                resultList.append(wordList[0])
            elif len(numList) > 0:
                resultList.append(numList[-1])
        else:                                                   # 第xx部 第xx章
            for i in chapterTemp:
                if i in self.stepf:
                    if not canStore:
                        canStore = True
                    try:
                        int(i)
                        numTemp += i
                    except Exception as e:
                        wordTemp += i
                else:
                    if canStore:
                        if wordTemp != '':
                            resultList.append(wordTemp)
                        elif numTemp != '':
                            resultList.append(numTemp)
                        numTemp = ''
                        wordTemp = ''
                        canStore = False
            if wordTemp != '':
                resultList.append(wordTemp)
            elif numTemp != '':
                resultList.append(numTemp)
        """ 提取数字 """
        cn = '_'.join(resultList)
        return [cn]


if __name__ == '__main__':
    test = [
        '11. 第九百九十九章 测试', '11.第 九百九十九 章 测试', '11. 第九百九十九 测试', '22. 第九百九十九　', '407.第 999章机遇', '第1章： 悲惨山村',
        '11. 【九百九十九】 测试', '11.【999】测试',
        '11.999章测试', '11.999 章 测试', '248.九百九十九章 真假观沧海', '7.007 大当家的', '85.085.杀鸡儆猴', '444.第九百九十九.疑点重重', '236.第二百三十五进入皇宫的方法', '236.第二百三三三进入皇宫的方法',
        '11.第 999 测试', '11.第 999测试', '369.章九百九十九 偶遇',
        '2.二', '83.第二卷在京都　第四十三章　破窗',
        '2.第三卷 sss 第一章xxx',
        '2.第三卷sss第一章xxx',
        '3.第 12 - 13 章', '3.第12-13章', '4.第12-0222章',
        '1180.第一千一百八十一章  止不住的回忆',
    ]

    cn = GetChapterName()
    for i in test:
        print('%-60s ---> %-20s' % (i, cn.chapter_index_str(i)))
        # print(i, end='\t-------->'),
        # for j in cn.chapter_index_str(i):
        #     print('%-20s' % j, end=' ')
        # print('\n')

    exit(0)
