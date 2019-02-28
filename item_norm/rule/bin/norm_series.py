#!/usr/bin/env python
#coding=utf-8

import os
import sys
import re

param_count = len(sys.argv)
if param_count != 4 :
  print ("请输入命令行参数:")
  print ("   参数1:白名单文件")
  print ("   参数2:原文件(norm_name\\tgid\\tview_count\\tfee_flag)")
  print ("   参数3:结果文件")
  print ("如下格式:")
  print ("python ./norm_series.py ./series_white_list.txt ./gid_norm_title.txt ./result.txt")
  sys.exit()

# 输入文件
series_white_list_file = sys.argv[1]
gid_norm_title_file = sys.argv[2]
result_file = sys.argv[3]

# 系列名白名单
dict_white = {}
f = open(r'' + series_white_list_file)
set = f.readlines()
for s in set :
  s = s.strip("\n")
  s_arr = s.split("{]")
  dict_white[s_arr[0]] = s_arr[1]
f.close()

f1 = open(r'' + gid_norm_title_file)
f2 = open(r'' + result_file, 'w')

set_d1 = []
set_d2 = []
set_d3 = []
set_d4 = []
sets = []

lines = f1.readlines()
for line in lines :
  line = line.strip('\n')
  line_arr = line.split('\t')
  if len(line_arr) != 6:
    continue
  gid = line_arr[0]
  feeFlag = line_arr[1]
  viewCount = line_arr[2]
  normName = line_arr[3]
  normAuthor = line_arr[4]
  normSeries = line_arr[5]

  if dict_white.has_key(normName):
    normSeries = dict_white[normName]
    # 直接输出白名单中的书籍
    f2.writelines(gid + "\t" + feeFlag + "\t" + viewCount + "\t" + normName + "\t" + normAuthor + "\t" + normSeries + "\n")
  else :
    line_tmp = re.search(r'^(.*?)(\d|之|上|中|下|pr1est|第|卷)(.*?)$', normSeries, re.I)
    if line_tmp:
      sets.append(line) # 有上、中、下之类的 系列名特征
    else :
      f2.writelines(gid + "\t" + feeFlag + "\t" + viewCount + "\t" + normName + "\t" + normAuthor + "\t" + normSeries + "\n")

# 第二步
for line in sets:
  line_arr = line.split('\t')
  if len(line_arr) != 6:
    print("系列归一错误：" + line)
    continue

  gid = line_arr[0]
  feeFlag = line_arr[1]
  viewCount = line_arr[2]
  normName = line_arr[3]
  normAuthor = line_arr[4]
  normSeries = line_arr[5]

  line_tmp = re.search(r'^(.*?)(\d+-\d+$|上下$)', normSeries, re.I)
  if line_tmp :
    if len(line_tmp.group(1)) > 0 and line_tmp.group(1) not in set_d1 :
      set_d1.append(line_tmp.group(1)) #set_d1 数字结尾、上、下
    continue

  line_tmp = re.search(r'^(.*?)((第\d+)(册|季|辑)|part\d+|卷\d+|上下部|上部|下部|中部之)(.*?)$', normSeries, re.I)
  if line_tmp :
    if len(line_tmp.group(1)) > 0 and line_tmp.group(1) not in set_d2 :
      set_d2.append(line_tmp.group(1)) #set_d2
    continue

  if normSeries[::-1].find("下"[::-1]) == 0 and normSeries[::-1].find("在下"[::-1]) == -1 and normSeries[::-1].find("天下"[::-1]) == -1 and normSeries[::-1].find("殿下"[::-1]) == -1 and normSeries[::-1].find("1下"[::-1]) == -1 and normSeries[::-1].find("陛下"[::-1]) == -1 and normSeries[::-1].find("之下"[::-1]) == -1 :
    line_tmp = re.search(r'^(.*?)下$', normSeries, re.I)
    if len(line_tmp.group(1)) > 0 and line_tmp.group(1) not in set_d3 :
      set_d3.append(line_tmp.group(1))
    continue

  line_tmp = re.search(r'^(.*?)([^a-zA-Z0-9\+])\d$', normSeries, re.I)
  if line_tmp :
    if normSeries[::-1].find("送"[::-1]) == 1 or normSeries[::-1].find("小"[::-1]) == 1 or normSeries[::-1].find("上"[::-1]) == 1 or normSeries[::-1].find("高"[::-1]) == 1 or normSeries[::-1].find("大"[::-1]) == 1 or normSeries[::-1].find("老"[::-1]) == 1 or normSeries[::-1].find("不"[::-1]) == 1 or normSeries[::-1].find("点"[::-1]) == 1 or normSeries[::-1].find("初"[::-1]) == 1 or normSeries[::-1].find("第"[::-1]) == 1 or normSeries[::-1].find("之"[::-1]) == 1 or normSeries[::-1].find("乔"[::-1]) == 1 or normSeries[::-1].find("于"[::-1]) == 1 or normSeries[::-1].find("为"[::-1]) == 1 or normSeries[::-1].find("太"[::-1]) == 1 or normSeries[::-1].find("唯"[::-1]) == 1 or normSeries[::-1].find("赠"[::-1]) == 1 or normSeries[::-1].find("无"[::-1]) == 1 or normSeries[::-1].find("加"[::-1]) == 1 :
      continue
    tmp = line_tmp.group(1) + line_tmp.group(2)
    if len(line_tmp.group(1)) > 2 and tmp not in set_d4 :
      set_d4.append(tmp)
    continue

