# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # #                                                                                   # # # #
# # # #                    1/2/3-shift scheduling algorithm - phase 2:                    # # # #
# # # #                                                                                   # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                       # # # #
# # # #                                                                                   # # # #
# # # #                             Shifto combo manipulation                             # # # #
# # # #                                                                                   # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                       # # # #
# # # #                                                                                   # # # #
# # # #   Author: Benjamin Bolling                                                        # # # #
# # # #   Affiliation: European Spallation Source ERIC                                    # # # #
# # # #   Lund, Sweden                                                                    # # # #
# # # #   Initialization date: 2020-06-08                                                 # # # #
# # # #   Milestone 1 (phase 1, 0:s and 1:s generated):                     2020-06-29    # # # #
# # # #   Milestone 2 (phase 1 all working, proceeding to phase 2):         2020-07-01    # # # #
# # # #   Milestone 3 (phase 2 all working, initial version ready):         2020-07-03    # # # #
# # # #   Milestone 4 (phase 2 finished, solution finder implemented):      2020-07-03    # # # #
# # # #                                                                                   # # # #
# # # #                                                                                   # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PyQt5.QtWidgets import QApplication,QComboBox,QDialog,QDoubleSpinBox,QFileDialog,QGridLayout,QHeaderView,QInputDialog,QLabel,QMessageBox,QPushButton,QSlider,QSpinBox,QTableWidget,QVBoxLayout
from PyQt5.QtCore import QSize, Qt, QCoreApplication
from csv import writer
import sys, numpy
from json import dump, load
from time import time

