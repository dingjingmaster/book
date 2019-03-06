/*************************************************************************
> FileName: com/easou/dingjing/library/test/HBaseOpTest.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年05月17日 星期四 11时48分54秒
 ************************************************************************/
package com.easou.dingjing.library.test

import com.easou.dingjing.library.HBaseOp
import scala.collection.mutable.Map

object HBaseOpTest {
  def main(args: Array[String]): Unit = {
    if (args.length != 1) {
      System.exit(1)
    }
    val path = args(0)
    val hb = new HBaseOp()
    hb.setTableName("item_info").open()
    hb.scanValueToFile(path, "x", Seq("rowkey", "name", "name"))
  }
}

