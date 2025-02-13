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
    button = Button(frame, text=name, font=("Arial", 14), command= func )
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
    
    def csvDelete(self, data: csvData) -> int:
        return csvRemove(data)
    
    #Method for starting the app
    def run(self) -> None:
        self.root.mainloop()

#Terminal class, requires a parent App to sit on, displays text
class Terminal:
    def __init__(self, parentApp: App):
        #Parent Frame
        self.parent = parentApp.terminalFrame

        #canvas parent
        #self.canvas=Canvas(self.parent)

        #frame in the canvas
        #self.frame = Frame(self.canvas)

        #Scrollbar
        #self.scrollBar = Scrollbar(self.canvas, orient=VERTICAL, command=self.canvas.yview)
        #self.canvas.configure(yscrollcommand=self.scrollBar.set)

        #self.parent.bind('<Configure>', lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        #self.canvas.pack(fill=BOTH, expand=True)
        #self.canvas.create_window((0, 0), window=self.frame)

        #self.scrollBar.pack(side=RIGHT, fill=Y)

        #Initial text
        self.text = "=> Pyventory, BlueArt 2025"

        #Creates the Label for displaying text
        self.mainLabel = Label(self.parent, text=self.text, font=("Arial", 16), justify="left",anchor="sw")
        self.mainLabel.pack(side="bottom", anchor="s", fill="x", padx=10, pady=10)
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

#Main Menu class, requires a parent App to sit on, buttons for other menus
class MainMenu:
    def __init__(self, parentApp: App):
        self.parentApp = parentApp
        #Parent
        self.parent = parentApp.mainFrame
        clear(self.parent)

        self.insertButton = createButton(self.parent, "Ingresar Computador", lambda : InsertMenu(self.parentApp))
        self.insertButton.config(height= 5)
        self.insertButton.pack(side=LEFT, fill=BOTH, expand=True)

        self.editButton = createButton(self.parent, "Buscar Computador", lambda: SearchMenu(self.parentApp))
        self.editButton.config(height = 5)
        self.editButton.pack(side=RIGHT, fill=BOTH, expand=True)

        self.exportButton = createButton(self.parent, "Exportar/Vista Rápida", lambda: ExportMenu(self.parentApp))
        self.exportButton.config(height = 5)
        self.exportButton.pack(side=RIGHT, fill=BOTH, expand=True)

# Insert menu class, requires a parent App to sit on, adds new computer to csv
class InsertMenu:
    def __init__(self, parentApp: App):
        self.parentApp = parentApp
        #Parent 
        self.parent = parentApp.mainFrame
        clear(self.parent)

        #Welcome message
        self.parentApp.terminal.addLine("Ha seleccionado ingresar un PC")

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
        self.parentApp.terminal.addLine("Ha seleccionado cancelar y volver al menú principal")
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
            self.entry.unbind("<Return>")
            self.parentApp.terminal.addLine("Volviendo al menú principal")
            MainMenu(self.parentApp)

