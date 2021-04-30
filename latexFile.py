class LatexFile():

    def __init__(self, fileName: str) -> None:
        self.__STRUCTURE_LAYER = {"title": None, "subSections": []}
        self.SECTION_HIERARCHY = ["chapter",
                                  "section", "subsection", "subsubsection"]
        self.fileName = fileName
        self.__f = open(fileName, "a+")
        self.__f.seek(0)
        self.__fContentsI = self.__f.read()

        # lists all sections and their positions in the form {<layer>,<title>,<position>}
        self.structure = []
        for i, val in enumerate(self.SECTION_HIERARCHY):
            j = 0
            # iterates through current string, finding all subsections
            while j <= len(self.__fContentsI):
                self.currentDir = self.inBrackets(val, j)
                if self.currentDir["endPos"] >= 0:
                    self.structure.append(
                        {"layer": i, "title": self.currentDir["contents"], "pos": self.currentDir["pos"]})
                    j = self.currentDir["endPos"]
                else:
                    j += 1

    def inBrackets(self, keyword: str, startPos: int = 0) -> dict:
        """Finds words inside {} for next appropriate LaTeX command

        Args:
            keyword (str): keyword to look for
            startPos (int): the initial position to search from, defaults to 0

        Returns:
            dict: {
                pos (int): the position of the '{'
                endPos (int): the position of the '}'
                contents (str): the string between the '{' and the '}'
                }
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
                    self.__endPos += 1
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
            raise TypeError(
                "Incorrectly formatted .tex document or misaligned startPos")
