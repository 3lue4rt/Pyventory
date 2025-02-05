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
import datetime

#creates a Button given a frame, name and function
def createButton(frame: Frame, name: str, func: types.FunctionType) -> Button:
    button = Button(frame, text=name, font=("Arial", 14), command= func)
    button.pack(fill="both")
    return button

#Clears a Frame of all their widgets
def clear(frame: Frame):
    for widget in frame.winfo_children():
        widget.pack_forget()

#turns the list of traits to data
def listToData(traitList: list[str]) -> csvData:
    return csvData(traitList[0], traitList[1], traitList[2], traitList[3],
                   traitList[4], traitList[5], traitList[6], traitList[7],
                   traitList[8])

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
        self.mainMenu = MainMenu(self)

        #Creates the Frame for the terminal
        self.terminalFrame = Frame(self.root, padx=10, pady=10)
        self.terminalFrame.pack(fill="both")

        #Creates the Terminal in the respective Frame
        self.terminal = Terminal(self)

        #Starts the csv Importer and checks if the file exists, if not creates one
        fileExists = csvINIT()
        if not fileExists:
            self.terminal.addLine("No se encontró ningun archivo data, se ha creado uno nuevo")
        isValid = csvValidate()
        if not isValid:
            self.terminal.addLine("El archivo no tiene el formato correcto... guarde los datos a mano y borre el archivo para restaurar")

    #imports data to the csv
    def csvImport(self, data: csvData):
        csvInsert(data)
        self.terminal.addLine(f"Se ha agregado exitosamente el computador ${data.exportList()[0]} a ${filename}")

    #Method for starting the app
    def run(self) -> None:
        self.root.mainloop()

#Terminal class, requires a parent Frame to sit on, displays text
class Terminal:
    def __init__(self, parentApp: App):
        #Parent Frame
        self.parent = parentApp.terminalFrame

        #Initial text
        self.text = "=> Pyventory, BlueArt 2025"

        #Creates the Label for displaying text
        self.mainLabel = Label(self.parent, text=self.text, font=("Arial", 16), justify="left",anchor="sw")
        self.mainLabel.pack(side="bottom", anchor="sw", fill="x", padx=10, pady=10)
        self.mainLabel.bind('<Configure>', lambda e: self.mainLabel.config(wraplength=self.mainLabel.winfo_width()))

    #Updates the text in the Label with the self.text string
    def update(self):
        self.mainLabel.config(text = self.text)

    #Adds a line of text to the bottom of the Label
    # NEEDS TESTING FOR OVERFLOW
    def addLine(self, text: str):
        self.text += "\n=> "+text
        self.update()

    #Deletes all text in Label
    def deleteText(self):
        self.text = "=> "
        self.update()

#Main Menu class, requires a parent Frame to sit on, buttons for other menus
class MainMenu:
    def __init__(self, parentApp: App):
        self.parentApp = parentApp
        #Parent
        self.parent = parentApp.mainFrame
        clear(self.parent)
        self.insertButton = createButton(self.parent, "Ingresar Computador", lambda : InsertMenu(parentApp))
        self.editButton = createButton(self.parent, "Editar Computador", lambda : None)

# Insert menu class, requires a parent Frame to sit on, adds new computer to csv
class InsertMenu:
    def __init__(self, parentApp: App):
        self.parentApp = parentApp
        #Parent 
        self.parent = parentApp.mainFrame
        clear(self.parent)

        #Data trait list
        self.result = []

        #Header helps order text in label
        self.header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]
        self.header = list("Ingrese: "+text for text in self.header)

        #Index helps other methods access the header and result without calling it directly
        self.index=0

        #Menu structure
        self.label = Label(self.parent, text=self.header[self.index], font=("Arial", 16))
        self.label.pack()
        
        #Entry for traits from the User, make() method dictates the input structure
        self.entry = Entry(self.parent, width=30)
        self.entry.pack()
        self.entry.bind("<Return>", self.make)

        self.cancelButton = createButton(self.parent, "Cancelar y Volver", lambda: MainMenu(self.parentApp))

    def make(self, dummyParameterForEntryBind=None):
        #Automatically enters actual date
        if self.index==1:
            self.result.append(datetime.datetime.now())
            self.entry.delete(0,100)
            self.index += 1
            self.make()

        #Handles no entry by the user
        if not self.entry.get():
            self.parentApp.terminal.addLine("No se puede ingresar nada, ingrese algo")
            return
        
        #Ends insert
        elif self.index>8:
            self.parentApp.csvImport(listToData(self.result))
            MainMenu(self.parentApp)

        #General case
        elif self.index != 1:
            self.label.config(text=self.header[self.index])
            self.result.append(self.entry.get())
            self.entry.delete(0,100)
            self.index += 1

        
        
