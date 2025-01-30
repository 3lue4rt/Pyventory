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
from csvHandling import *

#creates the Tkinter root
def rootInit() -> Tk:
    root = Tk()
    root.title("Pyventory")
    root.geometry("800x450")
    return root

#creates a Frame given a Tkinter root
def createFrame(root: Tk) -> Frame:
    frame = Frame(root, padx=10, pady=10)
    frame.pack(fill="both")
    return frame

#creates a Button given a frame, name and function
def createButton(frame: Frame, name: str, func: types.FunctionType) -> Button:
    button = Button(frame, text=name, font=("Arial", 14), command= func)
    button.pack(fill="both")
    return button

#creates an Entry given a frame
def createEntry(frame: Frame) -> Entry:
    entry = Entry(frame, width=30)
    entry.pack()
    return entry

#creates a label given a frame and text
def createLabel(frame: Frame, text: str) -> Label:
    label = Label(frame, text=text, font=("Arial", 16), justify="left")
    label.pack()
    return label

class Terminal:
    def __init__(self, parent: Frame, initialText: str):
        self.text=initialText
        self.terminal = Label(parent, text=self.text, font=("Arial", 16), justify="left",anchor="sw")
        self.terminal.pack(side="bottom", anchor="sw", fill="x", padx=10, pady=10)
        
    def update(self):
        self.terminal.config(text = self.text)

    def addLine(self, text: str):
        self.text += "\n"+text
        self.update()

    def deleteText(self):
        self.text = ""
        self.update()

class App:
    def __init__(self, root: Tk):
        self.root = root
        self.frame1 = createFrame(self.root)
        self.menu(self.frame1)
        self.frame2 = createFrame(self.root)
        self.terminal = Terminal(self.frame2, "Hello")
        
    #header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]

    def clear(self, frame: Frame):
        for widget in frame.winfo_children():
            widget.pack_forget()
            
    def menu(self, frame: Frame):
        self.clear(frame)
        self.insertButton = createButton(frame, "Ingresar Computador", lambda : self.insert1(self.frame1))
        self.editButton = createButton(frame, "Editar Computador", lambda : None)
        self.deleteButton = createButton(frame, "Eliminar Computador", lambda : None)
        self.searchButton = createButton(frame, "Buscar Computador", lambda : None)

    def insert1(self, frame):
        self.clear(frame)
        self.result=[]
        self.label = createLabel(frame, "Ingresar Número de Computador")
        self.entry = createEntry(frame)
        self.cancelButton = createButton(frame, "Cancelar y Volver", lambda: self.menu(frame))
        
        def foo(x):
            if buscarDatoCaracteristicaCSV(self.entry.get(),0):
                self.label.config(text="Ese numero de PC ya fue ingresado")
                self.insert1(frame)
            else:
                self.result.append(self.entry.get())
                self.insert2()
        self.entry.bind("<Return>", foo)
    
    def insert2(self):
        self.label.config(text="Ingrese Placa")
        def next(x):
            self.result.append(self.entry.get())
            self.insert3()
        self.entry.bind("<Return>", next)

    def insert3(self):
        self.label.config(text="Ingrese Partida")
        def next(x):
            self.result.append(self.entry.get())
            self.insert4()
        self.entry.bind("<Return>", next)
    
    def insert4(self):
        self.label.config(text="Ingrese Procesador")
        def next(x):
            self.result.append(self.entry.get())
            self.insert5()
        self.entry.bind("<Return>", next)
    
    def insert5(self):
        self.label.config(text="Ingrese RAM")
        def next(x):
            self.result.append(self.entry.get())
            self.insert6()
        self.entry.bind("<Return>", next)

    def insert6(self):
        self.label.config(text="Ingrese SSD")
        def next(x):
            self.result.append(self.entry.get())
            self.insert7()
        self.entry.bind("<Return>", next)

    def insert7(self):
        self.label.config(text="Ingrese Ubicación")
        def next(x):
            self.result.append(self.entry.get())
            self.insert8()
        self.entry.bind("<Return>", next)

    def insert8(self):
        self.label.config(text="Ingrese Monitor")
        def next(x):
            self.result.append(self.entry.get())
            self.menu(self.frame1)
        self.entry.bind("<Return>", next)