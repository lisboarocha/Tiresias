import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText

from mod.factiva import ParseHtm
import csv


class ViewFactiva():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="htm from Factiva to Prospero",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame 1
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)

        bn_csv = tk.Button(Fr1, text="Select a htm file",
            command=self.sel_file)
        bn_csv.pack(side=tk.RIGHT)

        self.choosen_file = tk.StringVar()
        csv_entry = tk.Entry(Fr1, width=52,
                             textvariable=self.choosen_file)
        csv_entry.pack()
        self.choosen_files = []
        
        #Frame 2
        Fr2 = tk.Frame(self.parent)
        Fr2.pack(anchor=tk.W)
        bnDir = tk.Button(Fr2, text="Select directory for Prospero Files",
            command=self.sel_dir)
        bnDir.pack(side=tk.RIGHT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(Fr2, width=52,
            textvariable=self.choosenDir)
        dir_entry.pack()

        #Frame 3
        Fr3 = tk.Frame(self.parent)
        Fr3.pack(anchor=tk.W)
        self.CleaningVal= tk.BooleanVar()
        Bn_Cleaning = tk.Checkbutton(Fr3,
                        text="clean texts",
                        variable=self.CleaningVal)
        Bn_Cleaning.select()
        Bn_Cleaning.pack(side=tk.LEFT)
        bn_process = tk.Button(Fr3, text="Process", command=self.process)
        bn_process.pack(side=tk.LEFT)

        #Frame 4
        Fr4 = tk.Frame(self.parent)
        Fr4.pack()
        self.log = ScrolledText(Fr4, height=10, bg="black", fg="orange")
        self.log.pack()

    def sel_file(self):
        self.choosen_file.set("")
        filename = fd.askopenfilenames(title = "Select htm file",
                                      filetypes =[("htm Files", "*.htm *.html"),])
        
        self.choosen_file.set(filename)
        self.choosen_files = filename
        
    def sel_dir(self):
        self.choosenDir.set("")
        dir = fd.askdirectory(title="Choose directory")
        self.choosenDir.set(dir)

    def process(self):
        filenames = self.choosen_files
        rows = []
        path = ""
        for file in filenames:
            filename = str(file)
            if filename:
                save_dir = self.choosenDir.get()
                if not save_dir:
                    save_dir = os.getcwd()
                self.log.insert(1.0, "Processing %s to %s\n"%(filename, save_dir))
                self.parent.update()
                parse = ParseHtm(filename)
                self.log.insert(1.0,
                                "%s: found %d article(s)\n"%(filename,
                                                        len(parse.content)))
                parse.get_supports("data/support.publi")
                self.log.insert(1.0, 
                                "%d unknown(s) source(s)\n" %len(parse.unknowns))
                for unknown in parse.unknowns:
                    self.log.insert(1.0, "unknown: %s\n" % unknown)
                parse.write_prospero_files(save_dir, self.CleaningVal.get())
                for row in parse.get_rows():
                    rows.append(row)
                path = parse.get_path_csv()
            else:
                self.log.insert(1.0, "Missing file to process\n")
        if rows:
            chaves = ["CLM", "SE", "HD", "BY", "CR", "WC", "PD", "SN", "SC", "ED", "PG", "LA", "CY", "LP", "TD", "ART", "CO", "IN", "NS", "RE", "IPC", "IPD", "PUB", "AN"]
        
            #criando o csv
            #escrever csv com valores onde a chave estiver em chaves
            try:
                with open(path, 'w', encoding="Windows-1252", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(chaves)
                    for row in rows:
                        writer.writerow(row)
            except:
                try:
                    with open(path, 'w', encoding="latin1", newline="") as csvfile:
                        writer = csv.writer(csvfile, delimiter=';', quotechar='"',
                                            quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(chaves)
                        for row in rows:
                            writer.writerow(row)
                except:
                    with open(path, 'w', encoding="utf8", newline="") as csvfile:
                        writer = csv.writer(csvfile, delimiter=';', quotechar='"',
                                            quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(chaves)
                        for row in rows:
                            writer.writerow(row)

        
