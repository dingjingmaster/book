/*************************************************************************
> FileName: com/easou/dingjing/ItemInfo.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年04月17日 星期二 14时46分06秒
 ************************************************************************/
package com.easou.dingjing.library;

import scala.collection.mutable.Map;
import scala.collection.mutable.ListBuffer;

class ItemInfo() {

  private var gid : String = "";
  private var map = Map[String, String]();


  def parseLine(line : String, token : String="\\t") : ItemInfo = {
    var linea = line.replace("\\r", "");
    linea = linea.replace("\\n", "");

    val arr = line.split(token, -1);
    var i = 0;
    gid = arr(i)

    i = 2;
    while(i < arr.size) {
      map(arr(i - 1).trim()) = arr(i);
      i += 2;
    }
    return this;
  }


  def getKeys() : Iterable[String] = {
    return map.keys;
  }


  def getValue(key : String) : String = {
    var value = "";
    try {
      value = map(key);
    } catch {
      case ex : Throwable => println("查询的key " + key + " 不合理");
    }

    return value;
  }

  def getValues(key : List[String]) : List[String] = {
    var res = ListBuffer[String]();
    if (! key.isEmpty) {
      res += this.gid
      for (i <- key) {
        res += getValue(i)
      }
    }

    return res.toList;
  }



}