# Edit menu, requiers parent App to sit on, starts the search for a PC
class SearchMenu:
    def __init__(self, parentApp: App):
        #parent Stuff
        self.parentApp = parentApp
        self.parent = parentApp.mainFrame
        clear(self.parent)
        self.subFrameLeft = Frame(self.parent)
        self.subFrameLeft.pack(side=LEFT, fill= BOTH, expand=True)
        self.subFrameRight = Frame(self.parent)
        self.subFrameRight.pack(side=RIGHT, fill= BOTH, expand=True)
        
        #Actual selected data
        self.selected: csvData | None = None

        #Welcome message
        self.parentApp.terminal.addLine("Ha seleccionado buscar un PC")

        #Menu Title
        self.label = Label(self.subFrameLeft, font=("Arial", 16), text= "Busque por número de PC")
        self.label.pack()

        #Entry with dropdown list*
        self.entry = Entry(self.subFrameLeft, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.update_list)  # Detect typing
        self.entry.bind("<Return>", self.getEntry)
        self.listbox = Listbox(self.subFrameLeft, width=30, height=5,font=("Arial", 16))
        self.listbox.bind("<ButtonRelease-1>", self.select_item)
        self.entry.bind("<FocusOut>", lambda dummyvar: self.listbox.place_forget()) #click out clears box

        #Edit Button
        self.editButton = createButton(self.subFrameRight, "Editar computador seleccionado", self.edit_item)
        self.editButton.pack(fill=BOTH, expand=TRUE)

        #delete button
        self.deleteButton = createButton(self.subFrameRight, "Eliminar computador seleccionado", self.delete_item)
        self.deleteButton.pack(fill=BOTH, expand=TRUE)

        #cancel button
        self.cancelButton = createButton(self.subFrameRight, "Volver", self.cancelCommand)
        self.cancelButton.pack(fill=BOTH, expand=TRUE)

    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.entry.unbind("<Return>")
        self.parentApp.terminal.addLine("Ha seleccionado volver al menú principal")
        MainMenu(self.parentApp)

    # gets the entry and sets the selected value to a csv
    # if no match, selected is None.
    def getEntry(self, dummyParameterForEntryBind=None):
        if self.entry.get()=="":
            self.parentApp.terminal.addLine("Porfavor escriba algo primero >:(")
            return
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

    #method for selecting from the listBox
    def select_item(self, dummyParameterForEntryBind=None):
        selected = self.listbox.get(ACTIVE)  # Get the selected item
        self.entry.delete(0, END)
        self.entry.insert(0, selected)
        self.listbox.place_forget()  # Hide the dropdown after selection

    def edit_item(self, dummyParameterForEntryBind=None):
        if self.selected == None:
            self.parentApp.terminal.addLine("Profavor seleccione un PC válido")
            return
        EditMenu(self.parentApp, self.selected)
 
    #Method for deleting the selected data from the data.txt
    def delete_item(self, dummyParameterForEntryBind=None):
        if self.selected == None:
            self.parentApp.terminal.addLine("Porfavor seleccione un PC válido")
            return
        quantity = self.parentApp.csvDelete(self.selected)
        self.parentApp.terminal.addLine(f"Se han eliminado {quantity} PCs con el número {self.selected.numero_pc}")

