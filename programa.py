version = "1.0 Primal Pine, BlueArt 2025"

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

#colors
black = "#1D1E18"
reseda_green = "#6B8F71"
celadon = "#AAD2BA"
mint_green = "#D9FFF5"
celados = "#B9F5D8"

#creates a Button given a frame, name and function, it defaults to 
#using the defined colors at the top of the script, it also automatically
#packs the button and returns the Button() obj.
def createButton(frame: Frame, name: str, func: types.FunctionType) -> Button:
    button = Button(frame, #parent
                    text=name, #text in the button
                    font=("Arial", 14), #font for the text
                    command= func, #function assigned to the button
                    background=celadon, #background color (unpressed)
                    foreground="Black", #text color (unpressed)
                    activebackground=mint_green, #background color (pressed)
                    activeforeground=black) #text color (pressed)
    button.pack(fill="both") #places the button filling the space
    return button

#Clears a Frame of all their widgets
def clear(frame: Frame):
    for widget in frame.winfo_children():
        widget.pack_forget()

#App class for initializing the application, it is passed around
#the menu classes for access to the terminal and frames.
# it ISN'T responsible for cleaning the frames after a menu
# is done.
class App:
    def __init__(self):
        #Creates the root
        self.root = Tk()
        self.root.title("Pyventory")
        self.root.geometry("800x450")

        #Creates the Frame for the menu
        self.mainFrame = Frame(self.root, padx=10, pady=10, background=black)
        self.mainFrame.pack(fill="both")

        #Creates the Main Menu in the respective Frame
        self.mainMenu = MainMenu(self)

        #Creates the Frame for the terminal
        self.terminalFrame = Frame(self.root, padx=10, pady=10, background=black)
        self.terminalFrame.pack(fill="both", expand=True)

        #Creates the Terminal in the respective Frame
        self.terminal = Terminal(self)

        #Starts the csv Importer and checks if the file exists, if not creates one
        fileExists = csvINIT()
        if not fileExists:
            self.terminal.addLine("No se encontró ningun archivo data, se ha creado uno nuevo")
        isValid = csvValidate()
        if not isValid:
            self.terminal.addLine("El archivo no tiene el formato correcto... guarde los datos a mano y borre el archivo para restaurar")

        self.root.bind("credits", lambda event: print(version))

    #imports data to the csv
    def csvImport(self, data: csvData):
        csvInsert(data)
        self.terminal.addLine(f"Se ha agregado exitosamente el computador {data.exportList()[0]} a {filename}")

    #returns a list of data given a substring of a trait
    def csvSearch(self, trait: str, index: int) -> list[csvData]:
        return csvSearchBy(trait, index)
    
    #deletes data from the data csv
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
        self.mainLabel = Label(self.parent, 
                               text=self.text, 
                               font=("Arial", 16), 
                               justify="left",
                               anchor="sw", 
                               background=black,
                               foreground=mint_green)
        self.mainLabel.pack(side="bottom", anchor="s", fill="x", padx=10, pady=10)
        self.mainLabel.bind('<Configure>', lambda e: self.mainLabel.config(wraplength=self.mainLabel.winfo_width()))


    #Updates the text in the Label with the self.text string
    def update(self):
        self.mainLabel.config(text = self.text)

    #Adds a line of text to the bottom of the Label
    # NEEDS TESTING FOR OVERFLOW
    def addLine(self, text: str):
        self.text += "\n\n=> "+text
        self.update()

    #Deletes all text in Label
    def deleteText(self):
        self.text = "=> "
        self.update()

