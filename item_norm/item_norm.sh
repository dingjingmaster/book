#!/bin/bash
. ~/.bashrc
. ~/.bash_profile
. shell_function
today=`date -d "-0 day" +%Y-%m-%d`
workPath=$(cd $(dirname $0); pwd)

#today="2019-02-13"

export GOPATH="${workPath}/sim/esti_simarity/"
export JAVA_OPTS="-Xms512m -Xmx4G"
export CLASSPATH=".:jar/:lib/:${CLASSPATH}"

debug=false
tableName="item_info"
log="${workPath}/inject_log.log"
sparkMaster="spark://qd01-tech2-spark001:7077,qd01-tech2-spark002:7077"

globalSavePath="hdfs://10.26.26.145:8020/rs/dingjing/item_norm/${today}/"                                           # hadoop 相似度相关
freeChapter=`hadoop fs -ls "hdfs://10.26.26.145:8020/rs/cn/*/free_*" | tail -n 1 | awk -F' ' '{print $8}'`          # 免费书章节信息
chargeChapter=`hadoop fs -ls "hdfs://10.26.26.145:8020/rs/cn/*/cp_*" | tail -n 1 | awk -F' ' '{print $8}'`          # 付费书章节信息
itemInfo="hdfs://10.26.26.145:8020/rs/iteminfo/current/"                                                            # Hadoop 物品信息
chapterPath="${globalSavePath}/chapter_info"                                                                        # Hadoop 保存处理过的章节信息

getNameAuthor="${workPath}/resource/gid_name_author.txt"                                                            # 归一化开始: 拉取 gid name author
ruleWhiteList="${workPath}/rule/bin/white_list.txt"                                                                 # 规则归一 白名单
seriesWhiteList="${workPath}/rule/bin/series_white_list.txt"
ruleResult="${workPath}/resource/rule_result.txt"
ruleResult1="${workPath}/resource/rule_result1.txt"
localItemInfo="${workPath}/resource/item_info.txt"
localMaybeSim="${workPath}/resource/maybe_sim_gid.txt"
hadoopMaybeSim="${globalSavePath}/maybe_sim_gid"
localmaybeSim="${workPath}/resource/gid_sim.txt"
whiteGid="./white_list/white_list_gid.txt"
whitePair="./white_list/white_list_pair.txt"
whiteSubstr="./white_list/white_list_substr.txt"
simResult="${workPath}/resource/sim_result.txt"
finallyResult="${workPath}/resource/finally_result.txt"
allgidsPath="${workPath}/resource/all_gids.txt"

sparkJar="${workPath}/sim/calc_similarity/jar/item_norm.jar"
sparkClass="com.easou.dingjing.itemnorm.Jaccard"
sparkConf=" --driver-memory 4g --class ${sparkClass} --master ${sparkMaster} ${sparkJar}"
if ${debug}
then
    cd ${workPath}/sim/calc_similarity/
    rm jar -fr && mkdir jar
    sbt package
    mv ./target/scala-*/*.jar ${sparkJar}
    rm ./target -fr
    rm ./project -fr
fi
d1=`date`
if true
then
rm -fr "${workPath}/resource"
mkdir "${workPath}/resource"
hadoop fs -cat "${itemInfo}*" | awk -F'\t' '{print $1"\t"$31"\t"$25"\t"$3"\t"$9}' > "${getNameAuthor}"
hadoop fs -cat "${itemInfo}*" | awk -F'\t' '{if ($51 != "111111111") print $1"\t"$5"\t"$11}' > ${localItemInfo}
hadoop fs -mkdir -p "${hadoopMaybeSim}"
python2 ${workPath}/rule/bin/norm_title_author.py ${getNameAuthor} ${ruleWhiteList} ${ruleResult1}
python2 ${workPath}/rule/bin/norm_series.py "${seriesWhiteList}" ${ruleResult1} ${ruleResult}

cd ${workPath}/sim/chapter_dispose
rm libs.zip
zip -r ./libs.zip ./*
spark-submit --py-files libs.zip dispose_chapter.py "${whiteGid}" "${whitePair}" "${whiteSubstr}" "${chargeChapter}" "${freeChapter}" "${itemInfo}" "${chapterPath}"
cd ${workPath}
hadoop fs -cat "${chapterPath}/*" | awk -F'\t' '{print $1}' > "${allgidsPath}"

cd ${workPath}/sim/esti_simarity
go build ./src/main/main.go
./main "${workPath}/sim/esti_simarity/"
hadoop fs -put "${localMaybeSim}" "${hadoopMaybeSim}"

cd ${workPath}/sim/calc_similarity/
spark-submit ${sparkConf} "${globalSavePath}"

cd ${workPath}/union
hadoop fs -cat "${globalSavePath}/sim_result/*" | awk -F'\t' '{if($3>=0.5) print $1"\t"$2"\t"$3}' > "${simResult}"
python2 union2.py "${ruleResult}" "${simResult}" "${finallyResult}"

cd ${workPath}
hdfs_exist "${globalSavePath}/sim_result/"
if [ $? -eq 0 ]
then
    java -jar jar/InjectNormNameAuthor.jar "${finallyResult}" "${log}" "${tableName}"
fi
fi
d2=`date`
echo $d1
echo $d2



