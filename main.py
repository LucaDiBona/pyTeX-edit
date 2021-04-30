from latexFile import LatexFile, Package
running = True
x = LatexFile("test.tex")
y= Package("foo",["bar","marmite=food"])
z= Package("foo",["cheese"])
while running:
    command = input("> ")  # TODO Replace with reasonable TUI (curses maybe)

    if command == "kill" or command == "q":
        running = False

    elif command == "tree":
        print(x.getStructure())
    elif command == "ls pkg":
        for i in x.getPackages():
            print(i.name())
            print(i.options())
    elif command == "geo":
        print(x.package("amsmath"))
    elif command == "add pkg a":
        print(x.addPackage(y))
    elif command == "add pkg b":
        print(x.addPackage(z))
