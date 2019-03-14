package com.easou.dingjing.statistic.day

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD

import scala.util.matching.Regex
import scala.collection.mutable.Set
import scala.collection.mutable.Map
import scala.collection.mutable.ArrayBuffer

import com.easou.dingjing.library.ReadEvent

object ReadEvent {
  def main(args: Array[String]): Unit = {
//    val bilogPath = args(0)
    val bilogPath = "hdfs://10.26.29.210:8020/user/hive/warehouse/event_info.db/b_read_chapter/ds=2019-03-12/*"
    val savePath = "hdfs://10.26.26.145:8020/rs/dingjing/demo"

    val conf = new SparkConf().setAppName("day_statistic")
                        .set("spark.executor.memory", "20g")
                        .set("spark.driver.memory", "4g")
                        .set("spark.cores.max", "10")
    val sc = new SparkContext(conf)
    val logRDD = sc.textFile(bilogPath)
                        .map(parse_log)
                        .filter(line=> line._2(0)._1 != "")
                        .filter(line=> line._2(0)._2 != "")
                        .reduceByKey((x, y) => x ::: y )
    logRDD.map(statistic)
        .filter(x => x != "")
        .repartition(1)
        .saveAsTextFile(savePath)
    sc.stop()
  }

  def statistic(x: Tuple2[String, List[Tuple3[String, String, String]]]): String = {

    var gids = Set[String]()
    val users = Set[String]()

    var gid = ""
    var user = ""

    for (info <- x._2) {
      gid = info._1
      user = info._2
      gids.add(gid)
      users.add(user)
    }

    return "" + x._1.replace("|", "\t") + "\t" + gids.toArray.length.toString + "\t" + users.toArray.length.toString + "\t" + x._2.toArray.length.toString
  }

  def parse_log(x : String) : Tuple2[String, List[Tuple3[String, String, String]]] = {
    val re = new ReadEvent().parseLine(x).getValues(List[String]("appid", "userlevel", "userarea",
                    "usertype", "isnewuser", "status", "booktype", "gid", "uid", "appudid",
                    "sort", "cpid", "ischapterincharged", "entrance"))
    var appid = re(0)                       // app 10001  10003  20001  20002  40001
    var userLevel = re(1)                   // 用户级别 --------------> 0 1
    var userArea = re(2)                    // 用户地区 --------------> 1 2 3 4
    var userType = re(3)                    // 用户类型 --------------> 包月 非包月
    var isNewUser = re(4)                   // 是否新用户  -----------> 1 2
    var bookStatus = re(5)                  // 书籍 连载/完结 状态 ---> 全本 完结 连载
    var bookType = re(6)                    // 书籍类别 --------------> 一折书籍 免费CP书  免费互联网书  包月  按章计费  断更  普通  赠书  限免  非包月

    var gid = re(7)                         // --> 书籍量
    var uid = re(8)                         // --> 用户量
    var appudid = re(9)
    var sort = re(10)                       // --> 章节量
    var cpid = re(11)
    var isChapterCharged = re(12)           // --> 付费章节量 --------> no NO yes YES 付费 免费 限免

    var entrance = re(13)                   // 入口 ------------------>下载通知栏 书友圈详情页 书架 书架-下载 书架-历史 书架页 免费 分类 包月-搜索结果页 封面 封面页 封面页目录 帖子详情页  我的足迹  搜书  搜索  搜索提示页-top榜  搜索提示页-直达  搜索结果页
                                            // 搜索结果页-一般词  搜索结果页-作者  搜索结果页-历史词 搜索结果页-标签 搜索结果页-联想-作者 搜索结果页-联想词 目录 目录页 章末页 精选  缓冲管理  缓冲管理页  网页书籍封面页  起始页

    var key = ""
    if (appid == "") {
      appid = "其它"
    }
    if (userLevel == "") {
      userLevel = "其它"
    }
    if (userArea == "") {
      userArea = "其它"
    }
    if (userType == "") {
      userType = "其它"
    }
    if (isNewUser == "") {
      isNewUser = "其它"
    }
    if (bookStatus != "连载") {
      bookStatus = "完结"
    } else if (bookStatus == "") {
      bookStatus = "其它"
    }
    if(bookType == "") {
      bookType = "其它"
    }
    if ((uid != "") && (uid != "0")) {
      key = uid
    } else {
      key = appudid
    }
    if(sort == "") {
      sort = "0"
    }
    if (cpid == "") {
      cpid = "其它"
    }
    if (isChapterCharged.toLowerCase == "yes") {
      isChapterCharged = "付费"
    } else if (isChapterCharged.toLowerCase == "no") {
      isChapterCharged = "免费"
    } else if (isChapterCharged == "") {
      isChapterCharged = "其它"
    }

    return (appid+"|"+userLevel+"|"+userArea+"|"+userType+"|"+isNewUser+"|"+bookStatus+"|"+bookType+"|"+isChapterCharged, List(Tuple3(gid, key, sort)))
  }
}