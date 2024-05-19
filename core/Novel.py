import requests
from requests import Response

from Headers import Headers
from Logger import Logger
from Code import Code
import abc


# 小说下载器
class Novel(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        """
        :brief
        :param novelUrl: 小说路径
        :param novelSaveFIleName: 小说保存文件名 .txt
        :param logFileName: 日志文件名称 .log
        """
        novelUrl = kwargs.get("novelUrl")
        if novelUrl:
            self.novelUrl = novelUrl
        else:
            raise Exception("novelUrl不可为空!!!")

        self.file = None
        saveFIleName = kwargs.get("novelSaveFIleName")
        filePredix = "../txts/"
        __fileName = ""
        if saveFIleName is None:
            __fileName = "newFile.txt"
        else:
            __fileName = "../txts/"
        self.file = open(filePredix + __fileName, "w+", encoding=Code.UTF8)
        self.logger = None
        logFileName = kwargs.get("logFileName")
        if logFileName is None:
            self.logger = Logger("newFile.log").getLogger()
        else:
            self.logger = Logger(logFileName).getLogger()

        # content info
        # ChapterList
        self.chapterInfoList = []
        self.singleChapterContent = ""
        self.response = None

    @abc.abstractmethod
    def getChapterInfoList(self):
        pass

    @abc.abstractmethod
    def getSingleChapterContent(self, info):
        pass

    def getResponse(self, uurl, text, codeFormat):
        count = 1
        while self.response is None and count < 4:
            try:
                self.logger.info(text + f"————>>> 第{count}次请求")
                self.response = requests.get(
                    url=uurl, headers=Headers().getRandomHeaders()
                )
                self.logger.info(text + f"————>>> 第{count}次请求成功")
            except Exception as e:
                self.logger.error(text + f"————>>> 第{count}次请求失败")
                self.logger.error(e)
            finally:
                count += 1
        if count == 4 and self.response is None:
            raise Exception("3次请求都失败")
        self.response.encoding = codeFormat

    def close(self):
        self.file.close()

    def run(self, index=0) -> None:
        self.getChapterInfoList()
        for chapterInfo in self.chapterInfoList[index:]:
            self.getSingleChapterContent(chapterInfo)
        self.close()
        self.chapterInfoList = None
        return None
