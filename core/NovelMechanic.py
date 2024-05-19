import time

import bs4
import requests

from Logger import Logger
from Headers import Headers
from Title import Title


class NovelMechanic:

    def __init__(self, **kwargs):
        if kwargs.get("firstPageUrl") is None or kwargs.get("firstPageUrl") == "":
            raise Exception("firstPageUrl不可为空!!!")
        else:
            self.__firstPageUrl = kwargs.get("firstPageUrl")
        if kwargs.get("filePath") is None:
            self.__file = open("./newFile.txt", "w+", encoding="utf-8")
        else:
            self.__file = open(kwargs.get("filePath"), "w+", encoding="utf-8")
        self.__nowChapterPage = int(
            self.__firstPageUrl[self.__firstPageUrl.index("_") + 1:]
            [:self.__firstPageUrl[self.__firstPageUrl.index("_"):].index(".") - 1]
        ) - 1
        self.__logger = None
        self.__nowContentPage = 0

    def __chapterPage(self):
        self.__nowChapterPage += 1
        return self.__nowChapterPage

    def __contentPage(self):
        self.__nowContentPage += 1
        return self.__nowContentPage

    def __getNextPageIndex(self, nowPageIndex):
        response = None
        while response is None:
            try:
                response = requests.get(url=nowPageIndex, headers=Headers().getRandomHeaders())
            except Exception as e:
                self.__logger.warning(f"==================异常的response==================\n")
                self.__logger.warning(response)
                self.__logger.error(e)
        response.encoding = "utf-8"
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        for tag in soup.select("span"):
            if tag['class'][0] == "right":
                nextPageIndex = tag.find("a").get("href")
                if nextPageIndex is None or nextPageIndex == "" or nextPageIndex == "#" or nextPageIndex == "/":
                    return None
                else:
                    return nextPageIndex

    def __getNovelChaptersCore(self, nowPageIndex):
        self.__novelChapters = []
        nextPageIndex = self.__getNextPageIndex(nowPageIndex)
        response = None
        while response is None:
            try:
                response = requests.get(url=nowPageIndex, headers=Headers().getRandomHeaders())
            except Exception as e:
                self.__logger.warning(f"==================异常的response==================\n")
                self.__logger.warning(response)
                self.__logger.error(e)
        response.encoding = "utf-8"
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        self.__logger.info(f"===================第{self.__chapterPage()}页===================\n\n")
        lis = soup.select(".section-list")[-1].select("li")
        for li in lis:
            a = li.find("a")
            self.__novelChapters.append((a.get("href"), a.get_text()))

        self.__getNovelContent()

        if nextPageIndex is not None:
            self.__getNovelChaptersCore(nextPageIndex)
        else:
            return

    def __getNovelChapters(self):
        self.__logger.info("===================获取每页章节信息===================")
        self.__getNovelChaptersCore(self.__firstPageUrl)

    def __getContentCore(self, nowContentPageUrl, text):
        content = text
        response = None
        while response is None:
            try:
                response = requests.get(url=nowContentPageUrl, headers=Headers().getRandomHeaders())
            except Exception as e:
                self.__logger.warning(f"==================异常的response==================\n")
                self.__logger.warning(response)
                self.__logger.error(e)
        self.__logger.info(f"第{self.__contentPage()}页\ting")
        response.encoding = "utf-8"
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        ps = soup.select("div #content")[0].select("p")
        for p in ps[:len(ps) - 1]:
            content += "\t" + p.get_text() + "\n\n"
        aNextUrl = soup.select("a#next_url")
        if aNextUrl[0].get_text().strip() == "下一页":
            content = self.__getContentCore(aNextUrl[0].get("href"), content)

        return content

    def __getNovelContent(self):
        for indexUrl, title in self.__novelChapters:
            title = Title(title)
            if title.isContainNum():
                title.update()
            else:
                continue
            self.__logger.info("正在下载：\t" + title.getTitle())
            self.__file.write(title.getTitle() + "\n\n\n")
            self.__nowContentPage = 0
            self.__file.write(self.__getContentCore(indexUrl, ""))
            self.__file.write("\n\n\n\n")
            self.__logger.info("===>\t下载完成\n\n")
            time.sleep(2)

    def __getLogger(self, logFileName):
        self.__logger = Logger(logFileName).getLogger()

    def run(self):
        self.__getLogger("Mechanic.log")
        self.__getNovelChapters()
        self.__file.close()
