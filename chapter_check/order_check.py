#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
sys.path.append('lib')

from GetChapterName import GetChapterName
from CharacterTransInt import CharacterTransInt

"""
    输入的数据格式： {]gid{]章节1{]章节2{].....
    为了xx章xx节类型的数据，统一归一为 第xx部 第xx章
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
    top10000 = work_dir + '/resource/top1000.txt'
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
            status = ''
            if int(arr[2]) == 2:
                status = '完结'
            else:
                status = '连载'
            top10000Dict[arr[0]] = status
    with open(work_dir + '/resource/charge_chapter.txt', 'r', encoding='utf8') as fr:
        for line in fr.readlines():
            """ 每一行代表一本小说 """
            line = line.strip()
            arr = line.split('{]')
            filter = {}
            gid = arr[1]
            lack_chapter = ''
            chapter_index_list = []
            if gid not in top10000Dict:
                continue
            for cp in arr[1:]:
                for cp_index in cn.chapter_index_str(cp):
                    arr = cp_index.split('_')
                    if len(arr) < 2:
                        debug_fw.write(cp + '\t' + cp_index + '\n')
                        continue
                    cpInt0 = ci.chinese_to_arabic(arr[0])
                    cpInt1 = ci.chinese_to_arabic(arr[1])
                    cpinfo = str(cpInt0) + '_' + str(cpInt1)
                    if cpinfo in filter or cpInt1 == 0:
                        continue
                    filter[cpinfo] = 0
                    chapter_index_list.append((cpInt0, cpInt1))
            """ 检查是否缺章 """
            chapter_length = len(chapter_index_list)
            if chapter_length > 1:
                chapter_index_list.sort(key=lambda x: (x[0], x[1]))
                # 第 xx 章的情况
                if chapter_index_list[chapter_length - 1][0] == 0:
                    if chapter_length == chapter_index_list[chapter_length - 1][1]:
                        rightNum += 1
                        right_fw.write(gid + '\n')
                    else:
                        wrongNum += 1
                        index = 1
                        for ik in chapter_index_list:
                            t1, t2 = ik
                            if t2 == index:
                                index += 1
                                continue
                            lack_chapter = str(index)
                            break
                        wrong_fw.write(gid + '\t' + top10000Dict[gid] + '\t' + lack_chapter + '\n')
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

