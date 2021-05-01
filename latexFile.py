# TODO Deal with \DocumentClass
# TODO Deal with environments
# TODO Deal with author, title, date etc
class LatexFile():

    def __init__(self, fileName: str) -> None:
        self.SECTION_HIERARCHY = ["chapter",
                                  "section", "subsection", "subsubsection"]
        # if one of these characters follows a command, it won't be read as part of the command
        self.ALLOWED_COMMAND_ADDITIONS = ["["]
        # treated as cc one/two for some purposes
        self.ADDED_CC_ONE = ["["]
        self.ADDED_CC_TWO = ["]"]
        # the value returned for a bracket if none exists
        self.DEFAULT_BRACKET = {"pos": -1,
                                "endPos": -1,
                                "contents": ""}
        self.CATCODES = [["\\"], ["{"], ["}"], ["$"], ["&"], ["\n"], ["#"],
                         ["^"], ["_"], [], [" ", " "], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], [], [], ["%"], []]  # TODO use full unicode set L & M for letter codes (possibly from https://github.com/garabik/unicode) - maybe make this optional to reduce load times
        self.fileName = fileName
        self.__f = open(fileName, "a+")
        self.__f.seek(0)
        self.__fContentsI = self.__f.read()
        self.fileContents = self.__fContentsI
        self.commands = self.parse()
        self.updatePackages()

    def updateFile(self) -> None:
        pass  # TODO update file based on changes

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
                self.currentDict = self.inBrackets(("{", "}"), val, j)
                if self.currentDict["endPos"] >= 0:
                    self.structure.append(
                        {"layer": i, "title": self.currentDict["contents"], "pos": self.currentDict["pos"]})
                    j = self.currentDict["endPos"]
                else:
                    j += 1
        return(self.structure)

    def updatePackages(self) -> None:
        """
        updates self.packages from self.fileContents
        """
        self.__packages = []
        i = 0
        while i <= len(self.fileContents):
            self.packageImport = self.inBrackets(("{", "}"), "usepackage", i)
            if self.packageImport["endPos"] >= 0:
                # there are options
                self.options = self.inBrackets(("[", "]"), "usepackage", i)
                if 0 < self.options["endPos"] < self.packageImport["pos"]:
                    # TODO make more robust in case of comma in val
                    self.__packages.append(
                        Package(self.packageImport["contents"], (self.options["contents"].split(","))))
                else:
                    self.__packages.append(
                        Package(self.packageImport["contents"]))
                i = self.packageImport["endPos"]

            else:
                break

    def updateCommands(self, command: str) -> None:
        pass  # TODO get this to work
        # TODO do the same with environments

    def getPackages(self) -> list:
        """
        getter for packages

        Returns:
            list: a list of package objects
        """
        return(self.__packages)

    def package(self, name: str) -> object:
        """
        get a single package

        Args:
            name (str): the name of the package

        Returns:
            Package or None: the package, returns None if doesn't exist
        """
        for i in self.__packages:
            if i.name() == name:
                return(i)
        return(None)

    def groupPackages(self) -> None:
        pass  # TODO group all packages without options into one \usepackage

    def splitPackages(self) -> None:
        pass  # TODO split packages into separate \usepackages

    def addPackage(self, package: object) -> None:
        """
        adds a package. if already present it replaces the options

        Args:
            package (Package): the package to be added
        """
        for i, val in enumerate(self.__packages):
            if val.name() == package.name():
                self.__packages[i] = package
                return(None)
        self.__packages.append(package)
        print(self.__packages)

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
        self.__endKywd = self.fileContents.find(
            ("\\"+keyword), startPos, len(self.fileContents))
        self.__checkVal = self.__endKywd + len(keyword) + 1
        if self.fileContents[self.__checkVal] in self.ALLOWED_COMMAND_ADDITIONS:
            self.__pos = self.fileContents.find(
                brackets[0], self.__endKywd, len(self.fileContents))
        else:
            self.__pos = self.__checkVal

        if self.__pos == -1:
            return(self.DEFAULT_BRACKET)
        else:
            self.__bracketContents = ""
            self.__unpairedBracketCount = 0  # ensures only inside {} are detected
            for i in range((self.__pos + 1), len(self.fileContents)):
                if self.fileContents[i] == brackets[1] and self.__unpairedBracketCount == 0:
                    self.__endPos = self.__pos + len(self.__bracketContents)
                    self.__endPos += 1
                    return({
                        "pos": self.__pos,
                        "endPos": self.__endPos,
                        "contents": self.__bracketContents
                    })
                else:
                    if self.fileContents[i] == brackets[1]:
                        self.__unpairedBracketCount -= 1
                    elif self.fileContents[i] == brackets[0]:
                        self.__unpairedBracketCount += 1

                    self.__bracketContents += self.fileContents[i]

            # Error raised if unpaired '{' or '}' present after startPos
            if self.__unpairedBracketCount != 0:
                raise TypeError(
                    "Incorrectly formatted .tex document or misaligned startPos")
            return(self.DEFAULT_BRACKET)

    def parse(self) -> list:

        def genCommand(self, text: str, param=None) -> object:

            def paramParse(self, paramText: str, open: list, close: list) -> list:
                unpairedBrackets = 0
                currentParam = ""
                outputList = []
                for j in paramText:
                    if j in open:
                        unpairedBrackets += 1
                    elif j in close:
                        unpairedBrackets -= 1
                        if unpairedBrackets == 0:
                            outputList.append(currentParam[1:])
                            currentParam = ""
                    if unpairedBrackets > 0:
                        currentParam += j
                return(outputList)

            if param[-1] in self.ADDED_CC_TWO:
                argOrder = "a"
            else:
                argOrder = "o"

            args = paramParse(self, param, self.CATCODES[1], self.CATCODES[2])
            optArgs = paramParse(
                self, param, self.ADDED_CC_ONE, self.ADDED_CC_TWO)

            return(Command(text[1:], 0, args, optArgs, argOrder))

        """
        Modes:
                0: text mode
                1: command mode
                2: parameter mode
                3: command in parameter mode
                4: parameter in parameter mode
                5: command in parameter in parameter mode
                ...
        """
        mode = 0  # text
        commands = []
        currentCommands = [""]
        for i, val in enumerate(self.fileContents):

            # start new command
            if val in self.CATCODES[0]:  # TODO deal with \\ special case
                # TODO deal with single char commands
                # TODO deal with left/right delimiter pairs
                # TODO deal with \a= etc in tabbed environments
                # if in text mode, switch to scan mode
                if mode % 2 == 0:
                    mode += 1  # command
                    currentCommands.append("")
                # if in command mode, process previous command
                else:
                    #! IDK if this will work
                    currentCommands[-2] += currentCommands[-1]
                    commands.append(genCommand(self, currentCommands[-1]))
                    currentCommands.pop()

            # continue to add to current command
            elif val in self.CATCODES[11]:
                pass

            # start looking for parameters
            elif val in self.CATCODES[1]:
                # if in command, go to next parameter
                if mode % 2 == 1:  # TODO deal with \{ command
                    mode += 1  # parameter
                    currentCommands.append("")
                # if in parameter/text mode, increment unpaired brackets

            elif val in self.ADDED_CC_ONE and mode % 2 == 1:
                mode += 1
                currentCommands.append("")

            elif val in self.CATCODES[2]:
                if mode % 2 == 1:
                    pass  # TODO deal with \} and \right}
                elif len(self.fileContents) > (i+1):
                    if not(self.fileContents[i+1] in (self.CATCODES[1] + self.ADDED_CC_ONE)):
                        commands.append(genCommand(
                            self, currentCommands[-2], (currentCommands[-1]+val)))
                        currentCommands[-2] += currentCommands[-1]
                        currentCommands[-3] += currentCommands[-2]
                        currentCommands.pop()
                        currentCommands.pop()
                        mode -= 2

            # invalid char
            elif val in self.CATCODES[15]:
                raise ValueError(".tex file contains and invalid character")
            else:
                if mode % 2 == 1:
                    currentCommands[-2] += currentCommands[-1]
                    commands.append(genCommand(self, currentCommands[-1]))
                    currentCommands.pop()
                    mode -= 1

            currentCommands[mode] += val
        return(commands)


