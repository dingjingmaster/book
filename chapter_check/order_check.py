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
    top10000 = work_dir + '/resource/top10000.txt'
    cn = GetChapterName()
    ci = CharacterTransInt()
    top10000Dict = {}
    right_fw = open(right, 'w', encoding='utf8')
    wrong_fw = open(wrong, 'w', encoding='utf8')
    left_fw = open(left, 'w', encoding='utf8')
    summary_fw = open(summary, 'w', encoding='utf8')
    debug_fw = open(work_dir + '/resource/debug.txt', 'w', encoding='utf8')
    with open(top10000, 'r', encoding='utf8') as fr:
        for line in fr.readlines():
            line = line.strip()
            arr = line.split('\t')
            top10000Dict[arr[0]] = 0
    with open(work_dir + '/resource/charge_chapter.txt',
              'r', encoding='utf8') as fr:
        for line in fr.readlines():
            """ 每一行代表一本小说 """
            line = line.strip()
            arr = line.split('{]')
            index = 0
            filter = {}
            gid = arr[1]
            lack_chapter = []
            chapter_index_list = []
            if gid not in top10000Dict:
                continue
            for cp in arr[2:]:
                cp_info = cn.chapter_index_str(cp)
                if '' == cp_info:
                    debug_fw.write(cp + '\t' + '1' + '\n')
                    continue
                cpint = ci.chinese_to_arabic(cp_info)
                if (cpint in filter) or (cpint == 0):
                    continue
                index += 1
                filter[cpint] = index
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
                    lackNumA = 0
                    lackNumB = 0
                    for ik in chapter_index_list:
                        tmp1 = filter[ik]
                        if ik + lackNumA == tmp1 + lackNumB:
                            continue
                        lack_chapter.append(str(tmp1))
                        lack_chapter.append(str(ik))
                        while True:
                            if ik + lackNumA > tmp1 + lackNumB:
                                lackNumB += 1
                            elif ik + lackNumA < tmp1 + lackNumB:
                                lackNumA += 1
                            elif ik + lackNumA == tmp1 + lackNumB:
                                break
                    lack_chapter = set(lack_chapter)
                    lack_chapter = list(lack_chapter)
                    lack_chapter.sort()
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
    debug_fw.close()
    right_fw.close()
    wrong_fw.close()
    left_fw.close()
    summary_fw.close()
    exit(0)

