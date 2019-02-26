#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
sys.path.append('lib')

from GetChapterName import GetChapterName
from CharacterTransInt import CharacterTransInt

"""
    输入的数据格式： {]gid{]章节1{]章节2{].....
"""

if __name__ == '__main__':
    leftNum = 0
    rightNum = 0
    wrongNum = 0
    work_dir = '/'.join(sys.argv[0].split('/')[:-1])
    right = work_dir + '/resource/chapter_right.txt'
    wrong = work_dir + '/resource/chapter_wrong.txt'
    left = work_dir + '/resource/chapter_left.txt'
    summary = work_dir + '/resource/summary.txt'
    cn = GetChapterName()
    ci = CharacterTransInt()
    right_fw = open(right, 'w', encoding='utf8')
    wrong_fw = open(wrong, 'w', encoding='utf8')
    left_fw = open(left, 'w', encoding='utf8')
    summary_fw = open(summary, 'w', encoding='utf8')
    with open(work_dir + '/resource/charge_chapter.txt',
              'r', encoding='utf8') as fr:
        for line in fr.readlines():
            """ 每一行代表一本小说 """
            chapter_index_list = []
            lack_chapter = []
            filter = set()
            line = line.strip()
            arr = line.split('{]')
            gid = arr[1]
            for cp in arr[1:]:
                cp_info = cn.chapter_index_str(cp)
                if '' == cp_info:
                    continue
                cpint = ci.chinese_to_arabic(cp_info)
                if cpint in filter:
                    continue
                filter.add(cpint)
                chapter_index_list.append(cpint)
            """ 检查是否缺章 """
            chapter_length = len(chapter_index_list)
            if chapter_length > 1:
                chapter_index_list.sort()
                if chapter_length == chapter_index_list[chapter_length - 1]:
                    rightNum += 1
                    right_fw.write(gid + '\n')
                else:
                    wrongNum += 1
                    """ 检查缺少哪些章节 """
                    index = 0
                    for i in chapter_index_list:
                        if index > 0 and i - chapter_index_list[index - 1] != 1:
                            lack_chapter.append(str(chapter_index_list[index - 1]))
                            lack_chapter.append(str(i))
                            break
                        index += 1
                    wrong_fw.write(gid + '\t' + '|'.join(lack_chapter) + '\n')
            else:
                left_fw.write(line + '\n')
                leftNum += 1
            """ 检查是否乱序 """
    result = '正确的: ' + str(rightNum) + '\n'\
             + '错误的: ' + str(wrongNum) + '\n'\
             + '未识别: ' + str(leftNum) + '\n'\
             + '总共: ' + str(rightNum + wrongNum + leftNum)
    print(result)
    summary_fw.write(result)
    right_fw.close()
    wrong_fw.close()
    left_fw.close()
    summary_fw.close()
    exit(0)

