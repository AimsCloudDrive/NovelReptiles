import re

import bs4

from com.main.Code import Code
from com.main.Novel import Novel


class NovelGetterMainOfXO(Novel):
    tId = 0
    contents = []
    nots = ["(珠胎暗结)", "请收藏本站：https://www.bqg70.com。笔趣阁手机版：https://m.bqg70.com ", "添加“buding765“微x号，看更多好看的小说！内容end"]

    def __getTitle(self):
        self.tId += 1
        return f"第{self.tId}章"

    def __getContent(self, link, t, Pid):
        self.getResponse(link, t + f"第_{Pid}页", Code.UTF8)
        soup = bs4.BeautifulSoup(self.response.text, Code.HTML_PARSER)
        self.response = None
        nextPageUrl = None
        sectionOpt = soup.select("div.section-opt")[0]
        nextUrlA = sectionOpt.select("a#next_url")[0]
        if nextUrlA.getText().replace(" ", "") == "下一页":
            nextPageUrl = "http://biqugetxt.cc" + nextUrlA.get("href")
        contentDiv = soup.select("div#content")[0]
        contentPs = contentDiv.select("p")

        for contentP in (contentPs[1:] if nextPageUrl is not None else contentPs):
            p = contentP.getText().replace("\xa0\xa0\xa0\xa0 ", "").replace("\r", "")
            if (re.match(r"\d+、", p) is not None) or (p in self.nots):
                continue
            self.contents.append("    " + p + "\n\n")
        if nextPageUrl is not None:
            self.__getContent(nextPageUrl, t, Pid + 1)

        return None

    def getSingleChapterContent(self, info):
        link, t = info
        Pid = 1
        self.file.write(t + "\n\n\n")
        self.__getContent(link, t, Pid)
        self.singleChapterContent = self.singleChapterContent.join(self.contents) + "\n\n\n"
        self.contents.clear()
        self.file.write(self.singleChapterContent)
        self.singleChapterContent = ""
        return None

    def getChapterInfoList(self):
        self.getResponse(self.novelUrl, "章节列表", Code.UTF8)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None
        divs = soup.select("div.section-box")[1]
        ul = divs.select("ul")[0]
        lis = ul.select("li")
        for li in lis:
            a = li.select("a")[0]
            link = "http://biqugetxt.cc" + a.get("href")
            t = self.__getTitle()
            self.chapterInfoList.append((link, t))

        return None

    # def run(self, index=0) -> None:
    #     self.getChapterInfoList()
    #     for info in self.chapterInfoList:
    #         self.getSingleChapterContent(info)
    #         break
