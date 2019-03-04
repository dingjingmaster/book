#!/bin/bash
source ~/.bash_profile
source ~/.bashrc

. shell_global_variable
. shell_function

workDir=$(cd $(dirname $0); pwd)
today=`date -d "-1 day" +%Y-%m-%d`
#today="2018-04-10"

itemInfoPath="${item_info_path}"
sparkRun="spark-submit --total-executor-cores=30 --executor-memory=18g --py-files libs.zip"
biReadLog="${bi_read_chapter_base_path}${today}/*"
itemChapterPurchase="${item_purchase_base_path}/${today}/"
itemChapterRead="${item_read_base_path}/${today}/"
localBuyPath="data/item_buy.txt"
localReadPath="data/item_read.txt"
buyResultPath="data/buy_result.txt"
readResultPath="data/read_result.txt"

###################     开始执行      ###########################
for((i=0;i<20;++i))
do
    # 解析日志 购买
    hdfs_exist "${itemChapterPurchase}"
    if [ $? -ne 0 ]
    then
        cd ${workDir}/bin/ && rm -fr libs.zip && zip libs.zip ./*
        ${sparkRun} item_buy.py ${itemInfoPath} ${biReadLog} ${itemChapterPurchase}
        sleep 3
        continue
    fi

    # 解析日志 阅读
    hdfs_exist "${itemChapterRead}"
    if [ $? -ne 0 ]
    then
        cd ${workDir}/bin/ && rm -fr libs.zip && zip libs.zip ./*
        ${sparkRun} item_read.py ${itemInfoPath} ${biReadLog} ${itemChapterRead}
        sleep 3
        continue
    fi

    break
done

# 统计邮件
cd ${workDir}
rm -fr data && mkdir data
hadoop fs -cat "${itemChapterPurchase}/*" > ${localBuyPath}
hadoop fs -cat "${itemChapterRead}/*" > ${localReadPath}

python send_email/generate_buy_email.py "${localBuyPath}" "${buyResultPath}"
python send_email/generate_read_email.py "${localReadPath}" "${readResultPath}"

if true
then
file_empty "${buyResultPath}"
if [ $? -eq 0 ]
then
    summary='<br><li>本邮件统计的购买实际是指对付费章节的阅读(基于阅读事件而不是购买事件统计)</li><li>不是从书架进入的购买用户不做统计</li><li>书籍量: 付费章节被阅读的书籍总数</li><li>付费章节阅读人数: 每本书籍的付费章节阅读人数之和</li><li>付费章节阅读量数: 每本书的付费章节阅读量之和</li>'
    sh send_email/auto_email.sh "天付费章节阅读量统计" "${today}" "${buyResultPath}" "${summary}"
fi
fi

if true
then

file_empty "${readResultPath}"
if [ $? -eq 0 ]
then
    summary='<br><li>不是从书架进入的阅读用户不做统计</li><li>书籍量: 天阅读的书籍总数</li><li>阅读量: 每本书籍的天阅读人数之和</li><li>阅读章节数: 每本书的天阅读章节数之和</li>'
    sh send_email/auto_email.sh "天阅读量统计" "${today}" "${readResultPath}" "${summary}"
fi
fi
exit 0
