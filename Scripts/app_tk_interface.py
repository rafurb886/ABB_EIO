import tkinter as tk
from tkinter import ttk

color_background = '#373737'
color_background_2 = '#737373'


class TkAppInterface():

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ABB signals translator')
        self.window.config(padx=20, pady=20, bg=color_background)

        self.logo_robotycy = tk.PhotoImage(file='H:\PythonProjects\ABB_EIO_translation\images\logo_robotycy.png')
        self.style_1 = ttk.Style()
        self.style_1.element_create("RoundedFrame",
                             "image", self.logo_robotycy,
                             border=16, sticky="nsew")
        self.style_1.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
        self.frame_title = ttk.Frame(style="RoundedFrame", master=self.window, width=150, height=50)
        self.frame_title.grid(row=0, column=3)
        self.label_title = tk.Label(text='EIO converter', bg=color_background_2)
        self.label_title.grid(row=0, column=1)

        self.label_logo = tk.Label(image=self.logo_robotycy, highlightthickness=0, borderwidth=0)
        self.label_logo.grid(row=0, column=3)
        self.label_description = tk.Label(text='Please select one option:', bg=color_background_2)
        self.label_description.grid(row=1, column=0)
        self.button_to_cfg = tk.Button(text='Convert excel to cfg', bg=color_background_2)
        self.button_to_cfg.grid(row=2, column=0)
        self.button_to_excel = tk.Button(text='Convert cfg to excel', bg=color_background_2)
        self.button_to_excel.grid(row=3, column=0)

        # self.label1 = tk.Label(master=self.frame, text="I'm at (0, 0)", bg="red")
        # self.label1.place(x=0, y=0d)
        # self.label2 = tk.Label(master=self.frame, text="I'm at (75, 75)", bg="yellow")
        # self.label2.place(x=75, y=75)

        for row_num in range(self.window.grid_size()[1]):
            self.window.rowconfigure(row_num, weight=1, minsize=100)
        for col_num in range(self.window.grid_size()[0]):
            self.window.columnconfigure(col_num, weight=1, minsize=100)

        self.window.mainloop()


if __name__ == '__main__':
    app = TkAppInterface()