class EditMenu:
    def __init__(self, parentApp: App, selected_data: csvData):
        self.parentApp = parentApp
        self.selected = selected_data

        self.selectedTrait: str | None = None

        self.parent = self.parentApp.mainFrame
        clear(self.parent)
        self.subFrameLeft = Frame(self.parent)
        self.subFrameLeft.pack(fill=BOTH, expand=True, side=LEFT)
        self.subFrameRight = Frame(self.parent)
        self.subFrameRight.pack(fill=BOTH, expand=True, side=RIGHT)

        self.validTraits = header.copy()
        self.validTraits.pop(0)

        self.listbox = Listbox(self.subFrameLeft, width=30, height=5,font=("Arial", 16))
        for trait in self.validTraits:
            self.listbox.insert(END, trait)
        self.listbox.bind("<ButtonRelease-1>", self.select_trait)
        self.listbox.pack()

        self.entry = Entry(self.subFrameLeft, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<Return>", self.entryCommand)

        self.cancelButton = createButton(self.subFrameRight, "Cancelar y volver", self.cancelCommand)
        self.cancelButton.pack(fill=BOTH, expand=TRUE)

    #asdfasdfasdf
    def entryCommand(self, dummyParameterForEntryBind=None):
        if self.entry.get() == "":
            self.parentApp.terminal.addLine("Porfavor ingrese algo para editar")
            return
        if self.selectedTrait == None:
            self.parentApp.terminal.addLine("Porfavor seleccione alguna parte para editar")
            return
        self.editSelected(self.entry.get(), self.validTraits.index(self.selectedTrait) + 1)
        SearchMenu(self.parentApp)


    #asdfasdf
    def select_trait(self, dummyParameterForEntryBind=None):
        self.selectedTrait = self.listbox.get(self.listbox.curselection())
        self.parentApp.terminal.addLine(f"Ha seleccionado editar {self.selectedTrait}, el antiguo es {self.selected.exportList()[self.validTraits.index(self.selectedTrait) + 1]}")

    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.entry.unbind("<Return>")
        self.parentApp.terminal.addLine("Ha seleccionado cancelar y volver al menú de búsqueda")
        SearchMenu(self.parentApp)

    def editSelected(self, trait: str, index: int):
        oldTrait = self.selected.exportList()[index]
        result = csvEditTrait(self.selected, trait, index)
        if result:
            self.parentApp.terminal.addLine(f"El/La {header[index]} {oldTrait} ha sido cambiado por {trait}")
        else:
            self.parentApp.terminal.addLine("No se ha encontrado el pc, intentelo denuevo")

#export/quickview menu, requires parent App to sit on, lets you selct a range
#of dates and shows you the pcs and number of pcs in that range, can export to .xlsx
#with a pop up to save in the same folder as the program
class ExportMenu:
    def __init__(self, parentApp: App):
        #initializing the parents
        self.parentApp = parentApp
        self.parent = self.parentApp.mainFrame
        
        #we clear the frame so we can draw the new widgets
        clear(self.parent)

        #subframes for organizing
        self.subFrameLeft = Frame(self.parent)
        self.subFrameLeft.pack(fill=BOTH, side=LEFT)
        self.subFrameRight = Frame(self.parent)
        self.subFrameRight.pack(fill=BOTH, side=RIGHT)

        #Entries for dates
        self.dateWidth=5
        self.yearMin = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.monthMin = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.dayMin = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.yearMax = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.monthMax = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.dayMax = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.labelFrom = Label(self.subFrameLeft, text="Desde: ", font=("Arial", 14))
        self.labelTo = Label(self.subFrameLeft, text="Hasta: ", font=("Arial", 14))

        #packing the date widgets within a grid
        self.labelFrom.grid(column=0, row=0)
        self.yearMin.grid(column=1, row=0)
        self.monthMin.grid(column=2, row=0)
        self.dayMin.grid(column=3, row=0)
        self.labelTo.grid(column=0, row=1)
        self.yearMax.grid(column=1, row=1)
        self.monthMax.grid(column=2, row=1)
        self.dayMax.grid(column=3, row=1)

        #we focus on the first entry
        self.yearMin.focus_set()

        #date Variables
        self.dateFrom: datetime.datetime = datetime.datetime(1,1,1)
        self.dateTo: datetime.datetime = datetime.datetime.now()

        #display for the selected pcs
        self.displayList = Listbox(self.subFrameRight)

        #button for returning
        self.cancelButton = Button(self.subFrameLeft, command=self.cancelCommand, text="Volver", font=("Arial", 14))
        self.cancelButton.grid(column=0, row=2, columnspan=4)


    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.parentApp.terminal.addLine("Ha seleccionado volver al menú principal")
        MainMenu(self.parentApp)

    #checks for the validity of the input dates, returns false if:
    #any of the variables is None
    #the "from" date is less than the minimum date
    #the "to" date is more than the actual date
    #returns True otherwise
    def checkDateRange(self, dummyParameterForEntryBind=None) -> bool:
        datecheck=lambda date: datetime.datetime(1,1,1)<date and date<datetime.datetime.now()
        if self.dateFrom==None or self.dateTo==None:
            return False
        return datecheck(self.dateFrom) and datecheck(self.dateTo) and self.dateFrom<self.dateTo
    
    #checks the date entries for filling the date variables, if it
    #finds inconsistencies, it goes back to the defaults
    def entryToVar(self, dummyParameterForEntryBind=None):
        def quickcheck(var):
            try:
                return int(var)
            except ValueError:
                return None
            
        minyear = quickcheck(self.yearMin.get())
        minmonth = quickcheck(self.monthMin.get())
        minday = quickcheck(self.dayMin.get())
        maxyear = quickcheck(self.yearMax.get())
        maxmonth = quickcheck(self.monthMax.get())
        maxday = quickcheck(self.dayMax.get())

        if not None in (minyear, minmonth, minday):
            #self.parentApp.terminal.addLine("Porfavor ingrese un valor válido para la fecha")
            try:
                self.dateFrom = datetime.datetime(minyear, minmonth, minday)
            except ValueError:
                self.dateFrom = datetime.datetime(1,1,1)

        if not None in (maxyear, maxmonth, maxday):
            #self.parentApp.terminal.addLine("Porfavor ingrese un valor válido para la fecha")
            try:
                self.dateTo = datetime.datetime(maxyear, maxmonth, maxday)
            except ValueError:
                self.dateTo = datetime.datetime.now()
        