#Main Menu class, requires a parent App to sit on, buttons for other menus,
#menus are responsible for cleaning themselves up, that means unbinding the hotkeys
#and cleaning the widgets from the frame So the next menu works without side-effects
class MainMenu:
    def __init__(self, parentApp: App):
        self.parentApp = parentApp
        #Parent
        self.parent = parentApp.mainFrame
        #clears leftovers
        clear(self.parent)

        #button for insert menu
        self.insertButton = createButton(self.parent, "Ingresar Computador \n(i)", 
                                         lambda: self.menu_bind(0, InsertMenu))
        self.parentApp.root.bind("i", lambda event: self.menu_bind(event, InsertMenu)) #hotkey
        self.insertButton.config(height= 5)
        self.insertButton.pack(side=LEFT, fill=BOTH, expand=True)

        #button for edit menu
        self.editButton = createButton(self.parent, "Buscar/Editar/Eliminar Computador \n(b)", 
                                       lambda : self.menu_bind(0, SearchMenu))
        self.parentApp.root.bind("b", lambda event: self.menu_bind(event, SearchMenu)) #hotkey
        self.editButton.config(height = 5)
        self.editButton.pack(side=RIGHT, fill=BOTH, expand=True)

        #button for export menu
        self.exportButton = createButton(self.parent, "Exportar/Vista Rápida \n(e)", 
                                         lambda : self.menu_bind(0, ExportMenu))
        self.parentApp.root.bind("e", lambda event: self.menu_bind(event, ExportMenu)) #hotkey
        self.exportButton.config(height = 5)
        self.exportButton.pack(side=RIGHT, fill=BOTH, expand=True)

    #method for changing menu, it unbinds the hotkeys it assigned
    def menu_bind(self, event=None,Menu=None):
        self.parentApp.root.unbind("i")
        self.parentApp.root.unbind("b")
        self.parentApp.root.unbind("e")
        for widget in self.parent.winfo_children():
            widget.destroy()
        Menu(self.parentApp)

