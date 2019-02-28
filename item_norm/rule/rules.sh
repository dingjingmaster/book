#!/bin/sh
source ~/.bashrc
source ~/.bash_profile
export CLASSPATH=.:./jar/*.jar:${CLASSPATH}

WORKDIR=$(cd $(dirname $0); pwd)
todayData=`date -d "-0 day" +%Y-%m-%d`

tableName="item_info"
getNameAuthor="data/gid_name_author.txt"
whiteList="bin/white_list.txt"
result="data/result.txt"
itemInfo="hdfs://10.26.26.145:8020/rs/iteminfo/current/"



# 获取原始书名和作者名
#java -jar ./jar/GetItemNameAndAuthor.jar ${tableName} ${getNameAuthor}
cd ${WORKDIR} && rm -fr data && mkdir data
hadoop fs -cat "${itemInfo}*" | awk -F'\t' '{print $1"\t"$31"\t"$25"\t"$3"\t"$9}' > "${getNameAuthor}"

cd ${WORKDIR}
python2 bin/norm_title_author.py ${getNameAuthor} ${whiteList} ${result}

echo '规则 归一 完成!!!'


