/*************************************************************************
> FileName: ./src/main/scala/com/easou/dingjing/library/HBaseOp.scala
> Author  : DingJing
> Mail    : dingjing@live.cn
> Created Time: 2018年05月17日 星期四 09时56分28秒
 ************************************************************************/
package com.easou.dingjing.library

import java.util.{ArrayList, List}
import java.io.{FileWriter, IOException, BufferedReader, File, FileReader}

import scala.collection.mutable.{Map}
import scala.collection.JavaConversions._

import org.apache.hadoop.hbase.util.Bytes
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.hbase.{HBaseConfiguration, KeyValue=>HKV}
import org.apache.hadoop.hbase.client.{Put, Result, ResultScanner, Scan, HTable}

import com.easou.dingjing.library.{KeyValue=>JKV}

class HBaseOp {
  private var tableName = ""
  private var hbaseconf = HBaseConfiguration.create()
  hbaseconf.set("hbase.zookeeper.quorum", "moses.namenode01,moses.datanode10,moses.datanode11,moses.datanode12,moses.datanode13")
  hbaseconf.set("hbase.zookeeper.property.clientPort", "2181")
  private var htable: HTable = null
  private var resultList = new ArrayList[Map[String, String]]()
  private var putList = new ArrayList[Put]()


  def setTableName (tn: String): HBaseOp = {
    tableName = tn

    return this
  }


  def open (): Boolean = {
      close()
      htable = new HTable(hbaseconf, tableName)
      if (null != htable) {
        return true
      }

      return false
  }


  def close (): Unit = {
    if (null != htable) {
      htable.close()
    }
  }


  private def commit(): Boolean = {
    if (null == htable) {
      println ("错误")
    }
    try {
      if (putList.size() > 0) {
        htable.put(putList)
        putList.clear()
        return true
      }
    } catch {
      case ex: IOException => {println(ex.getMessage())}
    }

    return false
  }


  private def addRow(row: String, family: String, column: String, value: String): Unit = {
    val p = new Put(Bytes.toBytes(row))
    p.add(Bytes.toBytes(family), Bytes.toBytes(column), Bytes.toBytes(value))
    putList += p
  }


  def inject(row: String, family: String, keyValue: Map[String, String]): Boolean = {

    for (i <- keyValue.iterator) {
      addRow(row, family, i._1, i._2)
    }
    if (commit()) {
      return true
    }

    return false
  }


  def inject(row: String, family: String, key: String, value: String): Boolean = {

    addRow(row, family, key, value)
    if (commit()) {
      return true
    }

    return false
  }


  def scanResult(family: String, filed: Seq[String]): HBaseOp = {

    var scan: Scan = null
    var scanner: ResultScanner = null
    try {
      scan = new Scan()
      for (i <- filed.toList) {
        scan.addColumn(Bytes.toBytes(family), Bytes.toBytes(i))
      }
      scanner = htable.getScanner(scan)
      var flag = true
      while(flag) {
        val res = scanner.next()
        if (res != null) {
          var resultLine = Map[String, String]()
          resultLine("rowkey") = Bytes.toString(res.getRow())
          for (kv <- res.list()) {
            resultLine(Bytes.toString(kv.getQualifier())) = Bytes.toString(kv.getValue())
          }
          resultList += resultLine
        } else {
          flag = false
        }
      }
    } catch {
      case ex: IOException => {println("error: " + ex.getMessage())}
    } finally {
    }

    return this
  }


  def scanToFile (path: String, family: String, filed: Seq[String]): Unit = {

    val jkv = new JKV()
    val fw = new FileWriter(path)
    var scanner: ResultScanner = null
    var resultTmp = new ArrayList[Map[String, String]]()
    try {
      val fw = new FileWriter(path)
      val scan = new Scan()
      for (i <- filed.toList) {
        scan.addColumn(Bytes.toBytes(family), Bytes.toBytes(i))
      }
      scanner = htable.getScanner(scan)
      var flag = true
      while(flag) {
        val res = scanner.next()
        if (res != null) {
          var resultLine = Map[String, String]()
          resultLine("rowkey") = Bytes.toString(res.getRow())
          for (kv <- res.list()) {
            resultLine(Bytes.toString(kv.getQualifier())) = Bytes.toString(kv.getValue())
          }
          resultTmp += resultLine
          if (resultTmp.length >= 1000) {
            writeFile (fw, resultTmp)
          }
        } else {
          flag = false
        }
      }
    } catch {
      case ex: IOException => {println("error: " + ex.getMessage())}
    } finally {
      writeFile (fw, resultTmp)
    }
  }


  def scanValueToFile (path: String, family: String, filed: Seq[String]): Unit = {

    val jkv = new JKV()
    val fw = new FileWriter(path)
    var scanner: ResultScanner = null
    var resultTmp = new ArrayList[Map[String, String]]()
    try {
      val fw = new FileWriter(path)
      val scan = new Scan()
      for (i <- filed.toList) {
        scan.addColumn(Bytes.toBytes(family), Bytes.toBytes(i))
      }
      scanner = htable.getScanner(scan)
      var flag = true
      while(flag) {
        val res = scanner.next()
        if (res != null) {
          var resultLine = Map[String, String]()
          resultLine("rowkey") = Bytes.toString(res.getRow())
          for (kv <- res.list()) {
            resultLine(Bytes.toString(kv.getQualifier())) = Bytes.toString(kv.getValue())
          }
          resultTmp += resultLine
          if (resultTmp.length >= 1000) {
            writeFile (fw, resultTmp, filed.toList)
          }
        } else {
          flag = false
        }
      }
    } catch {
      case ex: IOException => {println("error: " + ex.getMessage())}
    } finally {
      writeFile (fw, resultTmp, filed.toList)
      fw.close()
    }
  }


  def writeFile(fw: FileWriter, list: List[Map[String, String]], key: List[String]): Unit = {
    val jkv = new JKV()
    try {
      for (i <- list) {
        fw.write(jkv.valueLine(i, key.toList) + "\n")
      }
    } catch {
      case ex: IOException => {println(ex.getMessage())}
    } finally {
      list.clear()
    }
  }


  def writeFile(fw: FileWriter, list: List[Map[String, String]]): Unit = {
    val jkv = new JKV()
    try {
      for (i <- list) {
        fw.write(jkv.KVLine(i) + "\n")
      }
    } catch {
      case ex: IOException => {println(ex.getMessage())}
    } finally {
      list.clear()
    }
  }


  def writeFile(fw: FileWriter): Int = {

    val jkv = new JKV()
    try {
      for (i <- resultList) {
        fw.write(jkv.KVLine(i) + "\n")
      }
    } catch {
      case ex: IOException => {println(ex.getMessage())}
    } finally {
    }

    return resultList.length
  }

}
