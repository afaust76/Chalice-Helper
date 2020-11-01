from tkinter import Frame, Scrollbar, Listbox, END, Tk, Label, StringVar, \
Entry, OptionMenu, Button, messagebox, Checkbutton, IntVar
from os import getcwd

paramcodes = {"id":0,"protocol":1,"datasource":2,"Test Type":3,
    "Biobook Notebook Experiment ID":4,"Cell Line":5,"Cell Line Background":6,
    "Cancer Type":7,"Assay Start":8,"Assay Length":9,"Assay Endpoint":10,
    "Screen Name":11,"Experimenter":12,"Cell Density":13,"Plate Format":14,
    "Compound-D":15,"Compound-A":16,"Compound-A Designation":17,
    "Compound-A Name":18,"Compound-D Designation":19,"Compound-D Name":20}


# GUI manages the user interface of Chalice Helper
class GUI:
    # The GUI takes in the Directory object in order to access data
    def __init__(self, direc):
        # file is the current file being viewed in the interface
        self.file = -1
        self.filepos = -1
        self.main = Tk()
        self.main.geometry("955x565")

        # Creates a display denoting the current directory or current file
        path = StringVar()
        pathlabel = Label(self.main, textvariable=path, relief="raised")
        path.set(getcwd())
        pathlabel.place(x=0, y=0)

        # Creates checkboxes to control parameter display
        paramnames = {0:"id",1:"protocol",2:"datasource",3:"Test Type",
        4:"Biobook Notebook Experiment ID",5:"Cell Line",
        6:"Cell Line Background",7:"Cancer Type",8:"Assay Start",
        9:"Assay Length",10:"Assay Endpoint",11:"Screen Name",
        12:"Experimenter",13:"Cell Density",14:"Plate Format",15:"Compound-D",
        16:"Compound-A",17:"Compound-A Designation",18:"Compound-A Name",
        19:"Compound-D Designation",20:"Compound-D Name"}
        checkframe = Frame(self.main)
        checkframe.place(x=740, y=20)
        checkvars = []
        checkbuttons = []
        for i in range(21):
            checkvars.append(IntVar())
            checkbuttons.append(Checkbutton(checkframe, text=paramnames[i],
                                            pady=0, variable=checkvars[i]))
            checkbuttons[i].grid(row=i, column=0, sticky="W")
        for c in checkbuttons:
            c.select()

        # Creates a display for the Chalice files in the directory
        fileframe = Frame(self.main)
        fileframe.place(x=10, y=25)
        filescroll = Scrollbar(fileframe)
        filescroll.pack(side="right", fill="y")
        filelist = Listbox(fileframe, yscrollcommand=filescroll.set,
                           height=30, width=40)
        filelist.pack(side="left", fill="both")
        for f in direc.files:
           filelist.insert(END, f.name)
        filescroll.config(command=filelist.yview)

        # Creates a display for the entries in the selected file
        entryframe = Frame(self.main)
        entryframe.place(x=290, y=25)
        entryscroll = Scrollbar(entryframe)
        entryscroll.pack(side="right", fill="y")
        entrylist = Listbox(entryframe, yscrollcommand=entryscroll.set,
                            height=30, selectmode="extended", width=3)
        entrylist.pack(side="left", fill="both")
        entryscroll.config(command=entrylist.yview)

        # Creates a display for the parameter values of the selected entries
        paramframe = Frame(self.main)
        paramframe.place(x=350, y=25)
        paramscroll = Scrollbar(paramframe, orient="horizontal")
        paramscroll.pack(side="bottom", fill="x")
        paramlist = Listbox(paramframe, height=22, width=60,
                            xscrollcommand=paramscroll.set)
        paramlist.pack(side="top", fill="both")
        paramscroll.config(command=paramlist.xview)

        def printparams():
            paramlist.delete(0,END)
            if(self.file != -1):
                summary = self.file.summarylist()
                temp = 0
                for i in range(17):
                    if(checkvars[i].get() == 1):
                        paramlist.insert(END,summary[i] + " ")
                        temp = 1
                if(temp == 1):
                    paramlist.insert(END, "")
                for i in range(17, 21):
                    if(checkvars[i].get() == 1):
                        paramlist.insert(END, summary[i + 1] + " ")

        for c in checkbuttons:
            c.config(command=printparams)

        def selectall():
            for c in checkbuttons:
                c.select()
            printparams()

        def selectnone():
            for c in checkbuttons:
                c.deselect()
            printparams()

        allbutton = Button(self.main, text="All", command=selectall)
        allbutton.place(x=750, y=525)
        nonebutton = Button(self.main, text="None", command=selectnone)
        nonebutton.place(x=800, y=525)

        # Creates the interface for the search function
        searchval = StringVar()
        mainsearch = Frame(self.main)
        mainsearch.place(x=350, y=400)
        searchinput = Frame(mainsearch)
        searchinput.pack(side="top", fill="x")
        searchsetting = Frame(mainsearch)
        searchsetting.pack(side="bottom", fill="x")
        searchentry = Entry(searchinput, textvariable=searchval, width=49)
        searchentry.pack(side="left")
        searchentries = StringVar()
        searchentries.set("All entries")
        searchparams = StringVar()
        searchparams.set("protocol")
        entrychoices = ["All entries","Selected entries"]
        paramchoices = ["protocol","datasource","Test Type",
        "Biobook Notebook Experiment ID","Cell Line","Cell Line Background",
        "Cancer Type","Assay Start","Assay Length","Assay Endpoint",
        "Screen Name","Experimenter","Cell Density","Plate Format",
        "Compound-D","Compound-A","Compound-A Name","Compound-D Name"]
        searchentrymenu = OptionMenu(searchsetting, searchentries,
                                     *entrychoices)
        searchentrymenu.pack(side="left")
        searchparammenu = OptionMenu(searchsetting, searchparams,
                                     *paramchoices)
        searchparammenu.pack(side="left")

        def search():
            if(self.file != -1):
                param = paramcodes[searchparams.get()]
                if(searchentries.get() == "All entries"):
                    self.file.selected = []
                    self.file.search(param, searchval.get())
                else:
                    self.file.searchselected(param, searchval.get())
                self.file.reset_summary()
                printparams()
                searchentry.delete(0, END)
                if(len(self.file.selected) == 0):
                    messagebox.showinfo("Search results", "No entries found")

        searchbutton = Button(searchinput, text="Search", command=search)
        searchbutton.pack(side="right")

        # Creates the interface for the edit function
        editval = StringVar()
        mainedit = Frame(self.main)
        mainedit.place(x=350, y=460)
        editinput = Frame(mainedit)
        editinput.pack(side="top", fill="x")
        editsetting = Frame(mainedit)
        editsetting.pack(side="bottom", fill="x")
        editentry = Entry(editinput, textvariable=editval, width=51)
        editentry.pack(side="left")
        editentries = StringVar()
        editentries.set("Selected entries")
        editparams = StringVar()
        editparams.set("protocol")
        editentrymenu = OptionMenu(editsetting, editentries, *entrychoices)
        editentrymenu.pack(side="left")
        editparammenu = OptionMenu(editsetting, editparams, *paramchoices)
        editparammenu.pack(side="left")

        def edit():
            if((self.file != -1) & (editval.get() != "")):
                param = paramcodes[editparams.get()]
                if(editentries.get() == "All entries"):
                    self.file.selected = list(range(self.file.numentries))
                self.file.update_range(param, editval.get())
                self.file.reset_summary()
                printparams()
                editentry.delete(0, END)

        editbutton = Button(editinput, command=edit, text="Edit")
        editbutton.pack(side="right")

        # Creates a button to export the entry summary to a file
        def export():
            if(self.file != -1):
                if(len(self.file.selected) != 0):
                    selparams = []
                    for v in checkvars:
                        selparams.append(v.get())
                    self.file.export(selparams)
                    messagebox.showinfo("Export", "Export successful")

        exportbutton = Button(self.main, text="Export", command=export)
        exportbutton.place(x=350, y=525)

        # Creates a button to export the entry summary for all files
        def exportall():
            direc.export()
            messagebox.showinfo("Export", "Export successful")

        exportallbutton = Button(self.main, text="Export All",
                                 command=exportall)
        exportallbutton.place(x=400, y=525)

        # Creates a button to select a file to view
        def fileselect():
            selected = filelist.curselection()
            if(len(selected) != 0):
                self.file = direc.files[selected[0]]
                self.filepos = selected[0]
                path.set(getcwd() + "\\" + self.file.name)
                entrylist.delete(0, END)
                for i in range(self.file.numentries):
                    entrylist.insert(END, str(i + 1))
                self.file.selected = []
                self.file.reset_summary()
                paramlist.delete(0, END)

        fileselectbutton = Button(self.main, text="Select", command=fileselect)
        fileselectbutton.place(x=110, y=525)

        # Creates a button to select the next file
        def nextfile():
            if((self.filepos != -1) & (self.filepos != filelist.size() - 1)):
                self.filepos += 1
                self.file = direc.files[self.filepos]
                path.set(getcwd() + "\\" + self.file.name)
                entrylist.delete(0, END)
                for i in range(self.file.numentries):
                    entrylist.insert(END, str(i + 1))
                self.file.selected = []
                self.file.reset_summary()
                paramlist.delete(0, END)

        downbutton = Button(self.main, text=">>", relief="raised",
                            command=nextfile)
        downbutton.place(x=160, y=525)

        # Creates a button to select the previous file
        def prevfile():
            if((self.filepos != -1) & (self.filepos != 0)):
                self.filepos -= 1
                self.file = direc.files[self.filepos]
                path.set(getcwd() + "\\" + self.file.name)
                entrylist.delete(0, END)
                for i in range(self.file.numentries):
                    entrylist.insert(END, str(i + 1))
                self.file.selected = []
                self.file.reset_summary()
                paramlist.delete(0, END)

        upbutton = Button(self.main, text="<<", relief="raised",
                          command=prevfile)
        upbutton.place(x=75, y=525)

        # Creates a button to select entries to view
        def entryselect():
            selected = entrylist.curselection()
            if(len(selected) != 0):
                self.file.selected = list(selected)
                self.file.reset_summary()
                printparams()

        entryselectbutton = Button(self.main, text="Select",
                                   command=entryselect)
        entryselectbutton.place(x=285, y=525)

        # Launches interface
        self.main.mainloop()