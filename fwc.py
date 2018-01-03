#! python

''' This utility will copy a folder and its contents into a different folder
'''
import tkinter 
from tkinter import *
 
#from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import os
import shutil
import datetime 


from time import time
import subprocess as sp

class Application(Frame):

    def __init__(self, master):
        
        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables
        
        self.origin = os.getcwd()
        self.exactMatch = False
        self.source = ""
        self.allSet = True
        self.getMatch3 = IntVar()
        self.getMatch4 = IntVar()
        self.getMatch5 = IntVar()
        self.numberA = StringVar()
        self.numberB = StringVar()
        self.numberC = StringVar()
        self.numberD = StringVar()
        self.numberE = StringVar()
        
        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="38")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")

        Style().configure("L.TListbox", font="Verdana 8", width="40")
        Style().configure("E.TEntrybox", width="10")

        
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        
        # Create widgets
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="FANTASY FIVE CHECKER", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="Checks a Fantasy Five combination if it is a winner based on a selected text file ", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="downloaded from CALottery.com that contains all prior winners of the game. ", style="S.TLabel" )
        self.subLabelC = Label(self.main_container, text="Winners that match 3 or 4 numbers from the combination entered are also listed.", style="S.TLabel" )

        self.numberEntry = LabelFrame(self.main_container, text=' Combination ', style="O.TLabelframe")
        self.submit = Button(self.numberEntry, text="CHECK", style="B.TButton", width='22', command=self.startProcess)
        self.numA = Entry(self.numberEntry, textvariable=self.numberA, width="6")
        self.numB = Entry(self.numberEntry, textvariable=self.numberB, width="6")
        self.numC = Entry(self.numberEntry, textvariable=self.numberC, width="6")
        self.numD = Entry(self.numberEntry, textvariable=self.numberD, width="6")
        self.numE = Entry(self.numberEntry, textvariable=self.numberE, width="6")

        self.filterOpt = LabelFrame(self.main_container, text=' Filter Options ', style="O.TLabelframe")
        self.match3 = Checkbutton(self.filterOpt, text=' Match 3 Numbers ', style="B.TCheckbutton", variable=self.getMatch3)
        self.match4 = Checkbutton(self.filterOpt, text=' Match 4 Numbers ', style="B.TCheckbutton", variable=self.getMatch4)
        self.match5 = Checkbutton(self.filterOpt, text=' Match 5 Numbers ', style="B.TCheckbutton", variable=self.getMatch5)

        self.dataDisplay = LabelFrame(self.main_container, text=' Winner Matches ', style="O.TLabelframe")
        self.scroller = Scrollbar(self.dataDisplay, orient=VERTICAL)
        self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.scroller.set, width=70)
        
        self.dataOpt = LabelFrame(self.main_container, text=' Data File Options ', style="O.TLabelframe")
        self.dataSource = Button(self.dataOpt, text="SELECT DATA FILE", style="B.TButton", width=22, command=self.setSource)
        self.dataDownload = Button(self.dataOpt, text="DOWNLOAD DATA FILE", style="B.TButton", width=22, command=self.setSource)
        self.dataLabel = Label(self.dataOpt, text="None", style="B.TLabel" )

        self.reset = Button(self.main_container, text="RESET", style="B.TButton", width=30, command=self.resetProcess)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", width=30, command=self.checkExit)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)
        
        # Position widgets        
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_a.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.dataSelect.grid(row=0, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.scroller.grid(row=0, column=2, padx=(10,0), pady=5, sticky='NSEW')
        self.dataDisplay.grid(row=5, column=0, columnspan=3, rowspan=5, padx=5, pady=5, sticky='NSEW')

        self.sep_b.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        
        self.numA.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.numB.grid(row=0, column=0, padx=(65,0), pady=(5, 10), sticky='W')
        self.numC.grid(row=0, column=0, padx=(120,0), pady=(5, 10), sticky='W')
        self.numD.grid(row=0, column=0, padx=(175,0), pady=(5, 10), sticky='W')
        self.numE.grid(row=0, column=0, padx=(230,0), pady=(5, 10), sticky='W')
        self.submit.grid(row=0, column=0, padx=(290,0), pady=(5, 10), sticky='NSEW')
        self.numberEntry.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.match3.grid(row=0, column=0, padx=10, pady=(5, 10), sticky='W')
        self.match4.grid(row=0, column=1, padx=10, pady=(5, 10), sticky='W')
        self.match5.grid(row=0, column=2, padx=10, pady=(5, 10), sticky='W')
        self.filterOpt.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sep_c.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.dataLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='NSEW')
        self.dataSource.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='NSEW')
        self.dataDownload.grid(row=1, column=2, padx=10, pady=(5, 10), sticky='NSEW')
        self.dataOpt.grid(row=14, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sep_d.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.reset.grid(row=16, column=0, padx=(10, 0), pady=5, sticky='W')
        self.exit.grid(row=16, column=0, padx=(245, 0), pady=5, sticky='W')

        self.getMatch3.set(0)
        self.getMatch4.set(0)
        self.getMatch5.set(0)

    def setSource(self):

        ''' This function will select a data file and check if it is a Fantasy Five file
        '''

        filename = askopenfilename()

        if os.path.isfile(filename):

            datafile = open(filename)

            # Read the first record on file
            d_line = datafile.readline()
            d_list = d_line.split()

            datafile.close()
        
            if "FANTASY" in d_list:

                self.source = filename
                self.dataLabel["text"] = os.path.dirname(filename)[:15] + ".../" + os.path.basename(filename)
                
            else:
                messagebox.showerror("File Error", "File selected is not a valid Fantasy Five data file.")
                self.dataLabel["text"] = 'None'

            
    def startProcess(self):

        self.checkOptions()
            
        if self.allSet:

            self.checkForMatches()

            if self.exactMatch == True:
                messagebox.showinfo("Exact Match", "An exact combination match was found.")


    def checkOptions(self):

        self.allSet = True
        
        if self.source == "":
            messagebox.showerror("File Error", "Source file not yet selected.")
            self.allSet = False
            return

        if self.getMatch3.get() == 0 and self.getMatch4.get() == 0 and self.getMatch5.get() == 0:
                        
            self.getMatch3.set(1)
            self.getMatch4.set(1)
            self.getMatch5.set(1)


    def checkForMatches(self):

        self.progress_bar.start()

        # disable all buttons and check boxes

        self.submit["state"] = DISABLED
        self.reset["state"] = DISABLED
        self.exit["state"] = DISABLED

        self.readDataFile()

        self.submit["state"] = NORMAL
        self.reset["state"] = NORMAL
        self.exit["state"] = NORMAL

        self.progress_bar.stop()            
        

    def readDataFile(self):

        ''' This function will check for close matches to the numbers entered
        '''

        # Set indicator for finding exact match to False
        self.exactMatch = False

        # delete the contents of the list 
        self.dataSelect.delete(0, END)

        search_set = [int(self.numberA.get()), int(self.numberB.get()), int(self.numberC.get()), int(self.numberD.get()), int(self.numberE.get())]

        filename = self.source

        dataFile = open(filename, "r")

        while True:
        
            d_line = dataFile.readline()

            if d_line == "":
                break

            d_list = d_line.split()

            if len(d_list) > 0:

                if d_list[0].isdigit():

                    winner = []

                    for i in range(5, 10):
                        winner.append(int(d_list[i]))

                    match_ctr = 0

                    for w in winner:
                        for s in search_set:
                            if s == w:
                                match_ctr += 1

                    if match_ctr == 3 and self.getMatch3.get() == 1:
                        self.formatOutput(d_line, match_ctr)
                    elif match_ctr == 4 and self.getMatch4.get() == 1:
                        self.formatOutput(d_line, match_ctr)
                    elif match_ctr == 5 and self.getMatch5.get() == 1:
                        self.exactMatch = True
                        self.formatOutput(d_line, match_ctr)

        dataFile.close()

        self.scroller.config(command=self.dataSelect.yview)

    def formatOutput(self, data_line, match_ctr):

        data_list = data_line.split()

        winner_data = []

        # Format draw number
        draw_number = '{:06d}'.format(int(data_list[0]))

        winner_data.append(draw_number)

        in_date = data_list[2] + ' ' + data_list[3] + ' ' + data_list[4]
        draw_date = str(datetime.datetime.strptime(in_date, '%b %d, %Y').date())

        winner_data.append(draw_date)

        for i in range(5, 10):
            number = '{:02d}'.format(int(data_list[i]))
            winner_data.append(number)

        winner_data.append(str(match_ctr))

        format_data_line = "     |     ".join(winner_data)

        self.dataSelect.insert(END, format_data_line)


    def resetProcess(self):
        # Launch notepad to show status of last copy request

        response = messagebox.askquestion("Reset Process", "Reset process will require selection of new data file. Continue?")

        if response == 'no':
            return

        self.dataSelect.delete(0, END)

        os.chdir(self.origin)
        self.dataLabel["text"] = "None"
        self.getMatch3.set(0)
        self.getMatch4.set(0)
        self.getMatch5.set(0)
        self.source = ""

        self.numberA.set("")
        self.numberB.set("")
        self.numberC.set("")
        self.numberD.set("")
        self.numberE.set("")

    def checkExit(self):

        response = messagebox.askquestion("Exit Application", "Are you sure you want to exit the application?")

        if response == 'yes':
            root.destroy()



root = Tk()
root.title("FANTASY FIVE CHECKER")

# Set size

wh = 600
ww = 480

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
