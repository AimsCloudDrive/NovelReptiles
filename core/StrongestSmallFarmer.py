import bs4

from com.main.Code import Code
from com.main.Novel import Novel

url = "https://www.biquge365.net/"


class StrongestSmallFarmer(Novel):
    def getChapterInfoList(self):
        self.getResponse(self.novelUrl, "章节列表", Code.UTF8)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None
        border = soup.select("div.border")[0]
        info = border.select("ul.info")[0]
        lis = info.select("li")
        for li in lis:
            a = li.select("a")[0]
            href = url + a.get("href")
            t = a.get("title")
            self.chapterInfoList.append((href, t))
        pass

    def getSingleChapterContent(self, info):
        href, t = info
        self.file.write(t + "\n\n\n    ")
        self.getResponse(href, t, Code.UTF8)
        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.response = None
        content = soup.select("div#txt")[0].text
        contents = content.split("    ")[1:]
        self.singleChapterContent = "\n\n    ".join(contents)
        self.file.write(self.singleChapterContent + "\n\n\n\n")
        self.singleChapterContent = ""
        pass

