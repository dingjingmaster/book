#!/bin/bash
. ~/.bashrc
. ~/.bash_profile

workDir=$(cd $(dirname $0); pwd)
today=`date -d "-1 day" +%Y-%m-%d`

biLogPath="hdfs://10.26.29.210:8020/user/hive/warehouse/event_info.db/b_read_chapter/ds=${today}"
savePath="hdfs://10.26.26.145:8020/rs/dingjing/static/read_day/${today}/"

cd ${workDir}/jar
spark-submit --class com.easou.dingjing.statistic.day.ReadEvent ./read_statistic.jar "${biLogPath}" "${savePath}"
