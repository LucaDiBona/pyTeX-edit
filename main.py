from latexFile import LatexFile
running=True
while running:
    command=input("> ") #TODO Replace with reasonable TUI (curses maybe)
    x=LatexFile("test.tex")

    if command=="kill":
        running = False
