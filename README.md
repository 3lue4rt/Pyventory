# Pyventory
Pyventory es un proyecto para mantener el inventario del HHHA, este repositorio solo contiene el codigo fuente de la aplicación, si quiere el ejecutable tendrá que armarlo con **pyinstaller**.

La aplicación puede ingrsar computadores, buscarlos, editarlos, eliminarlos y exportar un listado de ellos a un archivo .xlsx (excel). Esta información se guarda en un csv para un almacenamiento liviano.

### Iniciacion del Programa

Al iniciar el programa revisa si existe un archivo llamado *data.csv*. Si no existe
crea uno nuevo. Es importante **no modificar este archivo**, ya que su alteración podría significar
un error en el programa o su **inutilización por completo**.

## Ingresar un Computador

Se le pedirá poner las carácteristicas del computador en el siguiente orden:

1. Número de pc: No puede repetirse (llave primaria) y **solo puede ser de 4 digitos**.

2. Fecha: Ocupa el formato *'AAAA-MM-DD HH:MM:SS'*, pero si no se ingresa nada se ingresa automaticamente el instante que se ingresa. Al exportar mantiene el formato fecha en el excel.

3. Partida: Al escribir se muestran sugerencias de partidas anteriores

4. Placa

5. Procesador

6. RAM

7. SSD

8. Ubicación: Al escribir se muestran sugerencias de ubicaciones anteriores

9. Monitor

## Buscar/Editar/Eliminar un Computador

En este menu se pedirá buscar un PC a partir de su número.

Despues de ser seleccionado se podrá acceder a dos menus, el de editar
y el de eliminar.

- Editar: se pedirá elegir una de las partes antiguas del computador
y al ingresar una parte nueva en la barra de ingreso se cambiará la parte antigua
por la nueva.

- Eliminar: esto abrirá una ventana nueva que le pedirá escribir "eliminar" para
borrar de manera definitiva el computador. Si no lo desea puede cerrar la ventana o
apretar \<Esc\>.

## Exportar computadores

En este menu se pueden seleccionar los computadores ingresados en un rango de fechas,
los cuales se verán visualizados en un listado a la derecha, por número de PC.

Por defecto, la fecha mínima es 1-1-1 y la máxima es el instante en que se abre el programa.

Uno puede ingresar fechas para los límites superiores e inferiores. Si no está completa la fecha
o se ingresa una fecha incorrecta (ej: 30-2-20xx) al poner \<Enter\> se ocupan las por defecto.

Al apretar importar se abrirá una ventana donde se podrá ingresar el nombre del documento. Se filtran
los nombres que incumplen las restricciones de nombramiento de Windows. Automaticamente se ingresa el sufijo
*.xlsx* si no tiene. El archivo se guarda en la misma carpeta que el programa.

## Instalación de la Aplicación

Se ocupó **pyinstaller** para crear el ejecutable de windows. Este programa ocupa: las librerías de
Tkinter, csv y openpyxl, esta última teniendose que instalar.

*En este repositorio solo se guarda el codigo base de la aplicación.*

> Benjamín "BlueArt" Duarte, 02/2025