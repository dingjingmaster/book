/*************************************************************************
> FileName: com/easou/dingjing/hbase/GetItemInfo.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年05月17日 星期四 18时43分58秒
 ************************************************************************/
package com.easou.dingjing.hbase
  
import com.easou.dingjing.library.{HBaseOp => JHBOP}

object GetItemInfo {
  def main(args: Array[String]): Unit = {
    if (args.length != 1) {
      println("请输入写出的文件名")
      System.exit(1)
    }
    val hbase = new JHBOP()
    if (hbase.setTableName("item_info").open()) {
      hbase.scanValueToFile(args(0), "x", Seq("rowkey", "name", "author"))
    } else {
      println("hbase 打开失败")
    }
    hbase.close()
  }
}