######################################################
for line in sets :
  line_arr = line.split('\t')
  gid = line_arr[0]
  feeFlag = line_arr[1]
  viewCount = line_arr[2]
  normName = line_arr[3]
  normAuthor = line_arr[4]
  line = line_arr[5]

  flag = 0

  for dd in set_d1 :
    if line.find(dd) != 0 :
      continue
    if line.find(dd + "之") == 0 or line.find(dd + "上") == 0 or line.find(dd + "中") == 0 or line.find(dd + "下") == 0 or line.find(dd + "pr1est") == 0 or line.find(dd + "+") == 0 or line.find(dd + "0") == 0 or line.find(dd + "1") == 0 or line.find(dd + "2") == 0 or line.find(dd + "3") == 0 or line.find(dd + "4") == 0 or line.find(dd + "5") == 0 or line.find(dd + "6") == 0 or line.find(dd + "7") == 0 or line.find(dd + "8") == 0 or line.find(dd + "9") == 0 :
      line = dd
      flag = 1
      break

  for dd in set_d2 :
    if line.find(dd) != 0 :
      continue
    if line.find(dd + "之") == 0 or line.find(dd + "上") == 0 or line.find(dd + "中") == 0 or line.find(dd + "下") == 0 or line.find(dd + "第") == 0 or line.find(dd + "卷") == 0 or line.find(dd + "0") == 0 or line.find(dd + "1") == 0 or line.find(dd + "2") == 0 or line.find(dd + "3") == 0 or line.find(dd + "4") == 0 or line.find(dd + "5") == 0 or line.find(dd + "6") == 0 or line.find(dd + "7") == 0 or line.find(dd + "8") == 0 or line.find(dd + "9") == 0 or line.find(dd + "part") == 0:
      line = dd
      flag = 1
      break

  for dd in set_d3 :
    if line.find(dd) != 0 :
      continue

    if line.find(dd + "上") == 0 or line.find(dd + "中") == 0 or line.find(dd + "下") == 0 or line.find(dd + "0") == 0 or line.find(dd + "1") == 0 or line.find(dd + "2") == 0 or line.find(dd + "3") == 0 or line.find(dd + "4") == 0 or line.find(dd + "5") == 0 or line.find(dd + "6") == 0 or line.find(dd + "7") == 0 or line.find(dd + "8") == 0 or line.find(dd + "9") == 0 :
      line = dd
      flag = 1
      break

  for dd in set_d4 :
    if line.find(dd) != 0 :
      continue

    if line.find(dd + "上") == 0 or line.find(dd + "中") == 0 or line.find(dd + "下") == 0 or line.find(dd + "0") == 0 or line.find(dd + "1") == 0 or line.find(dd + "2") == 0 or line.find(dd + "3") == 0 or line.find(dd + "4") == 0 or line.find(dd + "5") == 0 or line.find(dd + "6") == 0 or line.find(dd + "7") == 0 or line.find(dd + "8") == 0 or line.find(dd + "9") == 0 :
      #line = dd.replace("\+", "+")
      line = dd
      flag = 1
      break

  tmp = re.sub(r'黑岩$', '', line)
  if len(tmp) <= 0 or tmp.isspace() :
    tmp = line
  f2.writelines(gid + "\t" + feeFlag + "\t" + viewCount + "\t" + normName + "\t" + normAuthor + "\t" + tmp + "\n")

f1.close()
f2.close()
