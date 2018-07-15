#! python

''' This utility check whether a combination is a winner or not based on data file provided or the latest data available
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

import dataDownload as dataD

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # initialize fields

        self.origin = os.getcwd()
        self.exactMatch = False
        self.source = ""
        self.allSet = True

        # this variable will be checked for the game type
        self.gameType = IntVar()

        # this variable will be checked for the data to use, either the file selected or the current data from CALottery
        self.useData = IntVar()

        # these variables will determine the number of matches to look for
        self.getMatch3 = IntVar()
        self.getMatch4 = IntVar()
        self.getMatch5 = IntVar()

        # this variable will determine if the mega number is going to be check. Not used for Fantasy 5
        self.getMatchM = IntVar()

        # these variables are used for the numbers that will be checked
        self.numberA = StringVar()
        self.numberB = StringVar()
        self.numberC = StringVar()
        self.numberD = StringVar()
        self.numberE = StringVar()
        self.numberM = StringVar()

        # create the main tkinter frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # set label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white")
        Style().configure("MS.TLabel", font="Verdana 10")
        Style().configure("S.TLabel", font="Verdana 8")
        Style().configure("G.TLabel", font="Verdana 8")

        # set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")

        # set radio button styles
        Style().configure("B.TRadiobutton", font="Verdana 8")

        # set list box style
        Style().configure("L.TListbox", font="Verdana 8")

        # set entry box style
        Style().configure("E.TEntrybox", font="Verdana 8", anchor="center")

        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        self.parentTab = Notebook(self.main_container)
        self.optionsTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.resultsTab = Frame(self.parentTab)   # second page
        self.parentTab.add(self.optionsTab, text=' Options ')
        self.parentTab.add(self.resultsTab, text=' Results ')

        # main labels
        self.mainLabel = Label(self.main_container, text="WINNER CHECKER", style="M.TLabel")
        self.subLabelA = Label(self.main_container, text="Check if a number combination is a winner. Select the game played", style="S.TLabel")
        self.subLabelB = Label(self.main_container, text="and a data file to check against, or get the latest data file", style="S.TLabel")
        self.subLabelC = Label(self.main_container, text="from CALottery. You also have the option to check for three or", style="S.TLabel")
        self.subLabelD = Label(self.main_container, text="four matches, or the Mega number only.", style="S.TLabel")

        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)

        # create widgets for the options tab
        self.o_sep_a = Separator(self.optionsTab, orient=HORIZONTAL)
        self.o_sep_b = Separator(self.optionsTab, orient=HORIZONTAL)
        self.o_sep_c = Separator(self.optionsTab, orient=HORIZONTAL)
        self.o_sep_d = Separator(self.optionsTab, orient=HORIZONTAL)
        self.o_sep_e = Separator(self.optionsTab, orient=HORIZONTAL)
        self.o_sep_f = Separator(self.optionsTab, orient=HORIZONTAL)
        self.o_sep_g = Separator(self.optionsTab, orient=HORIZONTAL)

        self.gameSelection = LabelFrame(self.optionsTab, text=" Game", style="O.TLabelframe")
        self.gameA = Radiobutton(self.gameSelection, text="Fantasy", style="B.TRadiobutton", variable=self.gameType, value=1)
        self.gameB = Radiobutton(self.gameSelection, text="Super", style="B.TRadiobutton", variable=self.gameType, value=2)
        self.gameC = Radiobutton(self.gameSelection, text="Unused", style="B.TRadiobutton", variable=self.gameType, value=3)
        self.gameD = Radiobutton(self.gameSelection, text="Unused", style="B.TRadiobutton", variable=self.gameType, value=4)

        self.numberEntry = LabelFrame(self.optionsTab, text=" Combination", style="O.TLabelframe")
        self.tagA = Label(self.numberEntry, text="A", style="G.TLabel")
        self.tagB = Label(self.numberEntry, text="B", style="G.TLabel")
        self.tagC = Label(self.numberEntry, text="C", style="G.TLabel")
        self.tagD = Label(self.numberEntry, text="D", style="G.TLabel")
        self.tagE = Label(self.numberEntry, text="E", style="G.TLabel")
        self.tagM = Label(self.numberEntry, text="Mega", style="G.TLabel")
        self.numA = Entry(self.numberEntry, textvariable=self.numberA, width="6")
        self.numB = Entry(self.numberEntry, textvariable=self.numberB, width="6")
        self.numC = Entry(self.numberEntry, textvariable=self.numberC, width="6")
        self.numD = Entry(self.numberEntry, textvariable=self.numberD, width="6")
        self.numE = Entry(self.numberEntry, textvariable=self.numberE, width="6")
        self.numM = Entry(self.numberEntry, textvariable=self.numberM, width="6")

        self.matchFilter = LabelFrame(self.optionsTab, text=" Match Options", style="O.TLabelframe")
        self.match3 = Checkbutton(self.matchFilter, text="Match 3", style="B.TCheckbutton", variable=self.getMatch3)
        self.match4 = Checkbutton(self.matchFilter, text="Match 4", style="B.TCheckbutton", variable=self.getMatch4)
        self.match5 = Checkbutton(self.matchFilter, text="Match 5", style="B.TCheckbutton", variable=self.getMatch5)
        self.matchM = Checkbutton(self.matchFilter, text="Mega", style="B.TCheckbutton", variable=self.getMatchM)

        self.dataOptions = LabelFrame(self.optionsTab, text=" Data ", style="O.TLabelframe")
        self.dataLabel = Label(self.dataOptions, text="None", style="B.TLabel", width="52")
        self.getDataFile = Button(self.dataOptions, text="USE FILE", style="B.TButton", command=self.selectData)
        self.downloadData = Button(self.dataOptions, text="DOWNLOAD", style="B.TButton", command=self.downloadData)

        # create widgets for resetting and exiting
        self.reset = Button(self.optionsTab, style="B.TButton", text="RESET", command=self.resetOptions)
        self.check = Button(self.optionsTab, style="B.TButton", text="CHECK", command=self.startProcess)

        # create widgets for the results tab
        self.scroller = Scrollbar(self.resultsTab, orient=VERTICAL)
        self.dataSelect = Listbox(self.resultsTab, yscrollcommand=self.scroller.set, width="57", height="20")

        # create widget to exit application
        self.exit = Button(self.main_container, style="B.TButton", text="EXIT", command=self.checkExit)

        # position widgets in the options tab
        self.gameA.grid(row=0, column=0, padx=15, pady=(5, 10), sticky='W')
        self.gameB.grid(row=0, column=1, padx=15, pady=(5, 10), sticky='W')
        self.gameC.grid(row=0, column=2, padx=15, pady=(5, 10), sticky='W')
        self.gameD.grid(row=0, column=3, padx=15, pady=(5, 10), sticky='W')
        self.gameSelection.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.o_sep_a.grid(row=1, column=0, columnspan=2, padx=5, pady=1, sticky='NSEW')

        self.tagA.grid(row=0, column=0, padx=10, pady=(5,0), sticky='W')
        self.tagB.grid(row=0, column=1, padx=10, pady=(5,0), sticky='W')
        self.tagC.grid(row=0, column=2, padx=10, pady=(5,0), sticky='W')
        self.tagD.grid(row=0, column=3, padx=10, pady=(5,0), sticky='W')
        self.tagE.grid(row=0, column=4, padx=10, pady=(5,0), sticky='W')
        self.tagM.grid(row=0, column=5, padx=10, pady=(5,0), sticky='W')
        self.numA.grid(row=1, column=0, padx=10, pady=(2,10), sticky='W')
        self.numB.grid(row=1, column=1, padx=10, pady=(2,10), sticky='W')
        self.numC.grid(row=1, column=2, padx=10, pady=(2,10), sticky='W')
        self.numD.grid(row=1, column=3, padx=10, pady=(2,10), sticky='W')
        self.numE.grid(row=1, column=4, padx=10, pady=(2,10), sticky='W')
        self.numM.grid(row=1, column=5, padx=10, pady=(2,10), sticky='W')
        self.numberEntry.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.o_sep_b.grid(row=3, column=0, columnspan=2, padx=5, pady=1, sticky='NSEW')

        self.match3.grid(row=0, column=0, padx=15, pady=(5, 10), sticky='W')
        self.match4.grid(row=0, column=1, padx=15, pady=(5, 10), sticky='W')
        self.match5.grid(row=0, column=2, padx=15, pady=(5, 10), sticky='W')
        self.matchM.grid(row=0, column=3, padx=15, pady=(5, 10), sticky='W')
        self.matchFilter.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.o_sep_c.grid(row=5, column=0, columnspan=2, padx=5, pady=1, sticky='NSEW')

        self.dataLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.getDataFile.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.downloadData.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.dataOptions.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.o_sep_d.grid(row=7, column=0, columnspan=2, padx=5, pady=1, sticky='NSEW')

        self.check.grid(row=8, column=0, padx=5, pady=5, sticky='NSEW')
        self.reset.grid(row=8, column=1, padx=5, pady=5, sticky='NSEW')

        # position widgets in the results tab
        self.dataSelect.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky='NSEW')
        self.scroller.grid(row=0, column=2, columnspan=1, padx=5, pady=10, sticky= 'NSEW')

        # position the widgets in the main container
        self.mainLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.subLabelD.grid(row=4, column=0, columnspan=2, padx=5, pady=(0,5), sticky='NSEW')

        self.sep_a.grid(row=5, column=0, columnspan=2, padx=5, pady=1, sticky='NSEW')

        self.parentTab.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.sep_b.grid(row=7, column=0, columnspan=2, padx=5, pady=1, sticky='NSEW')

        self.exit.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.getMatch3.set(0)
        self.getMatch4.set(0)
        self.getMatch5.set(0)
        self.getMatchM.set(0)

        # set fantasy five as the defaults game
        self.gameType.set(1)

    def displaySource(self):
        pass

    def selectData(self):

        ''' This function will select a data file and check if it is a Fantasy Five file
        '''

        filename = askopenfilename()

        if os.path.isfile(filename):

            datafile = open(filename)

            # Read the first record on file
            d_line = datafile.readline()
            d_list = d_line.split()

            datafile.close()

            if self.gameType.get() == 1:
                if "FANTASY" in d_list:

                    self.source = filename
                    self.dataLabel["text"] = os.path.dirname(filename)[:15] + ".../" + os.path.basename(filename)

                else:
                    self.showFileError("FANTASY 5")

            elif self.gameType.get() == 2:

                if "SUPERLOTTO" in d_list:

                    self.source = filename
                    self.dataLabel["text"] = os.path.dirname(filename)[:15] + ".../" + os.path.basename(filename)

                else:
                    self.showFileError("SUPERLOTTO")
            else:

                self.source = ""
                self.dataLabel["text"] = 'None'

    def showFileError(self, source):

        ''' This function will show the error on the selected file
        '''
        messagebox.showerror("File Error", "File selected is not a valid " + source + " data file.")
        self.dataLabel["text"] = 'None'


    def downloadData(self):

        if self.gameType.get() == 1:
            baseUrl = 'http://www.calottery.com/play/draw-games/fantasy-5/winning-numbers'
            saveName = 'FantasyFive.txt'
        elif self.gameType.get() == 2:
            baseUrl = 'http://www.calottery.com/play/draw-games/superlotto-plus/winning-numbers'
            saveName = 'SuperLottoPlus.txt'
        else:
            messagebox.showerror("Download Error", "Download not available for game selected.")
            return

        dataD.dataDownload(baseUrl, saveName)

        self.source = saveName
        self.dataLabel["text"] = saveName

        messagebox.showinfo("Download complete", "The latest data file for the selected game hase been downloaded.")

    def resetOptions(self):
        ''' This function will reset the fields used in the application.
        '''

        response = messagebox.askquestion("Reset Process", "Reset process will require selection of new data file. Continue?")

        if response == 'no':
            return

        self.dataSelect.delete(0, END)

        os.chdir(self.origin)
        self.dataLabel["text"] = "None"
        self.getMatch3.set(0)
        self.getMatch4.set(0)
        self.getMatch5.set(0)
        self.getMatchM.set(0)
        self.source = ""

        self.numberA.set("")
        self.numberB.set("")
        self.numberC.set("")
        self.numberD.set("")
        self.numberE.set("")
        self.numberM.set("")

    def startProcess(self):

        self.checkOptions()

        if self.allSet:

            self.checkForMatches()

            if self.exactMatch == True:
                messagebox.showinfo("Exact Match", "An exact combination match was found.")

            self.parentTab.select(1)

    def checkOptions(self):

        ''' This function will check if all options have been set
        '''

        self.allSet = True

        if self.source == "":
            messagebox.showerror("File Error", "Source file not yet selected.")
            self.allSet = False
            return

        if self.getMatch3.get() == 0 and self.getMatch4.get() == 0 and self.getMatch5.get() == 0:

            self.getMatch3.set(1)
            self.getMatch4.set(1)
            self.getMatch5.set(1)

            if self.gameType.get() == 1:
                self.getMatchM.set(0)
            elif self.gameType.get() == 2:
                self.getMatchM.set(1)

    def checkForMatches(self):

        ''' This function will disable the buttons while it checks for matches, and enable them when done
        '''
        # disable all buttons and check boxes

        self.check["state"] = DISABLED
        self.reset["state"] = DISABLED
        self.exit["state"] = DISABLED

        self.readDataFile()

        self.check["state"] = NORMAL
        self.reset["state"] = NORMAL
        self.exit["state"] = NORMAL

    def readDataFile(self):

        ''' This function will check for close matches to the numbers entered
        '''

        # Set indicator for finding exact match to False
        self.exactMatch = False

        # delete the contents of the list
        self.dataSelect.delete(0, END)

        search_set = [int(self.numberA.get()), int(self.numberB.get()), int(self.numberC.get()), int(self.numberD.get()), int(self.numberE.get())]

        if self.gameType.get() == 2:
            search_mega = int(self.numberM.get())

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

                    match_ctr = 0
                    mega_ctr = 0

                    for i in range(5, 10):
                        winner.append(int(d_list[i]))

                    if self.gameType.get() == 2:
                        winner_mega = int(d_list[10])

                        if winner_mega == search_mega:
                            mega_ctr = 1

                    for w in winner:
                        for s in search_set:
                            if s == w:
                                match_ctr += 1

                    if match_ctr == 3 and self.getMatch3.get() == 1:
                        self.formatOutput(d_line, match_ctr, mega_ctr)

                    elif match_ctr == 4 and self.getMatch4.get() == 1:
                        self.formatOutput(d_line, match_ctr, mega_ctr)

                    elif match_ctr == 5 and self.getMatch5.get() == 1:
                        self.exactMatch = True
                        self.formatOutput(d_line, match_ctr, mega_ctr)

                    if self.gameType.get() == 2:
                        if search_mega == winner_mega and self.getMatchM.get() == 1:
                            self.formatOutput(d_line, match_ctr, mega_ctr)

        dataFile.close()

        self.scroller.config(command=self.dataSelect.yview)


    def formatOutput(self, data_line, match_ctr, mega_ctr=0):

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

        if self.gameType.get() == 2:
            winner_data.append('{:02d}'.format(int(data_list[10])))
            winner_data.append(str(mega_ctr))

        format_data_line = "  |  ".join(winner_data)

        self.dataSelect.insert(END, format_data_line)

    def checkExit(self):
        ''' This function will first check if the results list is empty. If it is, it will exit the application, otherwise it will
            ask the user before it exits the application
        '''
        if self.dataSelect.size() == 0:
            root.destroy()
        else:
            response = messagebox.askquestion("Exit Application", "Are you sure you want to exit the application?")

            if response == 'yes':
                root.destroy()



root = Tk()
root.title('WINNER CHECKER')

# set size
wh = 540
ww = 410

# set the minimum and maximum sizes. they are the same, so windows are not resizeable
root.minsize(ww, wh)
#root.maxsize(ww, wh)

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate the x and y coordinates
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
