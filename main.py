import msvcrt

'''
    Main
    Contains runtime loop in main()
    Checks input string and sends execution to appropriate class
    Manages display of text in console
'''
class Main:
    def __init__(self):
        self.running = True

    def ProcessInput(self, strinput):
        if strinput == "exit":
            self.running = False

    def ClearLine(self, bufflength):
        msvcrt.putch(b'\r')
        for x in range(bufflength):
            msvcrt.putch(b' ')
        msvcrt.putch(b'\r')

    def main(self):
        # Contains the main loop of the program.
        keybuffer = ""
        chbuff = ''
        while self.running == True:
            if msvcrt.kbhit():
                chbuff = msvcrt.getch()
                if chbuff == b'\r': # Watch for the enter key
                    self.ProcessInput(keybuffer)
                    self.ClearLine(len(keybuffer))
                    keybuffer = ""
                elif chbuff == b'\x08': # Watch for backspace
                    msvcrt.putch(chbuff)
                    msvcrt.putch(b' ')
                    msvcrt.putch(chbuff)
                    keybuffer = keybuffer[0:len(keybuffer)-2]
                else:
                    keybuffer += chbuff.decode("UTF-8")
                    msvcrt.putch(chbuff)

inst = Main()
inst.main()
