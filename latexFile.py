class LatexFile():

    def __init__(self, fileName: str) -> None:
        self.fileName=fileName
        self.__f=open(fileName, "a+")
        self.__f.seek(0)
        self.__fContentsI=self.__f.read()
        print(self.inBrackets("title"))

        self.structure=[{
            "chapterTitle": "preamble",
            "sections":[]
            }]


    def inBrackets(self, keyword: str, startPos: int = 0) -> dict:
        """Finds words inside {} for next appropriate LaTeX command

        Args:
            keyword (str): keyword to look for
            startPos (int): the initial position to search from, defaults to 0

        Returns:
            dict: the position of the '{' as pos and the contents of the {} as contents
        """
        self.__pos = self.__fContentsI.find(("\\"+keyword + "{"),startPos,len(self.__fContentsI))

        if self.__pos == -1:
            return({
                "pos": -1,
                "contents": ""
            })
        else:
            self.__bracketContents=""
            self.__unpairedBracketCount=0 #ensures onlu inside {} are detected
            for i in range((self.__pos + len(keyword) +2),len(self.__fContentsI)):
                if self.__fContentsI[i] == "}" and self.__unpairedBracketCount ==0:
                    return({
                        "pos": self.__pos,
                        "contents": self.__bracketContents
                    })
                else:
                    if self.__fContentsI[i] == "}":
                        self.__unpairedBracketCount-=1
                    elif self.__fContentsI[i] == "{":
                        self.__unpairedBracketCount +=1

                    self.__bracketContents+=self.__fContentsI[i]

            raise TypeError("Incorrectly formatted .tex document") #Error raised if unpaired '{' or '}' present after startPos
