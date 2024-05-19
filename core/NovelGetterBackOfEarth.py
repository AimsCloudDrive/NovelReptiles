import time

import bs4

from Novel import Novel
from Code import Code

g = "笔趣阁 www.52bqg.org，最快更新回到地球当神棍 ！"


class NovelGetterBackOfEarth(Novel):

    def getChapterInfoList(self):
        self.getResponse(self.novelUrl, "章节列表", Code.GBK)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None
        divList = soup.select("div#list")[0]
        dl = divList.select("dl")[0]
        dds = dl.select("dd")
        for dd in dds[12:]:
            a = dd.find("a")
            if a is None:
                continue
            u = a.get("href").split("/")[-1]
            t = a.text
            self.chapterInfoList.append((self.novelUrl + u, t))
        return None

    def getSingleChapterContent(self, info):
        u, t = info

        self.getResponse(u, t, Code.GBK)
        self.singleChapterContent = t + "\n"
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        contentDiv = soup.select("div#content")[0]
        contents = [content for content in contentDiv.text.split("\xa0\xa0\xa0\xa0") if content != g]
        contents.insert(0, "")
        self.singleChapterContent += "\n\n    ".join(contents) + "\n\n\n\n"
        self.file.write(self.singleChapterContent)
        self.singleChapterContent = ""
        self.response = None
        time.sleep(1)
        return None
