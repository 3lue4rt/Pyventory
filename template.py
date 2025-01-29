from openpyxl import Workbook

workbook = Workbook()

workbook.iso_dates = True

worksheet = workbook.active

header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]

worksheet.append(header)



#tupla en una columna
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