class Command():

    def __init__(self, name: str, pos: int, args: list = [], optArgs: list = [], argOrder: str = "o") -> None:
        self.__name = name
        self.__pos = pos
        self.__args = args
        self.__optArgs = optArgs
        self.__argOrder = argOrder

    def name(self) -> str:
        """
        getter for command/environment name

        Returns:
            str: command/environment name
        """
        return(self.__name)

    def rename(self, name: str) -> None:
        """
        rename a command/environment

        Args:
            name (str): new name
        """
        self.__name = name

    def pos(self, mode: str = "s", index: int = 0) -> int:
        """
        Gets the position of certain character

        Args:
            mode (str, optional): "s": The start of the command (eg '\')
                                  "e": The end of the command (eg '}')
                                  "sa": The start of the argument (eg '{'})
                                  "so": The start of the option (eg '[')
                                  "ea": The end of the argument (eg '}')
                                  "eo": The end of the option (eg ']')
                                   Defaults to "s".
            index (int, optional): The index if the item being considered in the list of arguments. Relative indices supported (with -ve vals). Defaults to 0.

        Returns:
            int: the position of the desired character
        """

        def length(self, list: list):
            length = 0
            for i in list:
                length += 2
                length += len(i)
            return(length)

        # Allows for negative indices
        if index < 0:
            if mode == "so" or "eo":
                index += len(self.__optArgs)
            elif mode == "sa" or "ea":
                index += len(self.__args)
            index += 1

        # calculates position based on arguments by summing up the lengths of the things prior to the position and adding this to the position of the command
        if mode == "s":
            return(self.__pos)
        elif mode == "e":
            addLen = len(self.__name)
            addLen += length(self, self.__args)
            addLen += length(self, self.__optArgs)
            return(self.__pos + addLen)
        elif mode == "so" and self.__argOrder == "o":
            addLen = len(self.__name)
            addLen += 1
            curList = self.__optArgs.copy()
            # removes all items in list from the last, up to and including the one being considered
            while len(curList) >= (index+1):
                curList.pop()
            addLen += length(self, curList)
            return(self.__pos + addLen)
        elif mode == "sa" and self.__argOrder == "a":
            addLen = len(self.__name)
            addLen += 1
            curlist = self.__args.copy()
            # removes all items in list from the last, up to and including the one being considered
            while len(curlist) >= (index+1):
                curlist.pop()
            addLen += length(self, curlist)
            return(self.__pos + addLen)
        elif mode == "eo" and self.__argOrder == "o":
            addLen = len(self.__name)
            curList = self.__optArgs.copy()
            # removes all items in list from the last, up to but not including the one being considered
            while len(curList) > (index+1):
                curList.pop()
            addLen += length(self, curList)
            return(self.__pos + addLen)
        elif mode == "ea" and self.__argOrder == "a":
            addLen = len(self.__name)
            curList = self.__args.copy()
            # removes all items in list from the last, up to but not including the one being considered
            while len(curList) > (index+1):
                curList.pop()
            addLen += length(self, curList)
            return(self.__pos + addLen)
        elif mode == "so" and self.__argOrder == "a":
            addLen = len(self.__name)
            addLen += length(self, self.__args)
            addLen += 1
            curList = self.__optArgs.copy()
            # removes all items in list from the last, up to and including the one being considered
            while len(curList) >= (index+1):
                curList.pop()
            addLen += length(self, curList)
            return(self.__pos + addLen)
        elif mode == "sa" and self.__argOrder == "o":
            addLen = len(self.__name)
            addLen += length(self, self.__optArgs)
            addLen += 1
            curlist = self.__args.copy()
            # removes all items in list from the last, up to and including the one being considered
            while len(curlist) >= (index+1):
                curlist.pop()
            addLen += length(self, curlist)
            return(self.__pos + addLen)
        elif mode == "eo" and self.__argOrder == "a":
            addLen = len(self.__name)
            addLen += length(self, self.__args)
            curList = self.__optArgs.copy()
            # removes all items in list from the last, up to but not including the one being considered
            while len(curList) > (index+1):
                curList.pop()
            addLen += length(self, curList)
            return(self.__pos + addLen)
        elif mode == "ea" and self.__argOrder == "o":
            addLen = len(self.__name)
            addLen += length(self, self.__optArgs)
            curList = self.__args.copy()
            # removes all items in list from the last, up to but not including the one being considered
            while len(curList) > (index+1):
                curList.pop()
            addLen += length(self, curList)
            return(self.__pos + addLen)
        else:
            raise ValueError("Invalid mode or argOrder")

    def getArgs(self) -> list:
        """
        Getter for the list of arguments

        Returns:
            list: list of all arguments
        """
        return(self.__args)

    def getArg(self, index: int) -> str:
        """
        Getter for an individual argument

        Args:
            index (int): index of argument

        Returns:
            str: value of argument
        """
        return(self.__args[index])

    def editArg(self, index: int, newVal: str) -> None:
        """
        Sets the value of a specific argument

        Args:
            index (int): index of argument
            newVal (str): new value of argument
        """
        self.__args[index] = newVal

    def removeArg(self, index: int = -1) -> None:
        """
        Removes an argument

        Args:
            index (int): index of argument. Defaults to last
        """
        self.__args.pop(index)

    def insertArg(self, index: int, val: str) -> None:
        """
        Args:
            index (int, optional): index for argument to be placed at.
            val (str): the value of the argument
        """
        self.__args.insert(index, val)

    def appendArg(self, val: str) -> None:
        """
        Appends and argument

        Args:
            val (str): argument to be appended
        """
        self.__args.append(val)

    def getOpts(self) -> list:
        """
        Getter for the list of options

        Returns:
            list: list of all options
        """
        return(self.__optArgs)

    def getOpt(self, index: int) -> str:
        """
        Getter for an individual option

        Args:
            index (int): index of option

        Returns:
            str: value of option
        """
        return(self.__optArgs[index])

    def editOpt(self, index: int, newVal: str) -> None:
        """
        Sets the value of a specific option

        Args:
            index (int): index of option
            newVal (str): new value of option
        """
        self.__optArgs[index] = newVal

    def removeOpt(self, index: int = -1) -> None:
        """
        Removes an option

        Args:
            index (int): index of option. Defaults to last
        """
        self.__optArgs.pop(index)

    def insertOpt(self, index: int, val: str) -> None:
        """
        Args:
            index (int, optional): index for option to be placed at.
            val (str): the value of the option
        """
        self.__optArgs.insert(index, val)

    def appendOpt(self, val: str) -> None:
        """
        Appends and option

        Args:
            val (str): option to be appended
        """
        self.__optArgs.append(val)

    def getArgOrder(self) -> str:
        """
        Getter for the argument order

        Returns:
            str: "o": options first
                 "a": arguments first
        """
        return(self.__argOrder)

    def setArgOrder(self, val: str) -> None:
        """
        Setter for the argument order

        Args:
            val (str): the argument order:
                      "o": options first
                      "a": arguments first
        """
        self.__argOrder = val


