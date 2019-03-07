#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys


def get_item_info(itemInfoPath, itemInfoDict, ruleResultDict):
	with open(itemInfoPath, 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line = line.strip()
			arr = line.split('\t')
			if len(arr) != 6:
				continue
			gid = arr[0]
			fee = arr[1]
			view = arr[2]
			name = arr[3]
			author = arr[4]
			series = arr[5]
			key = name + '|' + author
			itemInfoDict[gid] = (fee, view, name, author, series)
			if key in ruleResultDict:
				ruleResultDict[key].add(gid)
			else:
				m = set()
				m.add(gid)
				ruleResultDict[key] = m
	return


def get_sim_result(mpath: str, mdict: dict):
	with open(mpath, 'r', encoding='utf8') as fr:
		for line in fr.readlines():
			line = line.strip()
			arr = line.split('\t')
			for gid in arr[:2]:
				if gid in mdict:
					mdict[gid] = mdict[gid] | set(arr[:2])
				else:
					mdict[gid] = set(arr[:2])
	return


def chose_sim_result(itemInfoDict, simDict, simGroup):
	for gid, iv in simDict.items():
		if gid not in itemInfoDict:
			continue
		choseCharge = ('', 0)           # gid view
		choseFree = ('', 0)             # gid view
		for mgid in iv:
			if mgid not in itemInfoDict:
				continue
			mfee, mview, mname, nauthor, mseries = itemInfoDict[mgid]
			if int(mfee) == 1:
				cgid, cview = choseCharge
				if int(mview) >= cview:
					choseCharge = (mgid, int(mview))
			else:
				fgid, fview = choseFree
				if int(mview) >= fview:
					choseFree = (mgid, int(mview))
		if choseCharge[0] != '':
			for rgid in iv:
				simGroup[rgid] = choseCharge[0]
		elif choseFree[0] != '':
			for rgid in iv:
				simGroup[rgid] = choseFree[0]
	return


def out_sim_rule(mpath, ruleDict, simDict, simGroup, itemInfo):
	resultDict = {}
	for ik, iv in ruleDict.items():
		for gid in iv:
			resultDict[gid] = iv
	""" 整合相似度 """
	for ik, iv in simDict.items():
		if ik in resultDict:
			resultDict[ik] |= iv
		else:
			resultDict[ik] = set(iv)
	filter = {}
	for ik, iv in resultDict.items():
		ml = list(set(iv))
		ml.sort()
		filter['|'.join(ml)] = 0
	# 输出结果
	allGid = {}
	with open(mpath, 'w', encoding='utf8') as fw:
		for ik, iv in filter.items():
			arr = ik.split('|')
			tgid, name, author, series = '', '', '', ''
			for igid in arr:
				if (igid in simGroup) and (igid in itemInfoDict):
					tgid = simGroup[igid]
					break
			if '' != tgid:
				mfee, mview, name, author, series = itemInfoDict[tgid]
				for ig in arr:
					if ig in allGid:
						continue
					allGid[ig] = 0
					fw.write(ig + '\t' + name + '\t' + author + '\t' + series + '\n')
		# 未成对 或 规则的输出
		for ik, iv in itemInfoDict.items():
			if ik in allGid:
				continue
			allGid[ik] = 0
			mfee, mview, name, author, series = iv
			fw.write(ik + '\t' + name + '\t' + author + '\t' + series + '\n')
	return


"""
	先用 shell 对相似度结果做一个初步过滤，过滤出相似度>=0.5的组
	相似度归一化结果的组合
		1. 读取相似度的结果
		2. 相似度结果合并
		3. 读取物品信息
		4. 选取相似度的 归一化结果
"""
if __name__ == '__main__':
	workDir = '/'.join(sys.argv[0].split('/')[:-1])
	itemInfoPath = sys.argv[1]
	simResultPath = sys.argv[2]
	simGroupResultPath = sys.argv[3]
	# simResultPath = workDir + '/../resource/sim_result.txt'
	# itemInfoPath = workDir + '/../resource/rule_result.txt'
	# simGroupResultPath = workDir + '/../resource/finally_sim_result.txt'

	itemInfoDict = {}
	simResultDict = {}
	ruleResultDict = {}
	simGidMapping = {}                                                  # 为每个相似度结果选中一个 gid

	get_item_info(itemInfoPath, itemInfoDict, ruleResultDict)           # 读取物品信息 + 规则归一结果
	get_sim_result(simResultPath, simResultDict)                        # 读取相似度归一结果
	chose_sim_result(itemInfoDict, simResultDict, simGidMapping)        # 相似度归一结果整理
	out_sim_rule(simGroupResultPath, ruleResultDict, simResultDict, simGidMapping, itemInfoDict)
	exit(0)
