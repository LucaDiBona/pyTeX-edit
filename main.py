from latexFile import LatexFile, Package
running = True
while running:
    command = input("> ")  # TODO Replace with reasonable TUI (curses maybe)
    x = LatexFile("test.tex")
    y= Package("foo",["bar","marmite=food"])

    if command == "kill" or command == "q":
        running = False

    elif command == "tree":
        print(x.getStructure())
