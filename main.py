import programa as pg
import csvHandling as hand

#initialize
root = pg.rootInit()

main = pg.App(root)
create = hand.csvINIT("a+")




if __name__=="__main__":
    # main loop
    main.root.mainloop()