import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
from tkinter.scrolledtext import ScrolledText
from options import Options
import os
import generator
import parse


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.resizable(self, width=False, height=False)
        tk.Tk.wm_title(self, " PDF Generator")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = tk.Menu(container)
        tk.Tk.config(self, menu=menu)
        menu.add_cascade(label="Generator",
                         command=lambda: self.show_frame(Dashy))
        menu.add_cascade(label="Settings",
                         command=lambda: self.show_frame(Settings))

        self.frames = {}
        for F in (Dashy, Settings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(Dashy)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Dashy(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#202020")

        self.status_bar = tk.StringVar(value="Welcome to PDF Generator")
        # self.status_bar.set("Last ticket generated: N/A")

        self.notepad = ScrolledText(self, width=75, height=18, bg="#0c0c0c",
                                    fg="#F8F8F2", insertbackground="white",
                                    insertofftime=800, insertwidth=1, padx=2,
                                    font="Arial 12")
        self.notepad.pack()

        status = ttk.Label(self, textvariable=self.status_bar,
                           foreground="white", relief=tk.FLAT, anchor=tk.W,
                           background='#353535')
        status.pack(side=tk.BOTTOM, fill=tk.X)

        delete = tk.Button(self, text="Delete", height=1, width=8,
                           font=aux.big_font, activebackground="#b88ab8",
                           bg="#c29ac2", relief=tk.GROOVE, command=self.delete)
        delete.pack(side=tk.LEFT, padx=(5, 0))

        generate = tk.Button(self, text="Generate", height=1, width=8,
                             font=aux.big_font, activebackground="#5e955f",
                             bg="#7eaa7e", relief=tk.GROOVE,
                             command=lambda: self.generate())
        generate.pack(side=tk.RIGHT, padx=(0, 5))

    def generate(self):
        text = self.notepad.get("1.0", "end-1c")
        self.notepad.delete("1.0", "end")
        d = parse.Parser(text)
        data = d.build_data()
        generator.single_form_fill(aux.project_dir + r"\templates\example.pdf",
                                   data, aux.cache["Settings"][
                                       "output_path"] + r"\testfile.pdf",
                                   aux.cache["Settings"][
                                       "open_after_generation"])

    def delete(self):
        self.notepad.delete("1.0", "end")

    def status_update(self, noun, verb):
        status_message = "Last Activity: " + noun + verb
        self.var3.set(status_message)


class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#202020")
        output_label = ttk.Label(self, font=aux.big_font, background="#202020",
                                 foreground="#FFFFFF", text="Output "
                                                            "directory:")
        output_label.place(x=1, y=3)

        photo = PhotoImage(file=os.path.join(aux.project_dir,
                                             "images/folder1.png"))
        change_folder = tk.Button(self, image=photo, height=28, width=28,
                                  command=self.browse_directories)
        change_folder.image = photo
        change_folder.place(x=3, y=40)
        self.directory_label = tk.StringVar(value=aux.cache["Settings"][
            "output_path"])
        path_entry = ttk.Entry(self, width=40, font=("Calibri", 17),
                               textvariable=self.directory_label)

        path_entry["state"] = "disabled"
        path_entry.place(x=37, y=40)

    def browse_directories(self):
        path_prompt = tk.filedialog.askdirectory(
            title="Choose a new output folder!")
        if path_prompt != "":
            aux.set_settings("Settings", "output_path", path_prompt)
            self.directory_label.set(path_prompt)


class Popup(tk.Toplevel):
    def __init__(self, parent, message):
        tk.Toplevel.__init__(self, parent, bg="#1f1f36")
        tk.Tk.resizable(self, width=False, height=False)
        self.wm_title("Error")
        x = app.winfo_x() + 90
        y = app.winfo_y() + 100
        tk.Tk.geometry(self, '350x100+{}+{}'.format(x, y))
        lbl = ttk.Label(self, text="  " + message,
                        font=aux.regular_font, background="#1f1f36",
                        foreground="#AACCFF")
        lbl.pack(side="top", fill="x", pady=10, padx=10)
        btn = ttk.Button(self, text="OK", command=self.destroy)
        btn.pack(pady=10)
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)


aux = Options()
app = App()
screen_width = int(app.winfo_screenwidth() / 3)
screen_height = int(app.winfo_screenheight() / 5)
app.geometry("533x400+{}+{}".format(screen_width, screen_height))
app.mainloop()
