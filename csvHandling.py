import csv
import os
from datetime import datetime

#The name of the file to work with. defaults to 'data.txt'
filename = "data.txt"

#List of columns for the csv.
header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]

#Initializes the csv document, if it doesn't exist it creates the 
#document with the template it returns False, otherwise returns True.
def csvINIT() -> bool:
    # Check if the file exists
    file_exists = os.path.exists(filename)

    with open(filename, mode="a+", newline="") as file:
        writer = csv.writer(file)
        
        # If the file is newly created, write a header
        if not file_exists:
            writer.writerow(header)

    return file_exists

#Returns True if the csv doc has the correct template, otherwise return False
def csvValidate() -> bool:
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        first = next(reader, None)  # Read the first row (header)

        return first==header

#Represents a tuple in the csv, it's composed of traits
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
        return [self.numero_pc, self.fecha, self.partida, self.placa, self.procesador, self.ram, self.ssd, self.ubicacion, self.monitor]

#turns the list of traits to data
def listToData(traitList: list[str]) -> csvData:
    return csvData(traitList[0], traitList[1], traitList[2], traitList[3],
                   traitList[4], traitList[5], traitList[6], traitList[7], traitList[8])

#Inserts the data in the csv
def csvInsert(data: csvData):
    with open(filename, mode="+a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data.exportList())

#Given a substring of a trait and it's index in the header, it searches for data in the csv document 
#and returns the list of data that contain the substring in the trait
def csvSearchBy(trait: str | int, index: int) -> list[csvData] | list[None] :
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        result: list[csvData] = []
        headerindex = True
        for row in reader:
            if len(row)>1 and not headerindex and str(trait) in row[index]:
                result.append(listToData(row))
            headerindex = False
        return result

#Given data, its searches for all tuples equal to the data and removes them returning the number
#of tuples that were equal
def csvRemove(data: csvData) -> int:
    guardar: list[str] = []
    encontrado = 0
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row==data.exportList():
                encontrado+=1
            else:
                guardar.append(row)

    if encontrado:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(guardar)

    return encontrado

#Given old Data and new Data, it searches for the first tuple that matches the old data in the csv and replaces it
#with the new data returning True, otherwise return False
def csvEdit(oldData: csvData, newData: csvData) -> bool:
    guardar: list[list[str]] = []
    encontrado = False
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row==oldData.exportList() and not encontrado:
                guardar.append(newData.exportList())
                encontrado = True
            else:
                guardar.append(row)

    if encontrado:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(guardar)

    return encontrado

#Given old Data, a new trait and it's index for the header, it searches for the old Data
#if found it replaces ONLY the old trait in the index for the new trait returning True, 
#otherwise returns False.
def csvEditTrait(oldData: csvData, newTrait: str | int, index: int) -> bool:
    traitList=oldData.exportList()
    traitList[index]=str(newTrait)

    newData= csvData(traitList[0], 
                     traitList[1], 
                     traitList[2], 
                     traitList[3], 
                     traitList[4], 
                     traitList[5], 
                     traitList[6], 
                     traitList[7], 
                     traitList[8])
    
    result = csvEdit(oldData, newData)

    return result

#given a minimum date (defaults to 1-1-1 (min date)) and a maximum date (defaults to current date)
#returns a list of data
def dataRangeDate(minDate: datetime = datetime.min, maxDate: datetime = datetime.now()) -> list[csvData]:
    result: list[csvData] = []
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if str(row[1])>=str(minDate) and str(row[1])<=str(maxDate):
                result.append(listToData(row))
    return result