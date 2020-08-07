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
# # # #                                                                                   # # # #
# # # #                                                                                   # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PyQt5.QtWidgets import QApplication,QComboBox,QDialog,QFileDialog,QGridLayout,QHeaderView,QInputDialog,QLabel,QPushButton,QSpinBox,QTableWidget,QVBoxLayout
from PyQt5.QtCore import QSize, Qt
from csv import writer
import sys

class DialogPhase2(QDialog):
    def __init__(self, shifttype, shifts, series, shiftlengths, parent=None):
        super(DialogPhase2, self).__init__(parent)
        self.setWindowTitle("1o2o3 S-CSV-fcal phase 2")
        if shifttype == 0 and shifts == 0 and series == 0 and shiftlengths == 0:
            self.loadFunction() # For future ...
        else:
            self.shifttype = shifttype
            self.shifts = shifts
            self.series = series
            self.shiftlengths = shiftlengths
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
        dailyrestingtimelbl = QLabel("Minimum continuous daily resting time [h]: ")
        self.layout.addWidget(dailyrestingtimelbl,row,0,1,4)
        self.dailyrestinginput = QSpinBox()
        self.dailyrestinginput.setValue(self.dailyresting)
        self.dailyrestinginput.setMinimum(1)
        self.dailyrestinginput.setToolTip("Swedish law: 11 hours minimum")
        self.dailyrestinginput.valueChanged.connect(self.dailyrestinginputChanged)
        self.layout.addWidget(self.dailyrestinginput,row,4,1,3)
        row += 1
        toplabel4 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel4.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(toplabel4, row, 0, 1, 7)
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
        self.loadButton.setEnabled(False)
        self.loadButton.setToolTip("Future feature")
        self.layout.addWidget(self.loadButton,row,0,3,2)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveFunction)
        self.saveButton.setEnabled(False)
        self.saveButton.setToolTip("Future feature")
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
    def dailyrestinginputChanged(self):
        self.dailyresting = self.dailyrestinginput.value()
        # shiftdiff = int(16 - self.shiftlengths) + (16 - self.shiftlengths > 0)
        # self.dailyshiftsdiff = int(self.dailyresting/shiftdiff) + (self.dailyresting/shiftdiff > 0)
        self.readTableContents()
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
            else:
                widget1.setStyleSheet("background-color:#008000;");
            if self.shifttype > 1:
                widget2 = self.table2.cellWidget(1, j)
                widget2.setText(str(shift2))
                if shift2 < 1:
                    widget2.setStyleSheet("background-color:#800000;");
                else:
                    widget2.setStyleSheet("background-color:#008000;");
            if self.shifttype > 2:
                widget3 = self.table2.cellWidget(2, j)
                widget3.setText(str(shift3))
                if shift3 < 1:
                    widget3.setStyleSheet("background-color:#800000;");
                else:
                    widget3.setStyleSheet("background-color:#008000;");
    def readTableContents(self):
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

        self.getShiftSums()
        self.updateTable2()
    def loadFunction(self):
        print("Load")
    def saveFunction(self):
        print("Save")
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

if __name__ == '__main__':
    app = QApplication([sys.argv[0]])
    window = DialogPhase2(0,0,0)
    window.show()
    sys.exit(app.exec_())
