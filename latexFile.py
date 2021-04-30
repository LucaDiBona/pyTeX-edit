class LatexFile():

    def __init__(self, fileName: str) -> None:
        self.__STRUCTURE_LAYER = {"title": None, "subSections": []}
        self.SECTION_HIERARCHY = ["chapter","section","subsection","subsubsection"]
        self.fileName = fileName
        self.__f = open(fileName, "a+")
        self.__f.seek(0)
        self.__fContentsI = self.__f.read()
        self.structure = []  # structure containing a list of dictionaries, each with the title as a string and a list of dictionaries of the next layer
        self.__currentDir = {
            "pos": 0,
            "contents": ""}
        self.__pos = 0
        while self.__currentDir[pos] != -1:
            pass

    def inBrackets(self, keyword: str, startPos: int = 0) -> dict:
        """Finds words inside {} for next appropriate LaTeX command

        Args:
            keyword (str): keyword to look for
            startPos (int): the initial position to search from, defaults to 0

        Returns:
            dict: the position of the '{' as pos, the position of the '}' as endPos and the contents of the {} as contents
        """
        self.__pos = self.__fContentsI.find(
            ("\\"+keyword + "{"), startPos, len(self.__fContentsI))

        if self.__pos == -1:
            return({
                "pos": -1,
                "endPos": -1,
                "contents": ""
            })
        else:
            self.__bracketContents = ""
            self.__unpairedBracketCount = 0  # ensures only inside {} are detected
            for i in range((self.__pos + len(keyword) + 2), len(self.__fContentsI)):
                if self.__fContentsI[i] == "}" and self.__unpairedBracketCount == 0:
                    self.__endPos = self.__pos + len(self.__bracketContents)
                    self.__endPos +=1
                    return({
                        "pos": self.__pos,
                        "endPos": self.__endPos,
                        "contents": self.__bracketContents
                    })
                else:
                    if self.__fContentsI[i] == "}":
                        self.__unpairedBracketCount -= 1
                    elif self.__fContentsI[i] == "{":
                        self.__unpairedBracketCount += 1

                    self.__bracketContents += self.__fContentsI[i]

            # Error raised if unpaired '{' or '}' present after startPos
            raise TypeError("Incorrectly formatted .tex document or misaligned startPos")

    def getSection(self):
