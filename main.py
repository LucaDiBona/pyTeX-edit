import os, sys
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)
from latexFile import Command, LatexFile, Package
running = True
x = LatexFile("test.tex")
y= Package(x,"foo",["bar","marmite=food"]) #TODO fix this
z= Package(x,"foo",["cheese"])
cmd = Command("testcommand",0,["arg","uments"],["Opt"])


print([",".join([])])
print("\#")

while running:
    command = input("> ")  # TODO Replace with reasonable TUI (curses maybe)

    if command == "kill" or command == "q":
        running = False

    elif command == "tree":
        print(x.getStructure())
    elif command == "ls pkg":
        for i in x.getPackages():
            print(i.packageName())
            print(i.options())
    elif command == "geo":
        print(x.package("amsmath"))
    elif command == "add pkg a":
        print(x.addPackage(y))
    elif command == "add pkg b":
        print(x.addPackage(z))
    elif command == "e":
        y.editOption("marmite","drink")
        print(y.options())
