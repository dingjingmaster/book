/*************************************************************************
> FileName: KeyValueTest.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年05月16日 星期三 11时58分08秒
 ************************************************************************/
package com.easou.dingjing.library.test;

import com.easou.dingjing.library.{KeyValue=>KV};
import scala.collection.mutable.Map


object KeyValueTest{
  def main (args : Array[String]) : Unit = {
    val kv = new KV()
    val m = Map[String, String]("key1"->"value1", "key2"->"value2")
    val line = kv.KVLine(m)
    //val line = kv.KVLine(Map[String, String]())
    println(line)
    println(kv.parseLine(line).getValues(List("key1", "key2")))
    println(kv.valueLine(m, List("key1", "key2"), "\t"))
  }
}


