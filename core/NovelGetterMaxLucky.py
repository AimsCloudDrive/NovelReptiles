import time

import bs4

from com.main.Code import Code
from com.main.Novel import Novel


class NovelGetterMaxLucky(Novel):

    def __getContent(self, info) -> []:
        link, t = info
        count = 0
        while count < 3:
            self.getResponse(link, t, Code.GBK)
            if self.response is None:
                continue
            soup = bs4.BeautifulSoup(self.response.text, "html.parser")
            tp = soup.select("div#content")
            if len(tp) != 0:
                content = tp[0]
                contents = [p.getText() for p in content.select("p")]
                if len(contents) != 0:
                    return contents
            self.response = None
            count += 1

    def getSingleChapterContent(self, info):
        link, t = info
        self.file.write(
            t + "\n"
        )
        contents = self.__getContent(info)
        self.response = None
        self.file.write("".join([c.replace("\u3000\u3000", "\n\n\t\t") for c in contents]) + "\n\n\n\n")
        pass

    def getChapterInfoList(self):
        self.getResponse(self.novelUrl, "章节列表", Code.GBK)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None

        divs = soup.select("div#list")[0]
        dl = divs.select("dl")[0]
        dds = dl.select("dd")
        for dd in dds:
            a = dd.select("a")[0]
            link = self.novelUrl + a.get("href").split("/")[-1]
            t = a.getText()
            self.chapterInfoList.append((link, t))
        return None

    def run(self, index=0) -> None:
        self.getChapterInfoList()
        for chapterInfo in self.chapterInfoList[index:]:
            time.sleep(1)
            self.getSingleChapterContent(chapterInfo)
            # break
        self.close()
        self.chapterInfoList = None
        return None
