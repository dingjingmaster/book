/*************************************************************************
> FileName: ./spark/src/main/scala/com/easou/dingjing/itemnorm/Jaccard.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年10月29日 星期一 18时29分48秒
 ************************************************************************/
package com.easou.dingjing.itemnorm

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.ml.linalg.{Vectors, SparseVector}
import org.apache.spark.sql.{SparkSession, Row, Dataset, SQLContext}
import org.apache.spark.ml.feature.{HashingTF, IDF, IDFModel, Tokenizer}
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}

import scala.collection.{Seq, Map}
import scala.collection.mutable.{ArrayBuffer}
import scala.reflect.runtime.universe._
import scala.math._
import scala.util.control._



object Jaccard {
  def main (args: Array[String]): Unit = {
    if(args.length != 1) {
      System.exit(1)
    }

    val chapterPath = args(0) + "/chapter_info"
    val maybeSimPath = args(0) + "/maybe_sim_gid"
    val savePath = args(0) + "/sim_result"

    val sparkConf = new SparkConf().setAppName("similarity")
                        .set("spark.executor.memory", "20g")
                        .set("spark.cores.max", "30")

    val sc = new SparkContext(sparkConf)

    val chapterRDD = sc.textFile(chapterPath)
                        .map(x => x.split("\\t", -1))
                        .filter(x => x.length == 3)
                        .map(x => (x(0), x(2)))
                        .filter(x => x._2 != "")

    val maybeSimRDD = sc.textFile(maybeSimPath)
                        .zipWithIndex()
                        .flatMap(gid_index(_))
                        .reduceByKey((x, y) => x ::: y)

    // 获取可能相似书籍的 章节信息
    val gidChapterRDD = maybeSimRDD.join(chapterRDD)

    gidChapterRDD.flatMap(index_gid_chapter(_))
                        .reduceByKey((x, y) => x ::: y)
                        .filter(x => x._2.length == 2)
                        .map(jaccard)
                        .filter(x => x != "")
                        .saveAsTextFile(savePath)

  }

  def jaccard(x: Tuple2[String, List[String]]): String = {

    val xArr = x._2(0).split("\\t", -1)
    val yArr = x._2(1).split("\\t", -1)

    val xgid = xArr(0)
    val ygid = yArr(0)

    val xChapter = xArr(1).split("\\{\\]", -1).toSet
    val yChapter = yArr(1).split("\\{\\]", -1).toSet

    val j = xChapter & yChapter
    val h = xChapter ++ yChapter

    val jl = j.size.toDouble
    val hl = h.size.toDouble

    if (hl <= 0) {
      return "" // xgid + "\t" + ygid + "\t0\t" + xArr(1) + "\t" + yArr(1)
    }

    return xgid + "\t" + ygid + "\t" + (jl / hl).toString // + "\t" + xArr(1) + "\t" + yArr(1)

  }


  def index_gid_chapter(x: Tuple2[String, Tuple2[List[String], String]]) : List[Tuple2[String, List[String]]] = {
    val gid = x._1
    val index = x._2._1
    val chapter = x._2._2

    val res = ArrayBuffer[Tuple2[String, List[String]]]()

    for (indext <- index) {
      res.append((indext, List[String](gid + "\t" + chapter)))
    }

    for (i <- res.toList)
      yield i
  }


  def gid_index(x: Tuple2[String, Long]): List[Tuple2[String, List[String]]] = {
    val arr = x._1.split("\\t", -1)
    val index = x._2
    val res = ArrayBuffer[Tuple2[String, List[String]]]()

    res.append((arr(0), List(index.toString)))
    res.append((arr(1), List(index.toString)))

    for(i <- res.toList)
      yield i
  }
}

