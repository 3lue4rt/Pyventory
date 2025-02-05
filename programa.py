try:
    from tkinter import *
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")

try:
    from tkinter import ttk
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")

import types
from exportxls import *
from csvHandling import *

'''
interface for tkinter pyventory gui: programa
it uses the csvHandling file for data storing in a csv
and the exportxls file for exporting data in a xlsx file (excel)



    
'''
'''
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

'''
#creates a Button given a frame, name and function
def createButton(frame: Frame, name: str, func: types.FunctionType) -> Button:
    button = Button(frame, text=name, font=("Arial", 14), command= func)
    button.pack(fill="both")
    return button

#Clears a Frame of all their widgets
def clear(frame: Frame):
    for widget in frame.winfo_children():
        widget.pack_forget()

#App class for initializing the application
class App:
    def __init__(self):
        #Creates the root
        self.root = Tk()
        self.root.title("Pyventory")
        self.root.geometry("800x450")

        #Creates the Frame for the menu
        self.mainFrame = Frame(self.root, padx=10, pady=10)
        self.mainFrame.pack(fill="both")

        #Creates the Main Menu in the respective Frame
        self.mainMenu = MainMenu(self.mainFrame)

        #Creates the Frame for the terminal
        self.terminalFrame = Frame(self.root, padx=10, pady=10)
        self.terminalFrame.pack(fill="both")

        #Creates the Terminal in the respective Frame
        self.terminal = Terminal(self.terminalFrame)

    #Method for starting the app
    def run(self) -> None:
        self.root.mainloop()

#Terminal class, requires a parent Frame to sit on, displays text
class Terminal:
    def __init__(self, parentFrame: Frame):
        #Parent Frame
        self.parent = parentFrame

        #Initial text
        self.text = "=> Pyventory, BlueArt 2025"

        #Creates the Label for displaying text
        self.mainLabel = Label(self.parent, text=self.text, font=("Arial", 16), justify="left",anchor="sw")
        self.mainLabel.pack(side="bottom", anchor="sw", fill="x", padx=10, pady=10)

    #Updates the text in the Label with the self.text string
    def update(self):
        self.mainLabel.config(text = self.text)

    #Adds a line of text to the bottom of the Label
    # NEEDS TESTING FOR OVERFLOW
    def addLine(self, text: str):
        self.text += "\n=>"+text
        self.update()

    #Deletes all text in Label
    def deleteText(self):
        self.text = "=> "
        self.update()

#Main Menu class, requires a parent Frame to sit on, buttons for other menus
class MainMenu:
    def __init__(self, parentFrame: Frame):
        #Parent
        self.parent = parentFrame
        clear(self.parent)
        self.insertButton = createButton(self.parent, "Ingresar Computador", lambda : None)
        self.editButton = createButton(self.parent, "Editar Computador", lambda : None)
        self.deleteButton = createButton(self.parent, "Eliminar Computador", lambda : None)
        self.searchButton = createButton(self.parent, "Buscar Computador", lambda : None)