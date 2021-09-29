import tkinter as tk
from bitmex import get_contracts

#if __name__ == 'main_test':  # statement will be executed only if the main module will be executed

bitmex_contracts = get_contracts()

root = tk.Tk()  # main window of the bot

i = 0

for contract in bitmex_contracts:
    label_widget = tk.Label(root, text=contract)
    label_widget.grid(row=i, column=0)

    i += 1





#root = tk.Tk()
root.mainloop()
