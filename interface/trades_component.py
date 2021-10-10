import tkinter as tk

from interface.styling import *


class TradesWatch(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.body_widgets = dict()

        self._headers = ['time', 'symbol', 'exchange', 'strategy', 'side', 'quantity', 'status', 'pnl']

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)

        for idx, h in enumerate(self._headers):
            header = tk.Label(self._table_frame, text=h.capitalize(), bg=BG_COLOR,
                              fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0, column=idx)

        for h in self._headers:
            self.body_widgets[h] = dict()
            if h in ['status', 'pnl']:
                self.body_widgets[h + '_var'] = dict()

        self._body_index = 1