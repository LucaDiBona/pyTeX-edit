from latexFile import Command, LatexFile, Package
running = True
x = LatexFile("test.tex")
y= Package("foo",["bar","marmite=food"])
z= Package("foo",["cheese"])
cmd = Command("testcommand",0,["arg","uments"],["Opt"])
while running:
    command = input("> ")  # TODO Replace with reasonable TUI (curses maybe)

    print(cmd.pos("e"))
    print(cmd.pos("s"))
    print(cmd.pos("sa"))
    print(cmd.pos("so"))
    print(cmd.pos("ea"))
    print(cmd.pos("eo"))
    print(cmd.pos("sa",1))

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
    elif command == "e":
        y.editOption("marmite","drink")
        print(y.options())
