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
# # # #   Milestone 3 (phase 2 all working, initial version ready):         2020-07-02    # # # #
# # # #                                                                                   # # # #
# # # #                                                                                   # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import PyQt5.QtWidgets as QtGui
from PyQt5 import QtCore
import sys

class Dialog(QtGui.QDialog):
    def __init__(self, input):
        super(Dialog, self).__init__()
        self.setWindowTitle("1o2o3 S-CSV-fcal phase 2")
        self.series, self.shifts, self.shifttype = self.fixInput(input)
        self.initValues()
        self.createLayout()
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
        self.layout = QtGui.QGridLayout(self)
        toplabel1 = QtGui.QLabel("1-, 2- or 3-Shift CSV File Constructor Algorithm.")
        toplabel2 = QtGui.QLabel("- - - -  Define the parameters below  - - - -")
        toplabel3 = QtGui.QLabel("")
        dailyrestingtimelbl = QtGui.QLabel("Minimum continuous daily resting time [h]: ")
        toplabel1.setAlignment(QtCore.Qt.AlignCenter)
        toplabel2.setAlignment(QtCore.Qt.AlignCenter)
        toplabel3.setAlignment(QtCore.Qt.AlignCenter)
        row = 0
        self.layout.addWidget(toplabel1, row,0,1,7)
        row += 1
        self.layout.addWidget(toplabel2, row,0,1,7)
        row += 1
        self.layout.addWidget(toplabel3, row,0,1,7)
        row += 1
        dailyrestingtimelbl = QtGui.QLabel("Minimum continuous daily resting time [h]: ")
        self.layout.addWidget(dailyrestingtimelbl,row,0,1,4)
        self.dailyrestinginput = QtGui.QSpinBox()
        self.dailyrestinginput.setValue(self.dailyresting)
        self.dailyrestinginput.setMinimum(1)
        self.dailyrestinginput.setToolTip("Swedish law: 11 hours minimum")
        self.dailyrestinginput.valueChanged.connect(self.dailyrestinginputChanged)
        self.layout.addWidget(self.dailyrestinginput,row,4,1,3)

        row += 1
        toplabel4 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel4.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel4, row, 0, 1, 7)

        row += 1
        tablelayout = QtGui.QVBoxLayout()
        self.layout.addLayout(tablelayout,row,0,len(self.series),7)

        self.table = QtGui.QTableWidget() # Create table for the series we work with
        tablelayout.addWidget(self.table)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels("Mon;Tue;Wed;Thu;Fri;Sat;Sun".split(";"))
        for i in range(0,7):
            self.table.horizontalHeader().setSectionResizeMode(i, QtGui.QHeaderView.Stretch)
        self.table.setRowCount(len(self.series))
        for row, serie in enumerate(self.series):
            for col, value in enumerate(serie):
                if value == 0:
                    wdg = QtGui.QLabel("0")
                    wdg.setAlignment(QtCore.Qt.AlignCenter)
                else:
                    wdg = QtGui.QComboBox()
                    for t in self.shifts:
                        wdg.addItem(t)
                    wdg.currentIndexChanged.connect(self.readTableContents)
                self.table.setCellWidget(row,col,wdg)
        self.table.setMaximumSize(self.getQTableWidgetSize(self.table))
        self.table.setMinimumSize(self.getQTableWidgetSize(self.table))

        row = row + 1 + len(self.series)*4
        toplabel5 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel5.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel5, row, 0, 1, 7)
        row += 1
        self.shifttype1Label = QtGui.QLabel("Number of "+self.shifts[0]+"-shifts: ")
        self.layout.addWidget(self.shifttype1Label, row, 0, 1, 2)
        self.shiftsof1 = QtGui.QLabel(str(self.shift1))
        self.layout.addWidget(self.shiftsof1, row, 2, 1, 2)
        if self.shifttype > 1:
            row += 1
            self.shifttype1Label = QtGui.QLabel("Number of "+self.shifts[1]+"-shifts: ")
            self.layout.addWidget(self.shifttype1Label, row, 0, 1, 2)
            self.shiftsof2 = QtGui.QLabel(str(self.shift2))
            self.layout.addWidget(self.shiftsof2, row, 2, 1, 2)
        if self.shifttype > 2:
            row += 1
            self.shifttype1Label = QtGui.QLabel("Number of "+self.shifts[2]+"-shifts: ")
            self.layout.addWidget(self.shifttype1Label, row, 0, 1, 2)
            self.shiftsof3 = QtGui.QLabel(str(self.shift3))
            self.layout.addWidget(self.shiftsof3, row, 2, 1, 2)
        row += 1
        toplabel6 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel6.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel6, row, 0, 1, 7)

        row += 1
        toplabel7 = QtGui.QLabel("Results:")
        toplabel7.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel7, row, 0, 1, 7)

        row += 1
        toplabel8 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel8.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel8, row, 0, 1, 7)


        row += 1
        table2layout = QtGui.QVBoxLayout()
        self.layout.addLayout(table2layout,row,0,3,7)

        self.table2 = QtGui.QTableWidget() # Create table for the series we work with
        table2layout.addWidget(self.table2)
        self.table2.setColumnCount(7)
        self.table2.setHorizontalHeaderLabels("Mon;Tue;Wed;Thu;Fri;Sat;Sun".split(";"))
        for i in range(0,7):
            self.table2.horizontalHeader().setSectionResizeMode(i, QtGui.QHeaderView.Stretch)
        self.table2.setRowCount(self.shifttype)
        for row in range(self.shifttype):
            for col in range(7):
                wdg = QtGui.QLabel("0")
                wdg.setAlignment(QtCore.Qt.AlignCenter)
                self.table2.setCellWidget(row,col,wdg)
        self.table2.setMaximumSize(self.getQTableWidgetSize(self.table2))
        self.table2.setMinimumSize(self.getQTableWidgetSize(self.table2))
    def dailyrestinginputChanged(self):
        self.dailyresting = self.dailyrestinginput.value()
    def getQTableWidgetSize(self, table):
        w = table.verticalHeader().width() + 2
        for i in range(table.columnCount()):
            w += table.columnWidth(i)  # seems to include gridline (on my machine)
        h = table.horizontalHeader().height() + 2
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        return QtCore.QSize(w, h)
    def fixInput(self,input):
        out2 = int(input[0])
        del input[0]
        out1 = []
        for i in range(out2):
            out1.append(input[i])
        for i in range(out2):
            del input[0]
        in0 = " ".join(input).split(" / ")
        out = []
        for inp in in0:
            inp = inp.split(" ")
            for i in range(0, len(inp)):
                inp[i] = int(inp[i])
            out.append(inp)
        return out, out1, out2
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
                if isinstance(widget, QtGui.QComboBox):
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
        for i in range(len(self.series)):
            for j in range(7):
                widget = self.table.cellWidget(i, j)
                if isinstance(widget, QtGui.QComboBox):
                    value = widget.currentIndex()
                    if value == 0:
                        self.shift1 += 1
                    elif value == 1:
                        self.shift2 += 1
                    elif value == 2:
                        self.shift3 += 1
        self.getShiftSums()
        self.updateTable2()

if __name__ == '__main__':
    input = [sys.argv[i] for i in range(1,len(sys.argv))]
    app = QtGui.QApplication([sys.argv[0]])
    window = Dialog(input)
    window.show()
    sys.exit(app.exec_())