# Insert menu class, requires a parent App to sit on, adds new computer to csv
#menus are responsible for cleaning themselves up, that means unbinding the hotkeys
#and cleaning the widgets from the frame So the next menu works without side-effects
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
        self.label = Label(self.parent, 
                           text=self.header[self.index], 
                           font=("Arial", 16), 
                           background=celadon,
                           foreground="black",
                           padx=10,
                           pady=10)
        self.label.pack()
        
        #Entry for traits from the User, make() method dictates the input structure
        self.entry = Entry(self.parent, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<Return>", self.make)
        self.entry.focus_set()

        #Listbox for some traits
        self.listBox = Listbox(self.parent, font=("Arial", 16), height=5, width=50)
        self.entry.bind("<KeyRelease>", self.update_list)
        self.entry.bind("<Down>", self.setListBoxFocus)
        self.listBox.bind("<Return>", self.select_trait)
        self.listBox.pack()

        #cancelmenu
        self.cancelButton = createButton(self.parent, "Cancelar y Volver\n<Esc>", self.cancelCommand)
        self.parentApp.root.bind("<Escape>", self.cancelCommand)
        self.cancelButton.pack_configure(fill="none", expand=False)

    #method for own arrowing from the entry so that it selects the first element 
    #from the listbox
    def setListBoxFocus(self, event=None):
        self.listBox.focus()
        self.listBox.select_set(0)

    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.entry.unbind("<Return>")
        self.parentApp.root.unbind("<Escape>")
        self.entry.unbind("<KeyRelease>")
        self.entry.unbind("<Down>")
        self.listBox.unbind("<Return>")
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parentApp.terminal.addLine("Ha seleccionado cancelar y volver al menú principal")
        MainMenu(self.parentApp)

    #handles the building of the data, which will be inserted when the 
    #promps end
    def make(self, dummyParameterForEntryBind=None):
        #Automatically enters actual date if nothing is entered
        if self.index==1 and self.entry.get()=="":
            self.result.append(str(datetime.datetime.now()))
            self.index += 1
            self.label.config(text=self.header[self.index])
            self.parentApp.terminal.addLine(f"se ha ingresado hasta ahora: {self.result}")
            return

        #Handles no entry by the user
        #elif self.entry.get()=="":
        #    self.parentApp.terminal.addLine("No se puede ingresar nada, ingrese algo")

        #No empty ID
        if self.index==0 and self.entry.get()=="":
            self.parentApp.terminal.addLine(f"Porfavor ingrese un número de PC")
            return
        #No repeating ID
        if self.index==0 and csvSearchBy(self.entry.get(), 0):
            self.parentApp.terminal.addLine(f"Ese numero de PC ya fue ocupado, edite o elimine el antiguo.")
            return
        #general case
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
            self.parentApp.root.unbind("<Escape>")
            self.entry.unbind("<KeyRelease>")
            self.entry.unbind("<Down>")
            self.listBox.unbind("<Return>")
            self.parentApp.terminal.addLine("Volviendo al menú principal")
            for widget in self.parent.winfo_children():
                widget.destroy()
            MainMenu(self.parentApp)

    #handles selecting the trait from the listBox hotkey <Return>
    def select_trait(self, event = None):
        selected = self.listBox.get(self.listBox.curselection())  # Get the selected item
        self.entry.delete(0, END)
        self.entry.insert(0, selected)
        self.entry.focus()

    #fills the listbox with the known traits
    def update_list(self, dummyParameterForEntryBind=None): # Clear previous items
        self.listBox.delete(0, END)
        if self.index!=2 and self.index!=7:
            return
        if self.entry.get():  # Show matching items
            filtered = set(thing.exportList()[self.index] for thing in self.parentApp.csvSearch(self.entry.get(), self.index))
            for item in filtered:
                self.listBox.insert(END, item)

# Search menu, requires parent App to sit on, starts the search for a PC
#menus are responsible for cleaning themselves up, that means unbinding the hotkeys
#and cleaning the widgets from the frame So the next menu works without side-effects
class SearchMenu:
    def __init__(self, parentApp: App):
        #parent Stuff
        self.parentApp = parentApp
        self.parent = parentApp.mainFrame
        clear(self.parent)

        #subframing so the widgets can be better organized
        self.subFrameLeft = Frame(self.parent, background=black)
        self.subFrameLeft.pack(side=LEFT, fill= BOTH, expand=True)
        self.subFrameRight = Frame(self.parent, background=black)
        self.subFrameRight.pack(side=RIGHT, fill= BOTH, expand=True)
        
        #Actual selected data
        self.selected: csvData | None = None

        #Welcome message
        self.parentApp.terminal.addLine("Ha seleccionado buscar un PC")

        #Menu Title
        self.label = Label(self.subFrameLeft, 
                           font=("Arial", 16), 
                           text= "Busque por número de PC",
                           background=celadon)
        self.label.pack()

        #Entry with dropdown list*
        self.entry = Entry(self.subFrameLeft, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.update_list)  # Detect typing
        self.entry.bind("<Return>", self.getEntry)
        self.listbox = Listbox(self.subFrameLeft, width=30, height=5,font=("Arial", 16))
        self.listbox.bind("<ButtonRelease-1>", self.select_item)
        self.listbox.bind("<Return>", self.select_item)
        self.entry.bind("<FocusOut>", lambda dummyvar: self.listbox.place_forget()) #click out clears box
        self.entry.bind("<Down>", self.select_from_entry) #select the first item in listbox when in entry

        #Edit Button
        self.editButton = createButton(self.subFrameRight, "Editar computador seleccionado\n<Ctrl+e>", self.edit_item)
        self.parentApp.root.bind("<Control-e>", self.edit_item)
        self.editButton.pack(fill=BOTH, expand=TRUE)

        #delete button
        self.deleteButton = createButton(self.subFrameRight, "Eliminar computador seleccionado\n<Ctrl+d>", self.delete_item)
        self.parentApp.root.bind("<Control-d>", self.delete_item)
        self.deleteButton.pack(fill=BOTH, expand=TRUE)

        #cancel button
        self.cancelButton = createButton(self.subFrameRight, "Volver\n<Esc>", self.cancelCommand)
        self.parentApp.root.bind("<Escape>", self.cancelCommand)
        self.cancelButton.pack(fill=BOTH, expand=TRUE)

        self.entry.focus() #focus on the entry when started

    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.entry.unbind("<Return>")
        self.entry.unbind("<KeyRelease>")
        self.entry.unbind("<FocusOut>")
        self.entry.unbind("<Down>")
        self.listbox.unbind("<ButtonRelease-1>")
        self.listbox.unbind("<Return>")
        self.parentApp.root.unbind("<Escape>")
        self.parentApp.root.unbind("<Control-e>")
        self.parentApp.root.unbind("<Control-d>")
        for widget in self.parent.winfo_children():
            widget.destroy()
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
        selected = self.listbox.get(self.listbox.curselection())  # Get the selected item
        self.entry.delete(0, END)
        self.entry.insert(0, selected)
        self.entry.focus()
        self.listbox.place_forget()  # Hide the dropdown after selection

    #cleans the frame and unbinds to access the edit menu
    def edit_item(self, dummyParameterForEntryBind=None):
        if self.selected == None:
            self.parentApp.terminal.addLine("Porfavor seleccione un PC válido")
            return
        self.entry.unbind("<Return>")
        self.entry.unbind("<KeyRelease>")
        self.entry.unbind("<FocusOut>")
        self.entry.unbind("<Down>")
        self.listbox.unbind("<ButtonRelease-1>")
        self.listbox.unbind("<Return>")
        self.parentApp.root.unbind("<Escape>")
        self.parentApp.root.unbind("<Control-e>")
        self.parentApp.root.unbind("<Control-d>")
        for widget in self.parent.winfo_children():
            widget.destroy()
        EditMenu(self.parentApp, self.selected)

    def select_from_entry(self, event=None):
        self.listbox.focus()
        self.listbox.select_set(0)
 
    #Method for deleting the selected data from the data.txt
    def delete_item(self, dummyParameterForEntryBind=None):
        if self.selected == None:
            self.parentApp.terminal.addLine("Porfavor seleccione un PC válido")
            return
        DeletePopUp(self.parentApp, self.selected)
        #quantity = self.parentApp.csvDelete(self.selected)
        #self.parentApp.terminal.addLine(f"Se han eliminado {quantity} PCs con el número {self.selected.numero_pc}")

#popup window for deleting
class DeletePopUp:
    def __init__(self, parentApp:App, selected: csvData):
        #parent stuff
        self.parentApp = parentApp

        #selected data to delete
        self.selected = selected

        #creates the popup
        self.popUp = Toplevel(self.parentApp.root)

        #frame in the popup
        self.parent = Frame(self.popUp, background=black)

        #label 1
        self.label = Label(self.parent, 
                           text=f"¿Está seguro que quiere eliminar el computador: {self.selected.numero_pc}?",
                           background=black,
                           foreground=mint_green,
                           font=("Arial", 16))
        
        #label 2
        self.options = Label(self.parent,
                             text= "Escriba eliminar para confirmar\nPresione <Esc> para abortar",
                             background=black,
                             foreground=mint_green,
                             font=("Arial", 16))
        #packing stuff
        self.parent.pack(fill=BOTH, expand=True)
        self.label.pack()
        self.options.pack()

        #bind the hotkeys
        self.popUp.bind("eliminar", self.handleDelete)
        self.popUp.bind("<Escape>", self.handleEscape)

        #automatic focus on the window
        self.popUp.focus()
        
    #handles if user chooses delete, cleans up the popup
    def handleDelete(self, event=None):
        quantity = self.parentApp.csvDelete(self.selected)
        self.parentApp.terminal.addLine(f"Se han eliminado {quantity} PCs con el número {self.selected.numero_pc}")
        self.popUp.destroy()

    #handles if users cancels, cleans the popup
    def handleEscape(self, event=None):
        self.parentApp.terminal.addLine("Proceso abortado")
        self.popUp.destroy()

# Edit menu, requires parent App to sit on, given a selected data it edits it
#menus are responsible for cleaning themselves up, that means unbinding the hotkeys
#and cleaning the widgets from the frame So the next menu works without side-effects
class EditMenu:
    def __init__(self, parentApp: App, selected_data: csvData):
        #parent stuff
        self.parentApp = parentApp
        self.selected = selected_data

        #selected trait to edit
        self.selectedTrait: str | None = None

        #more parent stuff
        self.parent = self.parentApp.mainFrame
        clear(self.parent)

        #subframing for organizing
        self.subFrameLeft = Frame(self.parent, background=black)
        self.subFrameLeft.pack(fill=BOTH, expand=True, side=LEFT)
        self.subFrameRight = Frame(self.parent, background=black)
        self.subFrameRight.pack(fill=BOTH, expand=True, side=RIGHT)

        #list for organizing the traits of the selected data
        self.validTraits = header.copy()
        self.validTraits.pop(0)
        self.validTraits = list(trait+f": {self.selected.exportList()[self.validTraits.index(trait) + 1]}" for trait in self.validTraits)

        #Listbox containing the old traits
        self.listbox = Listbox(self.subFrameLeft, width=30, height=5,font=("Arial", 16))
        for trait in self.validTraits:
            self.listbox.insert(END, trait)
        self.listbox.bind("<ButtonRelease-1>", self.select_trait)
        self.listbox.focus()
        self.listbox.select_set(0)
        self.listbox.bind("<Return>", self.select_trait)
        self.listbox.pack()

        #entry for editing
        self.entry = Entry(self.subFrameLeft, width=30, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<Return>", self.entryCommand)

        #cancel button
        self.cancelButton = createButton(self.subFrameRight, "Cancelar y volver\n<Esc>", self.cancelCommand)
        self.parentApp.root.bind("<Escape>", self.cancelCommand)
        self.cancelButton.pack(fill=BOTH, expand=TRUE)

    #handles non selected traits and no entry, if conditions are met
    #it edits the selected trait by the entry promp and
    #returns to the search menu cleaning after themselves
    def entryCommand(self, dummyParameterForEntryBind=None):
        if self.entry.get() == "":
            self.parentApp.terminal.addLine("Porfavor ingrese algo para editar")
            return
        if self.selectedTrait == None:
            self.parentApp.terminal.addLine("Porfavor seleccione alguna parte para editar")
            return
        self.entry.unbind("<Return>")
        self.parentApp.root.unbind("<Escape>")
        self.editSelected(self.entry.get(), self.validTraits.index(self.selectedTrait) + 1)
        for widget in self.parent.winfo_children():
            widget.destroy()
        SearchMenu(self.parentApp)


    #<Return> binding for listbox
    def select_trait(self, dummyParameterForEntryBind=None):
        self.selectedTrait = self.listbox.get(self.listbox.curselection())
        self.parentApp.terminal.addLine(f"Ha seleccionado editar {self.selectedTrait}")
        self.entry.focus()

    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.entry.unbind("<Return>")
        self.parentApp.root.unbind("<Escape>")
        self.parentApp.terminal.addLine("Ha seleccionado cancelar y volver al menú de búsqueda")
        for widget in self.parent.winfo_children():
            widget.destroy()
        SearchMenu(self.parentApp)


    #changes the trait (object atribute) of self.selected (Data) 
    #by trait (parameter) and index (parameter) indicates which one
    def editSelected(self, trait: str, index: int):
        oldTrait = self.selected.exportList()[index]
        result = csvEditTrait(self.selected, trait, index)
        if result:
            self.parentApp.terminal.addLine(f"El/La {header[index]} {oldTrait if oldTrait else "<NADA>"} ha sido cambiado por {trait}")
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
        self.subFrameLeft = Frame(self.parent,background=black)
        self.subFrameLeft.pack(fill=BOTH, side=LEFT)
        self.subFrameRight = Frame(self.parent,background=black)
        self.subFrameRight.pack(fill=BOTH, side=RIGHT)

        #Entries for dates
        self.dateWidth=10
        self.yearMin = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.monthMin = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.dayMin = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.yearMax = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.monthMax = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.dayMax = Entry(self.subFrameLeft, font=("Arial", 14), width=self.dateWidth)
        self.labelFrom = Label(self.subFrameLeft, text="Desde: ", font=("Arial", 14),background=black, foreground=mint_green)
        self.labelTo = Label(self.subFrameLeft, text="Hasta: ", font=("Arial", 14),background=black, foreground=mint_green)
        self.dia = Label(self.subFrameLeft, text="Día:", font=("Arial", 14),background=black, foreground=mint_green)
        self.mes = Label(self.subFrameLeft, text="Mes:", font=("Arial", 14),background=black, foreground=mint_green)
        self.anho = Label(self.subFrameLeft, text="Año:", font=("Arial", 14),background=black, foreground=mint_green)

        #easy hotkeys
        self.dayMin.bind("<Return>", lambda event: self.dateBind(event, self.monthMin))
        self.monthMin.bind("<Return>", lambda event: self.dateBind(event, self.yearMin))
        self.yearMin.bind("<Return>", lambda event: self.dateBind(event, self.dayMax))
        
        self.dayMax.bind("<Return>", lambda event: self.dateBind(event, self.monthMax))
        self.monthMax.bind("<Return>", lambda event: self.dateBind(event, self.yearMax))
        self.yearMax.bind("<Return>", lambda event: self.dateBind(event, self.dayMin))

        #packing the date widgets within a grid
        self.dia.grid(column=1, row=0)
        self.mes.grid(column=2, row=0)
        self.anho.grid(column=3, row=0)

        self.labelFrom.grid(column=0, row=1)

        self.dayMin.grid(column=1, row=1)
        self.monthMin.grid(column=2, row=1)
        self.yearMin.grid(column=3, row=1)
    
        self.labelTo.grid(column=0, row=2)

        self.dayMax.grid(column=1, row=2)
        self.monthMax.grid(column=2, row=2)
        self.yearMax.grid(column=3, row=2)

        #we focus on the first entry
        self.dayMin.focus_set()

        #date Variables
        self.dateFrom: datetime.datetime = datetime.datetime(1,1,1)
        self.dateTo: datetime.datetime = datetime.datetime.now()

        #display for the selected pcs
        self.displayList = Listbox(self.subFrameRight, font=("Arial", 16), height=5)
        self.displayList.pack(fill=BOTH, expand=True)
        self.updateList()

        #button for exporting
        self.exportButton = Button(self.subFrameLeft, 
                                   command= lambda: ExportWindow(self), 
                                   text="Exportar seleccionados <Ctrl+e>", 
                                   font=("Arial", 14),
                                   background=celadon,
                                   activebackground=mint_green,
                                   activeforeground=black)
        self.parentApp.root.bind("<Control-e>", lambda event: ExportWindow(self))
        self.exportButton.grid(column=1, row=3, columnspan=3)

        #button for returning
        self.cancelButton = Button(self.subFrameLeft, 
                                   command=self.cancelCommand, 
                                   text="Volver <Esc>", 
                                   font=("Arial", 14),
                                   background=celadon)
        self.parentApp.root.bind("<Escape>", self.cancelCommand)
        self.cancelButton.grid(column=2, row=4)


    #function for cancelButton for going back to the menu
    def cancelCommand(self, dummyParameterForEntryBind=None):
        self.parentApp.root.unbind_all("<Return>")
        self.parentApp.root.unbind("<Escape>")
        self.parentApp.root.unbind("<Control-e>")
        self.parentApp.terminal.addLine("Ha seleccionado volver al menú principal")
        for widget in self.parent.winfo_children():
            widget.destroy()
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
        else: 
            self.dateFrom = datetime.datetime(1,1,1)

        if not None in (maxyear, maxmonth, maxday):
            #self.parentApp.terminal.addLine("Porfavor ingrese un valor válido para la fecha")
            try:
                self.dateTo = datetime.datetime(maxyear, maxmonth, maxday)
            except ValueError:
                self.dateTo = datetime.datetime.now()
        else:
            self.dateTo = datetime.datetime.now()

        #updates the list with the valid entries
    
    #updates the list for the valid dates
    def updateList(self, dummyParameterForEntryBind=None):
        result = dataRangeDate(self.dateFrom, self.dateTo)
        self.displayList.delete(0, END)
        for data in result:
            self.displayList.insert(END, data.exportList()[0])

    def dateBind(self, event, next: Entry):
        acumulable = ""
        if not self.checkDateRange():
            acumulable += "La fecha actual no es válida en su totalidad\n"

        self.entryToVar()
        acumulable += "Se ha elegido hasta ahora:\n"
        acumulable += f"Desde: {self.dateFrom}\n"
        acumulable += f"Hasta: {self.dateTo}\n"
        self.updateList()
        next.focus_set()
        acumulable += f"El total de computadores seleccionados es {len(dataRangeDate(self.dateFrom, self.dateTo))}"
        self.parentApp.terminal.addLine(acumulable)

#export menu popup for saving the document, needs the export menu as a parameter for easy access to dates
class ExportWindow:
    def __init__(self, exportMenu: ExportMenu):
        #parent stuff
        self.parentMenu = exportMenu
        self.parentApp = self.parentMenu.parentApp
        self.parent = self.parentApp.mainFrame

        #popup
        self.popUp = Toplevel(self.parentApp.root)
        self.popUp.title("Exportando...")
        self.popUp.geometry("400x200")
        self.frame = Frame(self.popUp, background=black)
        self.frame.pack(fill=BOTH, expand=True)

        self.label = Label(self.frame, 
                           text=f'''Está exportando {len(dataRangeDate(self.parentMenu.dateFrom, self.parentMenu.dateTo))} elementos, escriba el nombre del archivo a guardar:''', 
                           font=("Arial", 14),
                           background=black,
                           foreground=mint_green)
        self.label.bind('<Configure>', lambda e: self.label.config(wraplength=self.label.winfo_width()))
        self.label.pack()

        self.entry = Entry(self.frame, font=("Arial", 14))
        self.entry.bind("<Return>", lambda event: self.exportData(event, self.entry.get()))
        self.entry.pack()
        self.entry.focus()

    #handles the good naming of the document (WINDOWS REGEX) and saves it wih the
    #user given name
    def exportData(self, event=None, name = "inventario"):
        result = dataRangeDate(self.parentMenu.dateFrom, self.parentMenu.dateTo)
        book = Workbook()
        book.active.append(header)
        expAppend(book, result)
        book.active.column_dimensions["A"].width = 15
        book.active.column_dimensions["B"].width = 20
        book.active.column_dimensions["C"].width = 10
        book.active.column_dimensions["D"].width = 28
        book.active.column_dimensions["E"].width = 20
        book.active.column_dimensions["F"].width = 15
        book.active.column_dimensions["G"].width = 15
        book.active.column_dimensions["H"].width = 40
        book.active.column_dimensions["I"].width = 20

        if expSave(book, name):
            self.parentApp.terminal.addLine(f"Se ha guardado exitosamente el documento {name}")
            self.popUp.destroy()
        else:
            self.parentApp.terminal.addLine("No se ha podido guardar el documento, el nombre no es aceptable")
