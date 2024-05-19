import logging
from logging import handlers
import os.path
from colorama import Fore, Style
import sys


class Logger:
    def __init__(self, logFileName):
        self.logger = None
        self.__logFileName = logFileName

    def getLogger(self, level=logging.DEBUG, when='D', back_count=0):
        """
        :brief  日志记录
        :param level: 日志等级
        :param when: 间隔时间:
            S:秒
            M:分
            H:小时
            D:天
            W:每星期（interval==0时代表星期一）
            midnight: 每天凌晨
        :param back_count: 备份文件的个数，若超过该值，就会自动删除
        :return: logger
        """
        # 创建一个日志器。提供了应用程序接口
        self.logger = logging.getLogger(self.__logFileName)

        dirName, fileName = os.path.split(os.path.abspath(sys.argv[0]))
        LOG_ROOT = dirName

        # 设置日志输出的最低等级,低于当前等级则会被忽略
        self.logger.setLevel(level)

        # 创建日志输出路径
        logPath = os.path.join(LOG_ROOT, "logs")
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        logFilePath = os.path.join(logPath, self.__logFileName)

        # 创建格式器
        formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        # 创建处理器：ch为控制台处理器，fh为文件处理器
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # 输出到文件
        fh = logging.handlers.TimedRotatingFileHandler(
            filename=logFilePath,
            when=when,
            backupCount=back_count,
            encoding='utf-8')
        fh.setLevel(level)

        # 设置日志输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 将处理器，添加至日志器中
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        return self

    def debug(self, msg):
        """
        定义输出的颜色debug--white，info--green，warning/error/critical--red
        :param msg: 输出的log文字
        :return:
        """
        self.logger.debug(Fore.WHITE + "DEBUG - " + str(msg) + Style.RESET_ALL)

    def info(self, msg):
        self.logger.info(Fore.GREEN + "INFO - " + str(msg) + Style.RESET_ALL)

    def warning(self, msg):
        self.logger.warning(Fore.RED + "WARNING - " + str(msg) + Style.RESET_ALL)

    def error(self, msg):
        self.logger.error(Fore.RED + "ERROR - " + str(msg) + Style.RESET_ALL)

    def critical(self, msg):
        self.logger.critical(Fore.RED + "CRITICAL - " + str(msg) + Style.RESET_ALL)

