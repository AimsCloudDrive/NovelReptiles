import time
from Code import Code
from Novel import Novel
import bs4

textR = [
    "最新站名：千夜阁 最新网址：www.qianyege.com",
    "(欢迎各位读者大大加群，普通群：248213917，小说阅读网读者群：191059312（此群只加小说阅读网读者）",
    "‘",
    "’",
]
titleR = ["（求收藏，求推荐）", "粉嫩新书求推荐求收藏）", "（求推荐求收藏）", "。"]


class ExtremeSpiritChaosTechnique(Novel):
    def getChapterInfoList(self):
        self.getResponse(self.novelUrl, "章节列表", Code.GBK)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None
        divList = soup.select("div#list")[0]
        dl = divList.select("dl")[0]
        dds = dl.select("dd")
        for dd in dds:
            a = dd.find("a")
            if a is None:
                continue
            u = a.get("href").split("/")[-1]
            t = a.text
            for r in titleR:
                t = t.replace(r, "")
            self.chapterInfoList.append((self.novelUrl + u, t))
        return None

    def getSingleChapterContent(self, info):
        u, t = info

        self.getResponse(u, t, Code.GBK)
        self.singleChapterContent = t + "\n"
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        contentDiv = soup.select("div#content")[0]
        text = contentDiv.getText()
        for r in textR:
            text = text.replace(r, "")

        self.singleChapterContent += "\n\n" + text + "\n\n\n\n"
        self.file.write(self.singleChapterContent)
        self.singleChapterContent = ""
        self.response = None
        return None
