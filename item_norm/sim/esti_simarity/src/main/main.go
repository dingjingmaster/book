package main

import (
	"bufio"
	"fmt"
	"github.com/yanyiwu/gojieba"
	"io"
	"log"
	"norm"
	"os"
	"strings"
	"sync"
	"unicode/utf8"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(-1)
	}

	workPath := os.Args[1]
	/* 切换路径 */
	os.Chdir(workPath)
	gidInfo := workPath + "/../../resource/item_info.txt"
	gidSim := workPath + "/../../resource/maybe_sim_gid.txt"
	allGid := workPath + "/../../resource/all_gids.txt"
	allGidDict := map[string]bool{}
	flag := false                      // 是否读取 章节信息列表
	gidInfoDict := map[string]string{} // gid 关键字
	wordDict := map[string]map[string]bool{}

	wait := sync.WaitGroup{}
	resChan := make(chan string, 100000)
	checkNum := 1000
	if _, err := os.Stat(gidSim); nil != err {
		os.Create(gidSim)
	}
	flag = readGids(allGid, &allGidDict)
	if fw, err := os.OpenFile(gidSim, os.O_WRONLY|os.O_RDONLY, 0770); nil == err {
		defer fw.Close()
		if readFile(gidInfo, &gidInfoDict, &wordDict, flag, &allGidDict) {
			lens := len(gidInfoDict)
			cur := 0

			gidInfoChan := make(chan string, 1)
			go func() {
				for gid, info := range gidInfoDict {
					gidInfoChan <- gid + "\t" + info
					cur++
				}
				close(gidInfoChan)
			}()

			// 计算过的 gid\gid 信息

			// 开始计算相似的 gid  相似度
			for i := 0; i < checkNum; i++ {
				wait.Add(1)
				go func() {
					for {
						if gidInfo, ok := <-gidInfoChan; ok {
							if arr := strings.Split(gidInfo, "\t"); len(arr) == 2 {
								xgid := arr[0]                      //gid
								xtmp := strings.Split(arr[1], "{]") // key word {] name {] author
								xinfo := strings.Split(xtmp[0], "|")

								// 查找 所有可能相似的 gid 。上一步把有关键词的gid都放到一组中
								maybeGid := map[string]bool{}
								for _, kw := range xinfo { // 关键字
									if value, ok := wordDict[kw]; ok {
										for v, _ := range value {
											if xgid != v {
												maybeGid[v] = false
											}
										}
									}
								}

								// 所有可能相似的 gid 与 现有 gid 进行相似度计算
								for ygid, _ := range maybeGid {
									if yInfoTemp, ok := gidInfoDict[ygid]; ok {

										ytmp := strings.Split(yInfoTemp, "{]")
										yinfo := strings.Split(ytmp[0], "|")

										// 书名 或 作者名 相同
										if xtmp[0] == ytmp[0] || xtmp[1] == ytmp[1] || xtmp[1] == ytmp[2] {
											resChan <- fmt.Sprintf("%s\t%s\t%f", xgid, ygid, 0.2)
											continue
										}

										// 计算相似度
										if sim := jaccard(xinfo, yinfo); sim >= 0.2 {
											resChan <- fmt.Sprintf("%s\t%s\t%f", xgid, ygid, sim)
										}
									}
								}
							}
						} else {
							wait.Done()
							break
						}
					}
				}()
			}

			go func() {
				count := 0
				for {
					if res, ok := <-resChan; ok {
						fw.Write([]byte(res + "\n"))
						count++
						if count%1000000 == 0 {
							fmt.Printf("发现相似组数: %d 已完成 %d 共有 %d\n", count, cur, lens)
						}
					}
				}
			}()
		} else {
			log.Println("读取文件错误!")
		}
	} else {
		log.Println("创建文件错误: %s", err)
	}

	wait.Wait()
}

/* 计算相似度 */
func jaccard(name1 []string, name2 []string) float64 {

	name1Map := map[string]bool{}
	namejMap := map[string]bool{}
	namebMap := map[string]bool{}

	for _, i := range name1 {
		name1Map[i] = true
		namebMap[i] = true
	}

	for _, i := range name2 {
		if _, ok := name1Map[i]; ok {
			namejMap[i] = true
		} else {
			namebMap[i] = true
		}
	}

	j := float64(len(namejMap))
	b := float64(len(namebMap))

	if b == 0 {
		b = 1
	}

	return j / b
}

/* 读取gid */
func readGids(file string, gids *map[string]bool) bool {
	retCode := false
	if fr, err := os.Open(file); nil == err {
		defer fr.Close()
		br := bufio.NewReader(fr)
		for {
			line, _, c := br.ReadLine()
			if io.EOF == c {
				retCode = true
				break
			}
			linet := strings.Trim(string(line), "\n")
			(*gids)[linet] = true
		}
	} else {
		fmt.Println("打开gids文件失败")
	}
	return retCode
}

/* 读取数据 */
func readFile(file string, gids *map[string]string, wordDict *map[string]map[string]bool, flag bool, allGid *map[string]bool) bool {

	stopWord := map[string]bool{
		"豪门": false,
		"总裁": false,
		"腹黑": false,
		"高冷": false,
		"侯门": false,
		"名门": false,
		"明少": false,
		"惊世": false,
	}

	ret := false
	if fr, err := os.Open(file); nil == err {
		defer fr.Close()
		jieba := gojieba.NewJieba()
		br := bufio.NewReader(fr)
		for {
			line, _, c := br.ReadLine()
			if io.EOF == c {
				ret = true
				break
			}
			arr := strings.Split(strings.Trim(string(line), "\n"), "\t")
			if len(arr) != 3 {
				continue
			}

			// 有章节信息的 gid 参与计算
			if _, ok := (*allGid)[arr[0]]; flag && !ok {
				continue
			}

			temp1 := jieba.Cut(norm.NormName(arr[1]), true)
			temp2 := jieba.Cut(norm.NormName(arr[2]), true)

			//temp := jieba.Cut(norm.NormName(arr[1])+norm.NormAuthor(arr[2]), true)

			nameAuthorUnig := map[string]bool{}
			nameAuthor := ""
			for _, t := range temp1 {
				// 去除停用词 和 单个字符
				if _, ok := stopWord[t]; !ok && (utf8.RuneCountInString(t) > 1) {
					nameAuthorUnig[t] = false
					nameAuthor += t + "|"
				}
			}

			for _, t := range temp2 {
				// 去除停用词 和 单个字符
				if _, ok := stopWord[t]; !ok && (utf8.RuneCountInString(t) > 1) {
					nameAuthorUnig[t] = false
					nameAuthor += t + "|"
				}
			}

			nameAuthor = strings.Trim(nameAuthor, "|")
			nameAuthor += "{]" + arr[1] + "{]" + arr[2]
			(*gids)[arr[0]] = nameAuthor

			for word, _ := range nameAuthorUnig {
				if value, ok := (*wordDict)[word]; ok {
					value[arr[0]] = false
					(*wordDict)[word] = value
				} else {
					tmp := map[string]bool{arr[0]: false}
					(*wordDict)[word] = tmp
				}
			}
		}
	} else {
		log.Println("打开文件错误 %s", err)
	}

	return ret
}
