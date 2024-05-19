import re


class Title:
    def __init__(self,title: str):
        self._title = title


    def update(self):
        pattern = r"\d+"
        res = re.search(pattern, self._title)
        if self.isContainNum():
            tmp = self._title
            self._title = "第" + self._title[res.span()[0]: res.span()[1]] + "章 "
            if self._isContain("章"):
                self._title += tmp[res.span()[1] + 2:].strip()
            else:
                self._title += tmp[res.span()[1]:].strip()
        else:
            raise Exception("找不到章节数")

    def isContainNum(self) -> bool:
        pattern = r"\d+"
        res = re.search(pattern, self._title)
        if res is None:
            return False
        else:
            return True

    def _isContain(self, patter):
        try:
            self._title.index(patter)
            return True
        except ValueError:
            return False

    def getTitle(self):
        return self._title


if __name__ == '__main__':
    t = Title("第1448章 新的秘闻与各奔前路")
    t.update()
    print(t.getTitle())

