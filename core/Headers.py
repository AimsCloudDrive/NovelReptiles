import random


class Headers:
    nowIndex = None

    def __init__(self):
        self.__Headers = [
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/114.0.0.0 Safari/537.36",
                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/112.0.0.0 Safari/537.36 ",
                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 ",
                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54 ",
                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64 ",
                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                          "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7 ",
                "Cookie": "cf_clearance=XRymPhXzh8GxDLBK7t_N5Lsoytb2DXDset6L2B8g0.s-1692447492-0-1-8c3f1330.3d5bc0b4"
                          ".75e40075-0.2.1692447492 "
            },
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                          "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6",
                "Cookie": "cf_clearance=XRymPhXzh8GxDLBK7t_N5Lsoytb2DXDset6L2B8g0.s-1692447492-0-1-8c3f1330.3d5bc0b4"
                          ".75e40075-0.2.1692447492",
                "Referer": "https://www.beqege.com/",
                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',

                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Site": "cross-site",

                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36 "
            }
        ]

    def getRandomHeaders(self, method="random"):
        index = None
        if method == "random":
            index = random.randint(0, len(self.__Headers) - 1)
        else:
            if self.nowIndex is None:
                self.nowIndex = random.randint(0, len(self.__Headers) - 1)
            index = self.nowIndex
        return self.__Headers[index]
