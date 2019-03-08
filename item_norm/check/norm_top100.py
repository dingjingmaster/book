#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
	输入：
		itemInfoPath 格式： gid \t 天阅读量
		resultPath 格式：gid normName normAuthor normSeries
"""

if __name__ == '__main__':
	chapterPath = '../resource/chapter.txt'
	outPath = '../resource/check_top100.txt'
	itemInfoPath = '../resource/item_rnd.txt'
	resultPath = '../resource/finally_result.txt'

	itemNorm = {}
	itemChapter = {}
	itemInfoDict = {}
	with open(itemInfoPath, 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line = line.strip('\n')
			arr = line.split('\t')
			if len(arr) != 2:
				continue
			gid = arr[0]
			rnd = arr[1]
			itemInfoDict[gid] = int(rnd)

	with open(resultPath, 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line = line.strip('\n')
			arr = line.split('\t')
			if len(arr) != 4:
				continue
			gid = arr[0]
			name = arr[1]
			author = arr[2]
			series = arr[3]
			key = name + '|' + author
			if key in itemNorm:
				itemNorm[key].add(gid)
			else:
				m = set()
				m.add(gid)
				itemNorm[key] = m

	top100List = []
	for ik, iv in itemNorm.items():
		if len(iv) < 2:
			continue
		num = 0
		for j in iv:
			if j in itemInfoDict:
				num += itemInfoDict[j]
		top100List.append(('|'.join(list(iv)), num, ik))
	top100List.sort(key=lambda x: x[1], reverse=True)
	top100List = top100List[:100]

	itemChapter = {}
	with open(chapterPath, 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line = line.strip('\n')
			arr = line.split('\t')
			gid = arr[0]
			view = arr[1]
			chapter = arr[2]
			itemChapter[gid] = (view, chapter)

	fw = open(outPath, 'w', encoding='utf8')
	for i in top100List:
		arr = i[0].split('|')
		fw.write('(' + i[2] + ')' + i[0] + '\n')
		for gid in arr:
			if gid in itemChapter:
				fw.write('\t\t' + gid + '\t' + itemChapter[gid][1] + '\n')
			else:
				fw.write('\t\t' + gid + '\n')
		fw.write('\n\n')
	fw.close()
	exit(0)
