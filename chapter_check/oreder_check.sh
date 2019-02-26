#!/usr/bin/env bash

# 获取天阅读量 top 10000 的书籍
hadoop fs -cat hdfs://10.26.26.145:8020/rs/iteminfo/2019-02-25/item_1551033217/part-00000 | awk -F'\t' '{if($3!=""&&$9!=""&&$31=="1")print $1"\t"$75}' | sort -nk 2 -r | less