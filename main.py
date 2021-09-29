import tkinter as tk
import logging

from binance_futures import get_contracts

logger = logging.getLogger()

logger.setLevel(logging.INFO)  # min logger level (for the 'Debug' level of message to show in info.log change to logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()  # to show up messages in Python terminal
formatter = logging.Formatter('%(asctime)s %(levelname)s  :: %(message)s')  # message what we want is to show (%current time of the log, %logging level,
stream_handler.setFormatter(formatter)  # add formatter to the stream_handler
stream_handler.setLevel(logging.INFO)  # log level of stream_handler

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)  # add stream_handler to the logger instance
logger.addHandler(file_handler)

if __name__ == '__main__':  # statement will be executed only if the main module will be executed

    binance_contracts = get_contracts()

    root = tk.Tk()  # main window of the bot



    for contract in binance_contracts:
        label_widget = tk.Label(root, text=contract)
        label_widget.pack(side=tk.LEFT)  # TOP,BOTTOM,LEFT,RIGHT # .pack method places widgets relatively to each other
        #label_widget.grid(side=tk.BOTTOM)  # .grid method can specify the column and row number of each widget


    root.mainloop()  # blocking func that prevent program from terminating ('event loop' func - wait for action from user)
