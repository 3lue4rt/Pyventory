import csv
import os

filename = "data.txt"

def csvINIT(mode: str) -> any | None:
    # Check if the file exists
    file_exists = os.path.exists(filename)

    with open(filename, mode=mode, newline="") as file:
        writer = csv.writer(file)
        
        # If the file is newly created, write a header
        if not file_exists:
            header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]
            writer.writerow(header) 

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

def insertarDato(dato: Dato):
    writer = csvINIT("a+")
    writer.writerow(dato.exportList())

def buscarDatoCaracteristica(caracteristica: str | int, indice: int) -> list[str] | None :
    reader = csvINIT("r")
    for row in reader:
        if len(row)>1 and row[indice]==str(caracteristica):
            return row
        
def eliminarDatoCaracteristica(caracteristica: str | int, indice: int):
    pass