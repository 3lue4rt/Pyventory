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
        self.terminal.addLine(f"Se ha agregado exitosamente el computador {data.exportList()[0]} a {filename}")

    #returns a list of data given a substring of a trait
    def csvSearch(self, trait: str, index: int) -> list[csvData]:
        return csvSearchBy(trait, index)
    
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
        self.insertButton = createButton(self.parent, "Ingresar Computador", lambda : InsertMenu(self.parentApp))
        self.editButton = createButton(self.parent, "Editar Computador", lambda : EditMenu(self.parentApp))

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
        self.entry = Entry(self.parent, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<Return>", self.make)

        self.cancelButton = createButton(self.parent, "Cancelar y Volver", self.cancelCommand)

    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.entry.unbind("<Return>")
        MainMenu(self.parentApp)

    def make(self, dummyParameterForEntryBind=None):
        #Automatically enters actual date if nothing is entered
        if self.index==1 and self.entry.get()=="":
            self.result.append(str(datetime.datetime.now()))
            self.index += 1
            self.label.config(text=self.header[self.index])

        #Handles no entry by the user
        elif self.entry.get()=="":
            self.parentApp.terminal.addLine("No se puede ingresar nada, ingrese algo")

        #General case
        else:
            self.result.append(self.entry.get())
            self.entry.delete(0,END)
            self.index += 1
            if self.index<=8:
                self.label.config(text=self.header[self.index])
            #sets up the question for automatic date
            if self.index==1:
                self.label.config(text=self.header[self.index] + " (Si quiere ingresar la fecha actual no ingrese nada)")

        self.parentApp.terminal.addLine(f"se ha ingresado hasta ahora: {self.result}")

        #Ends insert
        if self.index>8:
            self.parentApp.csvImport(listToData(self.result))
            self.cancelCommand()

# Edit menu, requiers parent frame to sit on, starts the search for a PC
class EditMenu:
    def __init__(self, parentApp: App):
        #parent Stuff
        self.parentApp = parentApp
        self.parent = parentApp.mainFrame
        clear(self.parent)
        
        #Actual selected data
        self.selected: csvData | None = None

        #Menu Title
        self.label = Label(self.parent, font=("Arial", 16), text= "Ingrese el número de PC")

        #Entry with dropdown list*
        self.entry = Entry(self.parent, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.update_list)  # Detect typing

        self.entry.bind("<Return>", self.getEntry)

        self.listbox = Listbox(self.parent, width=30, height=5,font=("Arial", 16))
        self.listbox.bind("<ButtonRelease-1>", self.select_item)
        self.entry.bind("<FocusOut>", lambda dummyvar: self.listbox.place_forget()) #click out clears box

        self.cancelButton = createButton(self.parent, "Cancelar y Volver", lambda: MainMenu(self.parentApp))

    # gets the entry and sets the selected value to a csv
    # if no match, selected is None.
    def getEntry(self, dummyParameterForEntryBind=None):
        resultList = self.parentApp.csvSearch(self.entry.get(), 0)
        self.selected = resultList[0] if not resultList == [] else None # First result if not empty
        if not self.selected is None:
            self.parentApp.terminal.addLine(f"Se ha seleccionado el PC-{self.selected.numero_pc}")
        else:
            self.parentApp.terminal.addLine("No se ha encontrado ningun PC con ese número")

    #Updates the listbox
    #IT ONLY SEARCHES BY PC NUMBER (INDEX 0), REST, TO IMPLEMENT
    def update_list(self, dummyParameterForEntryBind=None):
        self.listbox.delete(0, END)  # Clear previous items

        if self.entry.get()!="":  # Show matching items
            filtered = self.parentApp.csvSearch(self.entry.get(), 0)
            if not filtered == []:
                for item in filtered:
                    self.listbox.insert(END, item.numero_pc)

                # Position the Listbox below the Entry widget
                self.listbox.pack(after=self.entry)
            else:
                self.listbox.place_forget()  # Hide if no match

    def select_item(self, dummyParameterForEntryBind=None):
        selected = self.listbox.get(ACTIVE)  # Get the selected item
        self.entry.delete(0, END)
        self.entry.insert(0, selected)
        self.listbox.place_forget()  # Hide the dropdown after selection
 