class Package(Command):

    def __init__(self, packageName: str, options: list = []) -> None:
        if len(options) == 0:
            super().__init__("usepackage", -1, [packageName], [])
        else:
            super().__init__("usepackage", -1,
                             [packageName], [",".join(options)])
        self.__options = {}
        self.__packageName = packageName
        for i in options:
            # TODO allow other splitting methods
            splitOptions = i.split("=", 2)
            splitOptions.append(None)
            self.__options[splitOptions[0]] = splitOptions[1]

    def packageName(self) -> str:
        """
        Getter for the name of the package

        Returns:
            str: the name of the package
        """
        return(self.getArg(0))

    def packageRename(self, newVal: str) -> None:
        """
        Renames a package

        Args:
            newVal (str): the new name of the package
        """
        self.editArg(0, newVal)

    def removeOption(self, option: str) -> None:
        """
        Removes an option from a package, if it exists, else returns an error

        Args:
            option (str): the option to be removed

        Raises:
            TypeError: if no such option exists

        """
        if option in self.__options.keys():
            self.__options.pop(option)
        else:
            raise TypeError("No such option")

    def options(self) -> dict:
        """
        Getter for options

        Returns:
            dict: options
        """
        return(self.__options)

    def editOption(self, option: str, newVal) -> None:
        """
        Edits an option from a package, if it exists, else returns an error

        Args:
            option (str): the option to be changed
            newVal ([type]): the new value of the option

        Raises:
            TypeError: if no such option exists
        """
        if option in self.__options.keys():
            self.__options[option] = newVal
        else:
            raise TypeError("No such option")

    def ifOption(self, option: str) -> bool:
        """
        Detects is an option is present

        Args:
            option (str): the option being tested

        Returns:
            bool: True is option present, false if not
        """
        return(option in self.__options.keys())

    def option(self, option: str) -> str:
        """
        Getter for individual options

        Args:
            option (str): the option to be retrieved

        Raises:
            TypeError: if no such object exists

        Returns:
            str: the value of the option
        """
        if option in self.__options.keys():
            return(self.__options[option])
        else:
            raise TypeError("No such option")

    def addOption(self, option: str, val) -> None:
        """
        Adds new option and value

        Args:
            option (str): name of option
            val (str or None): the value
        """
        self.__options[option] = val
