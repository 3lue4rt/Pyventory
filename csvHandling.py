import csv
import os

filename = "data.txt"

def csvINIT() -> None:
    # Check if the file exists
    file_exists = os.path.exists(filename)

    with open(filename, mode="a+", newline="") as file:
        writer = csv.writer(file)
        
        # If the file is newly created, write a header
        if not file_exists:
            header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]
            writer.writerow(header)

def csvAPPEND():
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
    return writer

def csvREADER():
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
    return reader

def csvWRITER():
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
    return writer

class Dato:
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

def insertarDatoCSV(dato: Dato):
    writer = csvWRITER()
    writer.writerow(dato.exportList())

def buscarDatoCaracteristicaCSV(caracteristica: str | int, indice: int) -> list[str] | None :
    reader = csvREADER()
    for row in reader:
        if len(row)>1 and row[indice]==str(caracteristica):
            return row
        
def eliminarDatoCaracteristicaCSV(caracteristica: str | int, indice: int) -> bool:
    guardar: list[str] = []
    encontrado = False
    reader = csvREADER()
    for row in reader:
        if len(row)>1 and row[indice]==caracteristica:
            encontrado = True
        else:
            guardar.append(row)

    if encontrado:
        writer = csvWRITER()
        header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]
        writer.writerow(header)
        writer.writerows(guardar)

    return encontrado

