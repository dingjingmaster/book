/*************************************************************************
> FileName: ./src/main/scala/com/easou/dingjing/itemnorm/ItemPair.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年10月24日 星期三 00时26分37秒
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

object ItemPair {
  def main(args: Array[String]): Unit = {
    if (args.length != 4) {
      System.exit(1)
    }

    val itemInfoPath = args(0)
    val freeChapterPath = args(1)
    val chargeChapterPath = args(2)
    val saveBasePath = args(3)

    val sparkConf = new SparkConf().setAppName("item_norm")
                        .set("spark.executor.memory", "20g")
                        .set("spark.cores.max", "30")

    val sc = new SparkContext(sparkConf)

    val itemInfoRDD = sc.textFile(itemInfoPath)
                        .map(x => x.split("\t", -1))
                        .filter(x => x.length > 50)
                        .filter(x => x(50) != "111111111")
                        .map(x => (x(0), (x(2), x(8))))
                        .filter(x => x._1.length > 4)
                        .map(x => x._1 + "\t" + x._2._1 + "\t" + x._2._2)
                        .zipWithIndex()

    itemInfoRDD.map(x => x._1 + "\t" + x._2)
                        .saveAsTextFile(saveBasePath + "/gid_info/")

    /*val freeChapterRDD = sc.textFile(freeChapterPath)
                        .map(x => x.split("\\{\\]", -1))
                        .map(detail_free)
                        .filter(x => x._1 != "")
                        .join(itemInfoRDD)
                        .map(x => (x._1, (x._2._2, x._2._1)))

    val chargeChapterRDD = sc.textFile(chargeChapterPath)
                        .map(x => x.split("\\{\\]", -1))
                        .map(detail_charge)
                        .filter(x => x._1 != "")
                        .join(itemInfoRDD)
                        .map(x => (x._1, (x._2._2, x._2._1)))

    val gidChapterRDD = chargeChapterRDD.union(freeChapterRDD)

    gidChapterRDD.map(x => x._1 + "\t" + x._2._1 + "\t" + x._2._2.mkString("{]"))
                        .saveAsTextFile(saveBasePath + "/gid_info/")
    */

  }

  def detail_charge(x: Array[String]): Tuple2[String, List[String]] = {
    var gid = x(1)
    var res = Array[String]()
    var ctemp = ArrayBuffer[String]()
    val loop = new Breaks

    if (x.length > 3) {
      var clist = x.slice(1, x.length - 1)
      if (clist.length > 22) {
        loop.breakable {
          for (i <- 1 to clist.length) {
            // 對章節進行處理
            //
            ctemp.append(clist(i))
            if (ctemp.length >= 20) {
              loop.break
            }
          }
        }
        res = ctemp.toArray
      } else {
        res = clist
      }
    } else {
      gid = ""
      res = null
    }
        
    return (gid, res.toList)
  }



  def detail_free(x: Array[String]): Tuple2[String, List[String]] = {
    var gid = x(1)
    var res = Array[String]()
    val ctemp = ArrayBuffer[String]()
    val loop = new Breaks

    if (x.length > 3) {
      var clist = x.reverse.slice(0, x.length - 2)
      if (clist.length > 22) {
        loop.breakable {
          for (i <- 1 to clist.length) {
            // 對章節進行處理
            //
            ctemp.append(clist(i))
            if (ctemp.length >= 20) {
              loop.break
            }
          }
        }
        res = ctemp.toArray
      } else {
        res = clist
      }
    } else {
      gid = ""
      res = null
    }
        
    return (gid, res.toList)
  }


}

