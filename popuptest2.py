import Tkinter as tk
import tkFileDialog

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.button = tk.Button(text="Pick a file!", command=self.pick_file)
        self.button.pack()
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(side="top", fill="both", expand=True)
        self.entry_frame.grid_columnconfigure(0, weight=1)

    def pick_file(self):
        file = tkFileDialog.askopenfile(title="pick a file!")
        if file is not None:
            entry = tk.Entry(self)
            entry.insert(0, file.name)
            entry.grid(in_=self.entry_frame, sticky="ew")
            self.button.configure(text="Pick another file!")

app = SampleApp()
app.mainloop()
