#TODO Deal with \DocumentClass
#TODO Deal with author, title, date etc
class LatexFile():

    def __init__(self, fileName: str) -> None:
        self.__STRUCTURE_LAYER = {"title": None, "subSections": []}
        self.SECTION_HIERARCHY = ["chapter",
                                  "section", "subsection", "subsubsection"]
        self.fileName = fileName
        self.__f = open(fileName, "a+")
        self.__f.seek(0)
        self.__fContentsI = self.__f.read()
        self.fileContents = self.__fContentsI.copy()
        print(self.inBrackets(("{","}"),"chapter",0))
        self.updatePackages()



    def getStructure(self) -> list:
        """
        Getter for the structure of the LaTeX file

        Returns:
            list: [dict:{
                layer (int): the layer at which the chapter/section... is
                title (str): the text of the chapter/section... title
                pos (int): the position of the '{' of the chapter/section
            }...]
        """
        self.structure = []
        for i, val in enumerate(self.SECTION_HIERARCHY):
            j = 0
            # iterates through current string, finding all subsections
            while j <= len(self.fileContents):
                self.currentDict = self.inBrackets(("{","}"),val, j)
                if self.currentDict["endPos"] >= 0:
                    self.structure.append(
                        {"layer": i, "title": self.currentDict["contents"], "pos": self.currentDict["pos"]})
                    j = self.currentDict["endPos"]
                else:
                    j += 1
        return(self.structure)

    def updatePackages(self) -> None:
        """
        updates self.packages
        """
        self.packages=[]
        i=0
        while i <= len(self.fContents):
            self.packageImport=self.inBrackets(("{","}","usepackage",i))
            if self.packageImport["endPos"] >=0:
                if self.inBrackets(("[","]"),"usepackage",i)["endPos"] > self.packageImport["pos"]:
                    pass


    def getPackages(self) -> list:
        pass #TODO output packages

    def groupPackages(self) -> None:
        pass #TODO group all packages without options into one \usepackage

    def splitPackages(self) -> None:
        pass #TODO split packages into separate \usepackages

    def addPackage(self, name: str, options = None) -> None:
        pass #TODO add package

    def inBrackets(self, brackets: tuple, keyword: str, startPos: int = 0) -> dict:
        """
        Finds words inside brackets for next appropriate LaTeX command

        Args:
            brackets Tuple(str,str): opening and closing brackets
            keyword (str): keyword to look for
            startPos (int): the initial position to search from, defaults to 0

        Returns:
            dict: {
                pos (int): the position of the opening bracket
                endPos (int): the position of the closing bracket
                contents (str): the string between the opening and closing brackets
                }
        """
        self.__pos = self.__fContentsI.find(
            ("\\"+keyword + brackets[0]), startPos, len(self.__fContentsI))

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
                if self.__fContentsI[i] == brackets[1] and self.__unpairedBracketCount == 0:
                    self.__endPos = self.__pos + len(self.__bracketContents)
                    self.__endPos += 1
                    return({
                        "pos": self.__pos,
                        "endPos": self.__endPos,
                        "contents": self.__bracketContents
                    })
                else:
                    if self.__fContentsI[i] == brackets[1]:
                        self.__unpairedBracketCount -= 1
                    elif self.__fContentsI[i] == brackets[0]:
                        self.__unpairedBracketCount += 1

                    self.__bracketContents += self.__fContentsI[i]

            # Error raised if unpaired '{' or '}' present after startPos
            raise TypeError(
                "Incorrectly formatted .tex document or misaligned startPos")

class Package():

    def __init__(self, name: str, options: list =[]) -> None:
        self.name=name
        self.options={}
        for i in options:
            splitOptions=i.split("=",2)
            splitOptions.append(None)
            self.options[splitOptions[0]] = splitOptions[1]
        print(self.options)

    def remove(self) -> None:
        pass #TODO remove package

    def removeOption(self, option: str) -> None:
        pass #TODO remove option

    def editOption(self, option: str, newVal) -> None:
        pass #TODO edit option value

    def ifOption(self, option: str) -> bool:
        pass #TODO See if option is present

    def option(self, option: str) -> str:
        pass #TODO return value of option

    def addOption(self, option: str, val) -> None:
        pass #TODO add option