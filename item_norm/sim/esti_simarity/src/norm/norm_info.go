package norm

import (
	"regexp"
)

/* 特殊符号 */
var reg = regexp.MustCompile(`(\pP|作者|书名)`)

func NormName(name string) string {

	/* 删除特殊符号 */
	str1 := reg.ReplaceAllString(name, "")

	return str1
}

func NormAuthor(author string) string {

	/* 删除特殊符号 */
	str1 := reg.ReplaceAllString(author, "")

	return str1
}
