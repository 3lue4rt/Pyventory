import programa as pg
import csvHandling as hand



#initialize
root = pg.rootInit()
hand.csvINIT()
main = pg.App(root)

if __name__=="__main__":
    # main loop
    main.root.mainloop()