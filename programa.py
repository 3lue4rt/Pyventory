try:
    from tkinter import *
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")

try:
    from tkinter import ttk
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")

import types

from template import *

def rootInit() -> Tk:
    root = Tk()
    root.title("Pyventory")
    root.geometry("1600x900")
    return root

def createFrame(root: Tk) -> Frame:
    frame = Frame(root, padx=10, pady=10)
    frame.pack(fill="both")
    return frame

def createButton(frame: Frame, name: str, func: types.FunctionType) -> Button:
    button = Button(frame, text=name, font=("Arial", 14), command= func)
    button.pack(fill="both")
    return button

class Terminal:
    def __init__(self, parent: Frame, initialText: str):
        self.text=initialText
        self.terminal = Label(parent, text=self.text, font=("Arial", 16), justify="left")
        self.terminal.pack()
        
    def update(self):
        self.terminal.config(text = self.text)

    def addLine(self, text: str):
        self.text += "\n"+text
        self.update()

    def deleteText(self):
        self.text = ""
        self.update()

class Menu:
    def __init__(self, root):
        self.frame1 = createFrame(root)
        self.frame2 = createFrame(root)
        
        self.insertButton = createButton(self.frame1, "Insertar Computador", lambda : None)
        self.editButton = createButton(self.frame1, "Editar Computador", lambda : None)
        self.deleteButton = createButton(self.frame1, "Eliminar Computador", lambda : None)
        self.searchButton = createButton(self.frame1, "Buscar Computador", lambda : None)

        self.terminal = Terminal(self.frame2, "Hello")
        


    ### terminal
    
    
    


