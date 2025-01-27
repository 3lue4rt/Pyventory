from openpyxl import Workbook

workbook = Workbook()

worksheet = workbook.active

header = ["Número PC", "Fecha", "Partida", "Placa", "Procesador", "RAM", "SSD", "Ubicación", "Monitor"]

worksheet.append(header)

workbook.save("..\\test.xlsx")