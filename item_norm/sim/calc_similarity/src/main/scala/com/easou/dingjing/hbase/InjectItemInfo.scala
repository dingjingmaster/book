/*************************************************************************
> FileName: com/easou/dingjing/hbase/InjectItemInfo.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年05月18日 星期五 11时12分08秒
 ************************************************************************/
package com.easou.dingjing.hbase
  
import com.easou.dingjing.library.{HBaseOp => JHBOP}

import scala.io.Source
import scala.collection.mutable.{ListBuffer, Map}

object InjectItemInfo {
  def main(args: Array[String]): Unit = {
    if (args.length != 1) {
      println("请输入要注入文件名")
      System.exit(1)
    }
    val hbase = new JHBOP()
    if (hbase.setTableName("item_info").open()) {

      val lb = ListBuffer[String]()
      Source.fromFile(args(0)).getLines().foreach((x) => {
        val arr = x.split("\t")
        if ((arr(0).slice(0,2) == "i_") && (arr.length >= 4)) {
          hbase.inject(arr(0), "x", Map[String, String]("norm_name"->arr(1), "norm_author"->arr(2), "norm_series"->arr(3)))
        } else {
          println("error line: " + x)
        }
      })

    } else {
      println("hbase 打开失败")
    }
    hbase.close()
  }
}

// addRow(row: String, family: String, column: String, value: String)
