import tkinter as tk

from interface.styling import  *

class Logging(tk.Frame):
    def __init__(self, *args, **kwargs):  # *args means that we are allowed to pass arguments without specifying its name,
        # like we did when passing _left_frame argument  & **kwargs means that we can pass keywords arguments
        # like bg='gray12, bg=BG_COLOR
        super().__init__(*args, **kwargs)

        self.logging_text = tk.Text(self, height=10, width=60, state=tk.DISABLED, bg=BG_COLOR, fg=FG_COLOR2,
                                    font=GLOBAL_FONT)
        self.logging_text.pack(side=tk.TOP)