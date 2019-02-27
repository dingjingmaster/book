#!/usr/bin/env python3
# -*- coding: utf8 -*-


class CharacterTransInt:
    __CN_NUM = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
        '两': 2,
    }
    __CNN_UNIT = {
        '十': 10, '拾': 10,
        '百': 100, '佰': 100,
        '千': 1000, '仟': 1000,
        '万': 10000, '萬': 10000,
        '亿': 100000000, '億': 100000000,
    }

    def chinese_to_arabic(self, cn: str)->int:
        value = 0
        stack = []
        """ 预处理 """
        cn = cn.replace(' ', '')
        """ 本身就是数字 """
        try:
            value = int(cn)
            return value
        except Exception:
            pass

        """ 汉字数字转阿拉伯数字 """
        for cndig in reversed(cn):
            tmp = 0
            flag = False
            if cndig in self.__CNN_UNIT:
                unit = self.__CNN_UNIT.get(cndig)
                stack.append(unit)
            else:
                tmp = self.__CN_NUM.get(cndig)
                if tmp:
                    flag = True
            if flag and len(stack) > 0:
                value += tmp * stack.pop()
            elif flag and len(stack) == 0:
                value += tmp
        if len(stack) > 0:
            value += stack.pop()
        
        """ 一零一 类型的转换 """
        flag = False
        tmpInt = ''
        if value == 0:
            for i in cn:
                if i in self.__CN_NUM:
                    tmpInt += i
                if i in self.__CNN_UNIT:
                    flag = True
                    break
            if not flag:
                value = int(tmpInt)

        return value


if __name__ == '__main__':
    test = [
        '十', '一十', '九十九', '一百', '九百九十九', '一千',  '九千九百九十九', '一万', '九万九千九百九十九',
        '两百',
    ]

    ct = CharacterTransInt()

    for cn in test:
        x = ct.chinese_to_arabic(cn)
        print(cn, x)

