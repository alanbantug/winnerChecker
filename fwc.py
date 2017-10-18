#! python3

### This utility will copy a folder and its contents into a different folder
###
import Tkinter
from Tkinter import *

import ttk
from ttk import *

from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

import os
import shutil

from time import time
import subprocess as sp

class Application(Frame):

    def __init__(self, master):
        
        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables
        
        self.origin = os.getcwd()
        self.copied = IntVar()
        self.copying = 0
        self.source = ""
        self.target = ""
        self.script = ""
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
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", background="white", anchor="center")
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
        #self.dataSelect = Listbox(self.dataDisplay)
        
        self.dataOpt = LabelFrame(self.main_container, text=' Data File Options ', style="O.TLabelframe")
        self.dataSource = Button(self.dataOpt, text="DATA FILE", style="B.TButton", width=22, command=self.setSource)
        self.dataLabel = Label(self.dataOpt, text="None", style="B.TLabel" )

        #self.sep_s = Separator(self.sourceTarget, orient=HORIZONTAL)
        #self.sep_t = Separator(self.sourceTarget, orient=HORIZONTAL)
        
        self.statusLabel = Label(self.main_container, text="Select source and target folders", style="G.TLabel")
        self.reset = Button(self.main_container, text="RESET", style="B.TButton", width=30, command=self.resetProcess)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", width=30, command=root.destroy)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)
        
        # Position widgets        
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_a.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.numA.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.numB.grid(row=0, column=0, padx=(65,0), pady=(5, 10), sticky='W')
        self.numC.grid(row=0, column=0, padx=(120,0), pady=(5, 10), sticky='W')
        self.numD.grid(row=0, column=0, padx=(175,0), pady=(5, 10), sticky='W')
        self.numE.grid(row=0, column=0, padx=(230,0), pady=(5, 10), sticky='W')
        self.submit.grid(row=0, column=0, padx=(290,0), pady=(5, 10), sticky='NSEW')
        self.numberEntry.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sep_b.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.dataSelect.grid(row=0, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.scroller.grid(row=0, column=2, padx=(10,0), pady=5, sticky='NSEW')
        self.dataDisplay.grid(row=7, column=0, columnspan=3, rowspan=5, padx=5, pady=5, sticky='NSEW')

        self.dataSource.grid(row=0, column=0, padx=(10, 0), pady=(5, 10), sticky='W')
        self.dataLabel.grid(row=0, column=0, padx=(180,0), pady=(5, 10), sticky='W')
        self.dataOpt.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.match3.grid(row=0, column=0, padx=10, pady=(5, 10), sticky='W')
        self.match4.grid(row=0, column=1, padx=10, pady=(5, 10), sticky='W')
        self.match5.grid(row=0, column=2, padx=10, pady=(5, 10), sticky='W')
        self.filterOpt.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        
        self.sep_c.grid(row=14, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.reset.grid(row=15, column=0, padx=(10, 0), pady=5, sticky='W')
        self.exit.grid(row=15, column=0, padx=(245, 0), pady=5, sticky='W')

        self.sep_d.grid(row=16, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        #self.statusLabel.grid(row=15, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        #self.sep_e.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.progress_bar.grid(row=17, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

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
                self.dataLabel["text"] = 'File selected is not a Fantasy Five file'

            
    def startProcess(self):

        self.checkOptions()
            
        if self.allSet:

            self.processRequest()

    def checkOptions(self):

        self.allSet = True
        
        if self.source == "":
            self.showMessage("Source file not yet selected.")
            self.allSet = False
            return

        if self.getMatch3.get() == 0 and self.getMatch4.get() == 0 and self.getMatch5.get() == 0:
            #self.showMessage("All 3, 4 and 5 matches will be selected.")
            
            self.getMatch3.set(1)
            self.getMatch4.set(1)
            self.getMatch5.set(1)


    def showMessage(self, message):

        self.popConfirm = Toplevel(self.main_container)
        self.popConfirm.title("MESSAGE")

        self.messageText = Label(self.popConfirm, text=message, style="MS.TLabel" )
        self.close = Button(self.popConfirm, text="CLOSE", style="B.TButton", command=self.popConfirm.destroy)
        self.messageSep = Separator(self.popConfirm, orient=HORIZONTAL)

        self.messageText.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.messageSep.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.close.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        pop_wh = 80
        pop_ww = 300

        self.popConfirm.minsize(pop_ww, pop_wh)
        self.popConfirm.maxsize(pop_ww, pop_wh)

        # Position in center screen

        pop_ws = self.popConfirm.winfo_screenwidth() 
        pop_hs = self.popConfirm.winfo_screenheight() 

        # calculate x and y coordinates for the Tk root window
        x = (pop_ws/2) - (pop_ww/2)
        y = (pop_hs/2) - (pop_wh/2)

        self.popConfirm.geometry('%dx%d+%d+%d' % (pop_ww, pop_wh, x, y))


    def processRequest(self):

        import threading

        t = threading.Thread(None, self.checkForMatches, ())
        t.start()


    def checkForMatches(self):

        self.progress_bar.start()
        self.copying = 0

        # disable all buttons and check boxes

        self.submit["state"] = DISABLED
        self.reset["state"] = DISABLED
        self.exit["state"] = DISABLED

        for i in range(5):
            self.dataSelect.insert(END, i)

        self.submit["state"] = NORMAL
        self.reset["state"] = NORMAL
        self.exit["state"] = NORMAL

        self.progress_bar.stop()            
        

    def resetProcess(self):
        # Launch notepad to show status of last copy request

        self.dataSelect.delete(0, END)

        os.chdir(self.origin)
        self.dataLabel["text"] = "None"
        self.getMatch3.set(0)
        self.getMatch4.set(0)
        self.getMatch5.set(0)
        self.source = ""


root = Tk()
root.title("FANTASY FIVE CHECKER")
#root.minsize(480, 380)
#root.maxsize(480, 380)

# Set size

wh = 610
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
