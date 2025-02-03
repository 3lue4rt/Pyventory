import csv
import os

'''
Interface for csvHandling:

    filename: str
    The name of the file to work with. defaults to 'data.txt'

    header: list[str]
    List of columns for the csv. 
    Defaults to ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]

    def csvInit() => Bool: 
    Initializes the csv document, if it doesn't exist it creates the 
    document with the template it returns False, otherwise returns True.

    def csvValidation() => Bool:
    Returns True if the csv doc has the correct template, otherwise return False

    class csvData(numero_pc, fecha, partida, placa, procesador, ram, ssd, ubicacion, monitor): 
    Represents a tuple in the csv, it's composed of traits
        def exportList() => list[str]:
        exports the data as a list of traits

    def csvInsert(dato: Dato) => None: 
    Inserts the data in the csv

    def csvSearchBy(trait: str | int, index: int) => list[str] | None :
    Given a trait and it's index in the header, it searches for data in the csv document 
    and returns the list of data that contain that trait

    def csvRemove(data: Data) => bool:
    Given data, its searches for it and removes it returning True, otherwise False.

    def csvEdit(oldData: Data, newData: Data) => bool:
    Given old Data and new Data, it searches for the old data in the csv and replaces it
    with the new data returning True, otherwise return False

    def csvEditTrait(oldData: Data, newTrait: str | int, index: int) => bool:
    Given old Data, a new trait and it's index for the header, it searches for the old Data
    if found it replaces ONLY the old trait in the index for the new trait returning True, 
    otherwise returns False.

'''

filename = "data.txt"

header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]

def csvINIT() -> bool:
    # Check if the file exists
    file_exists = os.path.exists(filename)

    with open(filename, mode="a+", newline="") as file:
        writer = csv.writer(file)
        
        # If the file is newly created, write a header
        if not file_exists:
            writer.writerow(header)

    return file_exists

def csvValidate() -> bool:
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        first = next(reader, None)  # Read the first row (header)

        return first==header

class csvData:
    def __init__(self, numero_pc, fecha, partida, placa, procesador, ram, ssd, ubicacion, monitor):
        self.numero_pc = numero_pc
        self.fecha = fecha
        self.partida = partida
        self.placa = placa
        self.procesador = procesador
        self.ram = ram
        self.ssd = ssd
        self.ubicacion = ubicacion
        self.monitor = monitor

    def exportList(self) -> list[str]:
        [self.numero_pc, self.fecha, self.partida, self.placa, self.procesador, self.ram, self.ssd, self.ubicacion, self.monitor]

def insertarDatoCSV(dato: csvData):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(dato.exportList())

def buscarDatoCaracteristicaCSV(caracteristica: str | int, indice: int) -> list[str] | None :
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row)>1 and row[indice]==str(caracteristica):
                return row
        
def eliminarDatoCaracteristicaCSV(caracteristica: str | int, indice: int) -> bool:
    guardar: list[str] = []
    encontrado = False
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row)>1 and row[indice]==caracteristica:
                encontrado = True
            else:
                guardar.append(row)

    if encontrado:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]
            writer.writerow(header)
            writer.writerows(guardar)

    return encontrado