class DialogPhase2(QDialog):
    def __init__(self, shifttype, shifts, series, shiftlengths, weeklyresting, parent=None):
        super(DialogPhase2, self).__init__(parent)
        self.setWindowTitle("1o2o3 S-CSV-fcal phase 2")
        if shifttype == 0 and shifts == 0 and series == 0 and shiftlengths == 0:
            self.loadFunction() # For future ...
        else:
            self.shifttype = shifttype
            self.shifts = shifts
            self.series = series
            self.shiftlengths = shiftlengths
            self.weeklyresting = weeklyresting # Length of weekly minimum continuous resting time in hours
            self.initValues()
            self.createLayout()
            self.dailyrestinginputChanged()
            self.updateTable2()
    def initValues(self):
        self.dailyresting = 11      # Length of daily minimum resting time between shifts in hours
        self.shift1 = 0
        self.shift2 = 0
        self.shift3 = 0
        for j in self.series:
            for i in range(len(j)):
                self.shift1 += 1
    def createLayout(self):
        self.layout = QGridLayout(self)
        toplabel1 = QLabel("1-, 2- or 3-Shift CSV File Constructor Algorithm.")
        toplabel2 = QLabel("- - - -  Define the parameters below  - - - -")
        toplabel3 = QLabel("")
        dailyrestingtimelbl = QLabel("Minimum continuous daily resting time [h]: ")
        toplabel1.setAlignment(Qt.AlignCenter)
        toplabel2.setAlignment(Qt.AlignCenter)
        toplabel3.setAlignment(Qt.AlignCenter)
        row = 0
        self.layout.addWidget(toplabel1, row,0,1,7)
        row += 1
        self.layout.addWidget(toplabel2, row,0,1,7)
        row += 1
        self.layout.addWidget(toplabel3, row,0,1,7)
        row += 1
        shiftlengthlbl = QLabel("Shift lengths [h]: ")
        self.layout.addWidget(shiftlengthlbl,row,0,1,4)
        self.shiftlengthinput = QDoubleSpinBox()
        self.shiftlengthinput.setValue(self.shiftlengths)
        self.shiftlengthinput.setMinimum(1)
        self.shiftlengthinput.valueChanged.connect(self.shiftlengthinputChanged)
        self.layout.addWidget(self.shiftlengthinput,row,4,1,3)
        row += 1
        dailyrestingtimelbl = QLabel("Minimum continuous daily resting time [h]: ")
        self.layout.addWidget(dailyrestingtimelbl,row,0,1,4)
        self.checkWeeklyRestBtn = QPushButton("Check Weekly Rest")
        self.dailyrestinginput = QSpinBox()
        self.dailyrestinginput.setValue(self.dailyresting)
        self.dailyrestinginput.setMinimum(1)
        self.dailyrestinginput.setToolTip("Swedish law: 11 hours minimum")
        self.dailyrestinginput.valueChanged.connect(self.dailyrestinginputChanged)
        self.layout.addWidget(self.dailyrestinginput,row,4,1,3)
        row += 1
        weeklyrestingtimelbl = QLabel("Minimum continuous weekly resting time [h]: ")
        self.layout.addWidget(weeklyrestingtimelbl,row,0,1,4)
        self.weeklyrestinginput = QSpinBox()
        self.weeklyrestinginput.setValue(self.weeklyresting)
        self.weeklyrestinginput.setMinimum(1)
        self.weeklyrestinginput.setToolTip("Swedish law: 11 hours minimum")
        self.weeklyrestinginput.valueChanged.connect(self.weeklyrestinginputChanged)
        self.layout.addWidget(self.weeklyrestinginput,row,4,1,3)
        row += 1
        toplabel4 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel4.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(toplabel4, row, 0, 1, 7)
        if self.shifttype > 1:
            row += 1
            self.findSolutionsBtn = QPushButton("Find solutions")
            self.findSolutionsBtn.clicked.connect(self.findSolution)
            self.layout.addWidget(self.findSolutionsBtn, row, 1, 1, 1)
            self.find1SolutionBtn = QPushButton("Find First Solution")
            self.find1SolutionBtn.clicked.connect(self.find1Solution)
            self.layout.addWidget(self.find1SolutionBtn, row, 2, 1, 2)
            self.checkWeeklyRestBtn.clicked.connect(self.checkWeeklyRest)
            self.layout.addWidget(self.checkWeeklyRestBtn, row, 4, 1, 2)

            row += 1
            self.solutionsLbl = QLabel("Solution index: ")
            self.solutionsLbl.setVisible(False)
            self.layout.addWidget(self.solutionsLbl, row, 0, 1, 2)
            self.solutionsBrowsing = QSpinBox()
            self.solutionsBrowsing.valueChanged.connect(self.solutionIntChangedI)
            self.solutionsBrowsing.setVisible(False)
            self.solutionsBrowsing.setKeyboardTracking(False)
            self.layout.addWidget(self.solutionsBrowsing, row, 2, 1, 2)
            self.solutionsSlider = QSlider()
            self.solutionsSlider.setOrientation(Qt.Horizontal)
            self.solutionsSlider.setVisible(False)
            self.solutionsSlider.valueChanged.connect(self.solutionIntChangedS)
            self.solutionsSlider.sliderReleased.connect(self.solutionMatrix2Table1)
            self.layout.addWidget(self.solutionsSlider, row, 4, 1, 3)
            row += 1
            toplabel4b = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            toplabel4b.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(toplabel4b, row, 0, 1, 7)
        row += 1
        tablelayout = QVBoxLayout()
        self.layout.addLayout(tablelayout,row,0,len(self.series),7)
        self.table = QTableWidget() # Create table for the series we work with
        tablelayout.addWidget(self.table)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels("Mon;Tue;Wed;Thu;Fri;Sat;Sun".split(";"))
        for i in range(0,7):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.table.setRowCount(len(self.series))
        for rr, serie in enumerate(self.series):
            for col, value in enumerate(serie):
                if value == 0:
                    wdg = QLabel("0")
                    wdg.setAlignment(Qt.AlignCenter)
                else:
                    wdg = QComboBox()
                    for t in self.shifts:
                        wdg.addItem(t)
                    wdg.currentIndexChanged.connect(self.readTableContents)
                self.table.setCellWidget(rr,col,wdg)
        self.table.setMaximumSize(self.getQTableWidgetSize(self.table))
        self.table.setMinimumSize(self.getQTableWidgetSize(self.table))
        row = row + 1 + len(self.series)
        toplabel5 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel5.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(toplabel5, row, 0, 1, 7)
        row += 1
        self.shifttype1Label = QLabel("Number of "+self.shifts[0]+"-shifts: ")
        self.layout.addWidget(self.shifttype1Label, row, 0, 1, 2)
        self.shiftsof1 = QLabel(str(self.shift1))
        self.layout.addWidget(self.shiftsof1, row, 2, 1, 2)
        if self.shifttype > 1:
            row += 1
            self.shifttype1Label = QLabel("Number of "+self.shifts[1]+"-shifts: ")
            self.layout.addWidget(self.shifttype1Label, row, 0, 1, 2)
            self.shiftsof2 = QLabel(str(self.shift2))
            self.layout.addWidget(self.shiftsof2, row, 2, 1, 2)
        if self.shifttype > 2:
            row += 1
            self.shifttype1Label = QLabel("Number of "+self.shifts[2]+"-shifts: ")
            self.layout.addWidget(self.shifttype1Label, row, 0, 1, 2)
            self.shiftsof3 = QLabel(str(self.shift3))
            self.layout.addWidget(self.shiftsof3, row, 2, 1, 2)
        row += 1
        toplabel6 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel6.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(toplabel6, row, 0, 1, 7)
        row += 1
        toplabel7 = QLabel("Results:")
        toplabel7.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(toplabel7, row, 0, 1, 7)
        row += 1
        toplabel8 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel8.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(toplabel8, row, 0, 1, 7)
        row += 1
        table2layout = QVBoxLayout()
        self.layout.addLayout(table2layout,row,0,3,7)
        self.table2 = QTableWidget() # Create table for the series we work with
        table2layout.addWidget(self.table2)
        self.table2.setColumnCount(7)
        self.table2.setHorizontalHeaderLabels("Mon;Tue;Wed;Thu;Fri;Sat;Sun".split(";"))
        for i in range(0,7):
            self.table2.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.table2.setRowCount(self.shifttype)
        verticalHeaders = []
        for rr in range(self.shifttype):
            for col in range(7):
                wdg = QLabel("0")
                wdg.setAlignment(Qt.AlignCenter)
                self.table2.setCellWidget(rr,col,wdg)
            verticalHeaders.append(self.shifts[rr])
        self.table2.setVerticalHeaderLabels(verticalHeaders)
        self.table2.setMaximumSize(self.getQTableWidgetSize(self.table2))
        self.table2.setMinimumSize(self.getQTableWidgetSize(self.table2))
        row = row + 1 + self.shifttype * 10
        self.loadButton = QPushButton("Load")
        self.loadButton.clicked.connect(self.loadFunction)
        self.layout.addWidget(self.loadButton,row,0,3,2)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveFunction)
        self.layout.addWidget(self.saveButton,row,2,3,2)
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.exportFunction)
        self.exportButton.setToolTip("Export in a CSV format")
        self.layout.addWidget(self.exportButton,row,4,3,3)

        row = row + 1 + self.shifttype * 10
        bottomlabel1 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        bottomlabel2 = QLabel("Coder: Benjamin Bolling (benjaminbolling@icloud.com)")
        self.layout.addWidget(bottomlabel1, row, 0, 1, 7)
        row += 1
        self.layout.addWidget(bottomlabel2, row, 0, 1, 7)
    def shiftlengthinputChanged(self):
        self.shiftlengths = self.shiftlengthinput.value()
        self.readTableContents()
        self.checkWeeklyRestBtn.setStyleSheet("background-color:#DCDCDC;")
    def dailyrestinginputChanged(self):
        self.dailyresting = self.dailyrestinginput.value()
        self.readTableContents()
        self.checkWeeklyRestBtn.setStyleSheet("background-color:#DCDCDC;")
    def weeklyrestinginputChanged(self):
        self.weeklyresting = self.weeklyrestinginput.value()
        self.readTableContents()
        self.checkWeeklyRestBtn.setStyleSheet("background-color:#DCDCDC;")
    def getQTableWidgetSize(self, table):
        w = table.verticalHeader().width() + 2
        for i in range(table.columnCount()):
            w += table.columnWidth(i)  # seems to include gridline (on my machine)
        h = table.horizontalHeader().height() + 2
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        return QSize(w, h)
    def getShiftSums(self):
        self.shiftsof1.setText(str(self.shift1))
        if self.shifttype > 1:
            self.shiftsof2.setText(str(self.shift2))
        if self.shifttype > 2:
            self.shiftsof3.setText(str(self.shift3))
    def updateTable2(self):
        for j in range(7):
            shift1 = 0
            shift2 = 0
            shift3 = 0
            for i in range(len(self.series)):
                widget = self.table.cellWidget(i, j)
                if isinstance(widget, QComboBox):
                    value = widget.currentIndex()
                    if value == 0:
                        shift1 += 1
                    elif value == 1:
                        shift2 += 1
                    elif value == 2:
                        shift3 += 1
            widget1 = self.table2.cellWidget(0, j)
            widget1.setText(str(shift1))
            if shift1 < 1:
                widget1.setStyleSheet("background-color:#800000;");
                widget1.hide()
                widget1.show()
            else:
                widget1.setStyleSheet("background-color:#008000;");
                widget1.hide()
                widget1.show()
            if self.shifttype > 1:
                widget2 = self.table2.cellWidget(1, j)
                widget2.setText(str(shift2))
                if shift2 < 1:
                    widget2.setStyleSheet("background-color:#800000;");
                    widget2.hide()
                    widget2.show()
                else:
                    widget2.setStyleSheet("background-color:#008000;");
                    widget2.hide()
                    widget2.show()
            if self.shifttype > 2:
                widget3 = self.table2.cellWidget(2, j)
                widget3.setText(str(shift3))
                if shift3 < 1:
                    widget3.setStyleSheet("background-color:#800000;");
                    widget3.hide()
                    widget3.show()
                else:
                    widget3.setStyleSheet("background-color:#008000;");
                    widget3.hide()
                    widget3.show()
    def readTableContents(self):
        self.checkWeeklyRestBtn.setStyleSheet("background-color:#DCDCDC;")
        self.shift1 = 0
        self.shift2 = 0
        self.shift3 = 0
        widget = self.table.cellWidget(len(self.series)-1, 7)
        if isinstance(widget, QComboBox):
            prevval = widget.currentIndex()
        else:
            prevval = -1
        for i in range(len(self.series)):
            for j in range(7):
                widget = self.table.cellWidget(i, j)
                if isinstance(widget, QComboBox):
                    value = widget.currentIndex()
                    if value == 0:
                        self.shift1 += 1
                    elif value == 1:
                        self.shift2 += 1
                    elif value == 2:
                        self.shift3 += 1
                    if value >= prevval or self.dailyresting < (16 - (prevval-value)*self.shiftlengths):
                        widget.setStyleSheet("background-color:#008000;");
                    else:
                        widget.setStyleSheet("background-color:#800000;");
                    prevval = value
                else:
                    prevval = -1
        # Ensure first object is checked after last object as this is rotational so day 0 comes after day -1
        widget = self.table.cellWidget(0, 0)
        if isinstance(widget, QComboBox):
            value = widget.currentIndex()
            if value >= prevval or self.dailyresting < (16 - (prevval-value)*self.shiftlengths):
                widget.setStyleSheet("background-color:#008000;");
            else:
                widget.setStyleSheet("background-color:#800000;");
        self.getShiftSums()
        self.updateTable2()
        self.matrix = self.createFullMatrix()
    def loadFunction(self):
        filename, type = QFileDialog.getOpenFileName(self, 'Load File', "", "Text Files (*.txt)", options=QFileDialog.DontUseNativeDialog)
        if len(filename) > 0:
            self.solutionsBrowsing.setValue(0)
            self.solutionsSlider.setValue(0)
            self.findSolutionsBtn.setVisible(True)
            self.solutionsBrowsing.setVisible(False)
            self.solutionsSlider.setVisible(False)
            self.solutionsLbl.setVisible(False)
            with open(filename, 'r') as in_file:
                self.shifttype, self.shifts, self.series, self.shiftlengths, self.dailyresting, solutionMatrix = load(in_file)
            self.solutionMatrices = [solutionMatrix]
            self.solutionMatrix2Table1()
    def saveFunction(self):
        filename, type = QFileDialog.getSaveFileName(self, 'Save File', "Untitled.txt", "Text Files (*.txt)", options=QFileDialog.DontUseNativeDialog)
        if len(filename) > 0:
            if len(filename.split(".")) > 1:
                if filename.split(".")[-1] != "txt":
                    filename = filename+".txt"
            elif len(filename.split(".")) < 2:
                filename = filename+".txt"
            solutionMatrix = self.table1ToSolutionMatrix()
            toSave = [self.shifttype, self.shifts, self.series, self.shiftlengths, self.dailyresting, solutionMatrix]
            with open(filename, 'w') as out_file:
                dump(toSave, out_file)
    def exportFunction(self):
        filename, type = QFileDialog.getSaveFileName(self, 'Save output as...')
        format, ok = QInputDialog.getItem(self, "Export filetype", "Select filetype to export file into", ["CSV", "txt"], 1, False)
        if filename is not None and len(filename)>0 and ok is True:
            matrix = self.createFullMatrix()
            weeks = len(self.series)
            if format == "txt":
                file = open(filename+".txt", 'w')
                weekdays = "Mon\tTue\tWed\tThu\tFri\tSat\tSun\t"
                headlabel = "Worker:\t\t"
                for week in range(weeks):
                    headlabel = headlabel+weekdays
                file.write(headlabel+"\n")
                for ind, person in enumerate(matrix):
                    file.write("Person P"+str(ind)+"\t"+"\t".join(person)+"\n")
                file.close()
            elif format == "CSV":
                file = writer(open(filename+".csv", 'w'))
                weekdays = "Mon;Tue;Wed;Thu;Fri;Sat;Sun"
                for week in range(weeks):
                    if week == 0:
                        headlabel = "Worker:;"+weekdays
                    else:
                        headlabel = headlabel + ";" + weekdays
                file.writerow(headlabel.split(";"))
                for ind, person in enumerate(matrix):
                    person.insert(0,"Person "+str(ind))
                    file.writerow(person)
    def createFullMatrix(self):
        matrix0 = []
        for i in range(len(self.series)):
            cmatrix = []
            for j in range(7):
                widget = self.table.cellWidget(i, j)
                if isinstance(widget, QComboBox):
                    value = widget.currentText()
                    cmatrix.append(str(value))
                else:
                    cmatrix.append("-")
            matrix0.append(cmatrix)
        matrix = []
        for ind, rows in enumerate(matrix0):
            if ind == 0:
                expsub = matrix0.copy()
            else:
                switch = expsub[len(expsub)-1]
                del expsub[len(expsub)-1]
                expsub.insert(0,switch)
            personseries = []
            for week in expsub:
                for day in week:
                    personseries.append(day)
            matrix.append(personseries)
        return matrix
    def findSolution(self):
        # Now convert all series' values to zeroes and ones
        self.zeroOneS = []
        for m in range(len(self.matrix[0])):
            if self.matrix[0][m] == "-":
                self.zeroOneS.append(0)
            else:
                self.zeroOneS.append(1)
        self.findSolutionsBtn.setText("Finding solutions. Combinations to go through: "+str(int(float(self.shifttype)**float(sum(self.zeroOneS)))))
        QApplication.processEvents()
        QCoreApplication.processEvents()
        shifts = []
        for m in range(len(self.shifts)):
            shifts.append(m+1)
        # Now we have to try to construct solution matrices
        noofcombinations = int(float(self.shifttype)**float(sum(self.zeroOneS)))
        print(noofcombinations)
        if noofcombinations > 10**9:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Select how to proceed")
            memoryNeeded = noofcombinations*sum(self.zeroOneS)
            if memoryNeeded < 10**12:
                memoryNeeded = str(memoryNeeded/(10**9)) + " Gb"
            else:
                memoryNeeded = str(memoryCalc/(10**12)) + " Tb"
            msgbox.setText("Combinations to go through: "+str(noofcombinations)+".\nThis means up to "+memoryNeeded+" may be required in memory mode.\n\n     : Select which method to proceed with : \n\nInternal Memory mode may require substantial amount of memories.\n\nProcessing Mode requires less far less internal memory but more processing power (and is usually slower).")
            memBtn = msgbox.addButton("Memory Mode",QMessageBox.ResetRole)
            procBtn = msgbox.addButton("Processor Mode",QMessageBox.ApplyRole)
            cancelBtn = msgbox.addButton("Cancel",QMessageBox.NoRole)
            msgbox.exec_()
            if msgbox.clickedButton() == memBtn:
                proceed = 1
                mode = "proc"
            elif msgbox.clickedButton() == procBtn:
                proceed = 1
                mode = "mem"
            else:
                proceed = 0
                mode = ""
        else:
            proceed = 1
            mode = "mem"
        if proceed == 1:
            t0 = time()
            if mode == "proc":
                arrays = [[shifts[0]] * sum(self.zeroOneS)]
                self.solutionMatrices = self.recursiveCartesianProduct(sum(self.zeroOneS),shifts,arrays,arrays[0],1,1)
                if self.checkifshiftsOK(self.solutionMatrices[0]) == False:
                    del self.solutionMatrices[0]
            elif mode == "mem":
                self.solutionMatrices = list(self.createSolutionMatrices(sum(self.zeroOneS),shifts))
            t1  = time()
            if mode == "proc" or mode == "mem":
                print("Solutions found: "+str(int(len(self.solutionMatrices))))
                print("Time for completion: "+str(float("{:.6f}".format(t1-t0)))+" s")
                self.findSolutionsBtn.setText("Solutions found: "+str(int(len(self.solutionMatrices))))
                if len(self.solutionMatrices) > 0:
                    self.findSolutionsBtn.setEnabled(False)
                    self.findSolutionsBtn.setToolTip("Already generated, solutions found: "+str(len(self.solutionMatrices)))
                    self.solutionsBrowsing.setVisible(True)
                    self.solutionsBrowsing.setValue(0)
                    self.solutionsBrowsing.setRange(0,len(self.solutionMatrices)-1)
                    self.solutionsSlider.setVisible(True)
                    self.solutionsSlider.setValue(0)
                    self.solutionsSlider.setRange(0,len(self.solutionMatrices)-1)
                    self.solutionsLbl.setVisible(True)
                    self.solutionMatrix2Table1()
                else:
                    self.findSolutionsBtn.setEnabled(True)
                    self.solutionsBrowsing.setVisible(False)
                    self.solutionsSlider.setVisible(False)
                    self.solutionsLbl.setVisible(False)
    def solutionIntChangedS(self):
        self.solutionsBrowsing.setValue(self.solutionsSlider.value())
    def solutionIntChangedI(self):
        self.solutionsSlider.setValue(self.solutionsBrowsing.value())
        self.solutionMatrix2Table1()
    def table1ToSolutionMatrix(self):
        day = -1
        solutionMatrix = []
        for i in range(len(self.series)):
            for j in range(7):
                day += 1
                widget = self.table.cellWidget(i, j)
                if isinstance(widget, QComboBox):
                    solutionMatrix.append(widget.currentIndex()+1)
                elif isinstance(widget, QLabel):
                    solutionMatrix.append(0)
        return solutionMatrix
    def solutionMatrix2Table1(self):
        day = -1
        for i in range(len(self.series)):
            for j in range(7):
                day += 1
                widget = self.table.cellWidget(i, j)
                if isinstance(widget, QComboBox):
                    widget.setCurrentIndex(int(self.solutionMatrices[self.solutionsBrowsing.value()][day])-1)
                    widget.hide()
                    widget.show()
    def insertFreeDaysInSolutionMatrix(self,input):
        ind = -1
        matrixOut = []
        for m in range(len(self.zeroOneS)):
            if self.zeroOneS[m] == 1:
                ind += 1
                matrixOut.append(input[ind])
            else:
                matrixOut.append(0)
        return matrixOut
    def find1Solution(self):
        # Now convert all series' values to zeroes and ones
        self.zeroOneS = []
        for m in range(len(self.matrix[0])):
            if self.matrix[0][m] == "-":
                self.zeroOneS.append(0)
            else:
                self.zeroOneS.append(1)
        shifts = []
        for m in range(len(self.shifts)):
            shifts.append(m+1)
        t0 = time()
        arrays = [[shifts[0]] * sum(self.zeroOneS)]
        self.solutionMatrices = self.recursiveCartesianProduct(sum(self.zeroOneS),shifts,arrays,arrays[0],1,0)
        if self.checkifshiftsOK(self.solutionMatrices[0]) == False:
            del self.solutionMatrices[0]
        t1  = time()
        print("Time for completion: "+str(float("{:.6f}".format(t1-t0)))+" s")
        if len(self.solutionMatrices) > 0:
            self.find1SolutionBtn.setEnabled(False)
            self.solutionMatrix2Table1()
        self.solutionsBrowsing.setVisible(False)
        self.solutionsSlider.setVisible(False)
        self.solutionsLbl.setVisible(False)
    def recursiveCartesianProduct(self,days,shifts,arrays,array,level,manySolutions):
        if len(arrays) > 1 and manySolutions == 0:
            return arrays
        else:
            for m in range(1,len(shifts)):
                for n in range(level-1,days):
                    if array[n] != shifts[m]:
                        array2 = array.copy()
                        array2[n] = shifts[m]
                        matrixOut = self.insertFreeDaysInSolutionMatrix(array2)
                        if matrixOut not in arrays:
                            if self.checkifshiftsOK(matrixOut) == True:
                                arrays.append(matrixOut)
                            if level < days:
                                arrays = self.recursiveCartesianProduct(days,shifts,arrays,array2,level+1,manySolutions)
            return arrays
    def createSolutionMatrices(self,days,shifts):
        results = self.cartesianProduct(days,shifts).tolist()
        for indR, result in enumerate(results):
            for indV, value in enumerate(result):
                results[indR][indV] = int(value)
        for result in results:
            matrixOut = self.insertFreeDaysInSolutionMatrix(result)
            shiftsOk = self.checkifshiftsOK(matrixOut)
            if shiftsOk == True:
                yield matrixOut
    def cartesianProduct(self,days,shifts):
        arrays = []
        print(days)
        print(shifts)
        for n in range(days):
            arrays.append(shifts)
        arr = numpy.empty([len(a) for a in arrays] + [days])
        for i, a in enumerate(numpy.ix_(*arrays)):
            arr[...,i] = a
        return arr.reshape(-1, days)
    def checkWeeklyRest(self):
        if self.freedaysweeklycheck(self.table1ToSolutionMatrix(),1) == True:
            self.checkWeeklyRestBtn.setStyleSheet("background-color:#008000;");
        else:
            self.checkWeeklyRestBtn.setStyleSheet("background-color:#800000;");


    def freedaysweeklycheck(self,item1,printout): # Just another constraint that must be fulfilled
        shiftstarts = 24/3

        noOnes = 0 # check so that number of free days over 7 day periods rule is followed.
        item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
        appendflag = True
        for m in range(len(item1)-7,len(item1)):
            item2.append(item1[m])
        for m in range(len(item1)):
            item2.append(item1[m])

        restingTime = 0
        daysGoneBy = 0
        hoursSinceShiftEnd = 0
        for ind,item in enumerate(item2):
            if item > 0:
                timetoShift = (item-1)*shiftstarts
                if timetoShift + hoursSinceShiftEnd >= self.weeklyresting:
                    daysGoneBy = 0
                else:
                    daysGoneBy += 1
                hoursSinceShiftEnd = 24 - ((item-1)*shiftstarts + self.shiftlengths)
            elif item == 0:
                hoursSinceShiftEnd = hoursSinceShiftEnd + 24
            if daysGoneBy > 6:
                appendflag = False
        return appendflag
    def checkifshiftsOK(self,solutionMatrix):
        shiftsOk = True
        prevval = 0
        # Check so time between each shift is obliged
        for shift in solutionMatrix:
            if int(shift) >= prevval or self.dailyresting < (16 - (prevval-int(shift))*self.shiftlengths):
                prevval = int(shift)
            elif int(shift) == 0:
                prevval = int(shift)
            else:
                prevval = int(shift)
                shiftsOk = False
        # Check so time between each last and first shift is obliged since shift 0 follows shift -1
        if solutionMatrix[0] < int(shift):
            shiftsOk = False
        # Check if all shifts are filled
        if shiftsOk == True:
            shiftsOk = self.freedaysweeklycheck(solutionMatrix,0)
        if shiftsOk == True:
            day = -1
            dayShifts = []
            for m in range(7):
                dayShifts.append([])
            for n in range(int(len(solutionMatrix))):
                day += 1
                dayShifts[day].append(int(solutionMatrix[n]))
                if day == 6:
                    day = -1
            for k in range(len(dayShifts)):
                if sum(dayShifts[k]) > 0:
                    for l in range(1,self.shifttype+1):
                        if l not in dayShifts[k]:
                            shiftsOk = False
        return shiftsOk

if __name__ == '__main__':
    app = QApplication([sys.argv[0]])
    # window = DialogPhase2(3,['D', 'E', 'N'],[[1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1], [1, 1, 1, 0, 1, 1, 1], [1, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0]],8.33)
    # window = DialogPhase2(2,['D', 'E'],[[0, 0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0]],8.33)
    # window = DialogPhase2(3,['D', 'E', 'N'],[[0, 0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0]],8.33)
    window = DialogPhase2(3,['D', 'E', 'N'],[[0, 0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0]],8.33)

    window.show()
    sys.exit(app.exec_())
