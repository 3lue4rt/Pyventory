import programa as pg

#initialize
root = pg.rootInit()
frame1 = pg.createFrame(root)
frame2 = pg.createFrame(root)

### make function for buttons
insertButton = pg.createButton(frame1, "Insertar Computador", lambda : None)
editButton = pg.createButton(frame1, "Editar Computador", lambda : None)
deleteButton = pg.createButton(frame1, "Eliminar Computador", lambda : None)
searchButton = pg.createButton(frame1, "Buscar Computador", lambda : None)

### terminal
terminal = pg.Terminal(frame2)

if __name__=="__main__":
    # main loop
    root.mainloop()