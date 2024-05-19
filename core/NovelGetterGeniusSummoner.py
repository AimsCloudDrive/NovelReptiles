import abc
import time
import bs4
import requests
from bs4 import ResultSet, Tag

from com.main.Code import Code
from com.main.Novel import Novel

index = 0


def getChapter() -> int:
    global index
    index += 1
    return index


def generateTitle(h2s: ResultSet[Tag]) -> str:
    h2sText = []
    for h2 in h2s:
        h2sText.append(h2.text)
    return " ".join(h2sText)


def generateContext(divs: ResultSet[Tag]) -> str:
    contexts = []
    context = "\n\n    "
    for div in divs:
        contexts.append(div.text)
    context += "\n\n    ".join(contexts)
    return context


class NovelGetterGeniusSummoner(Novel):

    def getChapterInfoList(self) -> None:
        self.getResponse(self.novelUrl, "章节列表", Code.UTF8)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None
        divList = soup.select("div.list")[0]
        ul = divList.select("ul")[0]
        lis = ul.select("li")
        for li in lis:
            a = li.findNext()
            u = a.get("href").split("/")[-1]
            t = a.get("title")
            self.chapterInfoList.append((self.novelUrl + u, f"第{getChapter()}章 " + t))
        return None

    def getSingleChapterContent(self, info: [tuple[str, str]]) -> None:
        u, t = info

        self.getResponse(u, t, Code.UTF8)
        self.singleChapterContent = t + "\n"
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        contentDiv = soup.select("div.text")[0]
        contents = contentDiv.text.replace("\n", "").split("\xa0\xa0\xa0\xa0")
        if contents[0] != "":
            contents.insert(0, "")
        self.singleChapterContent += "\n\n    ".join(contents) + "\n\n\n\n"
        self.file.write(self.singleChapterContent)
        self.singleChapterContent = ""
        self.response = None
        time.sleep(1)
        return None

    def run(self):
        self.getChapterInfoList()  # 货物章节列表
        for chapterInfo in self.chapterInfoList[:]:
            self.getSingleChapterContent(chapterInfo)  # 获取每章内容
            # break
        self.file.close()  # 关闭文件
        self.chapterInfoList = []
