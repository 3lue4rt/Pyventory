try:
    from tkinter import *
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")

try:
    from tkinter import ttk
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")

from template import *

root = Tk()
root.title("Pyventory")
root.geometry("300x400")

entry = Entry(root, width=20, font=("Arial", 18), justify="right")
entry.pack(pady=10)

buttons_frame = Frame(root)
buttons_frame.pack()

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('0', 4, 1),
    ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3),
    ('C', 4, 0), ('=', 4, 2)
]

def on_button_click(value):
    
    if value == "C":
        entry.delete(0, END)

    elif value == "=":
        try:
            result=str(eval(entry.get()))
            entry.delete(0, END)
            entry.insert(END, result)
            
        except Exception:
            entry.delete(0, END)
            entry.insert(END, "Error")
    else:
        entry.insert(END, value)
    

for (text, row, col) in buttons:
    button = Button(buttons_frame, text=text, font=("Arial", 14), height=2, width=5,
                       command=lambda t=text: on_button_click(t))
    button.grid(row=row, column=col, padx=5, pady=5)


if __name__=="__main__":
    root.mainloop()

