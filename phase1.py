# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # #                                                                                   # # # #
# # # #                    1/2/3-shift scheduling algorithm - phase 1:                    # # # #
# # # #                                                                                   # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                       # # # #
# # # #                                                                                   # # # #
# # # #                             Automatic shift generator                             # # # #
# # # #                                                                                   # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                       # # # #
# # # #                                                                                   # # # #
# # # #   Author: Benjamin Bolling                                                        # # # #
# # # #   Affiliation: European Spallation Source ERIC                                    # # # #
# # # #   Lund, Sweden                                                                    # # # #
# # # #   Initialization date: 2020-06-08                                                 # # # #
# # # #   Milestone 1 (phase 1, 0:s and 1:s generated):                     2020-06-29    # # # #
# # # #   Milestone 2 (phase 1 all working, proceeding to phase 2):         2020-07-01    # # # #
# # # #                                                                                   # # # #
# # # #                                                                                   # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import PyQt5.QtWidgets as QtGui
from PyQt5 import QtCore
import sys, time, os

class Dialog(QtGui.QWidget):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("1o2o3 S-CSV-fcal phase 1")
        self.valuesInit()
        self.createLayout()
        self.afterworkvisibleinvisible(False)
    def valuesInit(self):
        # Inputs values
        self.shifttype = 1          # 1-shift or 2-shift or 3-shift, 1, 2, 3, resp.
        self.workingdays = 7        # Amount of days per week
        self.noofweeks = 2          # Amount of weeks to cycle over
        self.shiftlengths = 8.33    # Length of shifts in hours
        self.workinghours = 36      # Amount of working hours per person each week
        self.weeklyresting = 36     # Length of weekly minimum single continuous resting time in hours
        self.overwrite = 0          # In order to avoid re-running the algorithm unnecessarily
        self.shiftLabel1 = "D"      # Define how this shift is to be labelled in the next phase
        self.shiftLabel2 = "E"      # Define how this shift is to be labelled in the next phase
        self.shiftLabel3 = "N"      # Define how this shift is to be labelled in the next phase
    def createLayout(self):
        self.layout = QtGui.QGridLayout(self)
        toplabel1 = QtGui.QLabel("1-, 2- or 3-Shift Combinations Generator Algorithm.")
        toplabel2 = QtGui.QLabel("- - - -  Define the parameters below  - - - -")
        toplabel3 = QtGui.QLabel("")
        toplabel1.setAlignment(QtCore.Qt.AlignCenter)
        toplabel2.setAlignment(QtCore.Qt.AlignCenter)
        toplabel3.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel1, 0,0,1,7)
        self.layout.addWidget(toplabel2, 1,0,1,7)
        self.layout.addWidget(toplabel3, 2,0,1,7)

        # Labels / descriptions
        twothreeshiftslbl = QtGui.QLabel("Shift type: ")
        daysperweeklbl = QtGui.QLabel("Working days per week: ")
        noOfPeoplelbl = QtGui.QLabel("Number of people: ")
        noOfWeekslbl = QtGui.QLabel("Number of weeks to cycle over: ")
        noofpeoplepershiftlbl = QtGui.QLabel("Number of people per shift: ")
        lengthofshiftlbl = QtGui.QLabel("Shift Lengths [h]: ")
        workinghourslbl = QtGui.QLabel("Weekly working hours per person [h]: ")
        weeklyrestingtimelbl = QtGui.QLabel("Weekly minimum single continuous resting time [h]: ")

        # Shift type radiobuttons (2 or 3 shift)
        row = 3
        self.layout.addWidget(twothreeshiftslbl,row,0,1,4)
        self.shifttyperadiobutton = QtGui.QRadioButton("1-shift")
        self.shifttyperadiobutton.setChecked(True)
        self.shifttyperadiobutton.shift = 1
        self.shifttyperadiobutton.toggled.connect(self.shifttyperadiobuttonClicked)
        self.layout.addWidget(self.shifttyperadiobutton, row, 4, 1, 1)
        self.shifttyperadiobutton = QtGui.QRadioButton("2-shift")
        self.shifttyperadiobutton.shift = 2
        self.shifttyperadiobutton.toggled.connect(self.shifttyperadiobuttonClicked)
        self.layout.addWidget(self.shifttyperadiobutton, row, 5, 1, 1)
        self.shifttyperadiobutton = QtGui.QRadioButton("3-shift")
        self.shifttyperadiobutton.shift = 3
        self.shifttyperadiobutton.toggled.connect(self.shifttyperadiobuttonClicked)
        self.layout.addWidget(self.shifttyperadiobutton, row, 6, 1, 1)
        row += 1
        shiftLabelslbl = QtGui.QLabel("Define the shift labels (e.g. D / E / N): ")
        self.layout.addWidget(shiftLabelslbl, row, 0, 1, 4)
        self.shiftLabel1Edit = QtGui.QLineEdit(self.shiftLabel1)
        self.shiftLabel1Edit.setMaxLength(2)
        self.shiftLabel1Edit.setFixedWidth(50)
        self.shiftLabel1Edit.textChanged.connect(self.shiftLabelsClicked)
        self.layout.addWidget(self.shiftLabel1Edit, row, 4, 1, 1)
        self.shiftLabel2Edit = QtGui.QLineEdit(self.shiftLabel2)
        self.shiftLabel2Edit.setMaxLength(2)
        self.shiftLabel2Edit.setFixedWidth(50)
        self.shiftLabel2Edit.setVisible(False)
        self.shiftLabel2Edit.textChanged.connect(self.shiftLabelsClicked)
        self.layout.addWidget(self.shiftLabel2Edit, row, 5, 1, 1)
        self.shiftLabel3Edit = QtGui.QLineEdit(self.shiftLabel3)
        self.shiftLabel3Edit.setMaxLength(2)
        self.shiftLabel3Edit.setFixedWidth(50)
        self.shiftLabel3Edit.setVisible(False)
        self.shiftLabel3Edit.textChanged.connect(self.shiftLabelsClicked)
        self.layout.addWidget(self.shiftLabel3Edit, row, 6, 1, 1)
        row += 1
        toplabel4 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel4.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(toplabel4, row, 0, 1, 7)
        row += 1
        self.layout.addWidget(daysperweeklbl,row,0,1,4)
        self.workingdaysinput = QtGui.QSpinBox()
        self.workingdaysinput.setValue(self.workingdays)
        self.workingdaysinput.setRange(1,7)
        self.workingdaysinput.valueChanged.connect(self.workingdaysinputChanged)
        self.layout.addWidget(self.workingdaysinput, row, 4, 1, 3)
        row += 1
        self.layout.addWidget(noOfWeekslbl,row,0,1,4)
        self.noofweeksinput = QtGui.QSpinBox()
        self.noofweeksinput.setValue(self.noofweeks)
        self.noofweeksinput.setRange(1,10)
        self.noofweeksinput.valueChanged.connect(self.noofweeksinputChanged)
        self.layout.addWidget(self.noofweeksinput, row, 4, 1, 3)
        row += 1
        self.layout.addWidget(lengthofshiftlbl,row,0,1,4)
        self.shiftlengthsinput = QtGui.QDoubleSpinBox()
        self.shiftlengthsinput.setValue(self.shiftlengths)
        self.shiftlengthsinput.setMinimum(8)
        self.shiftlengthsinput.valueChanged.connect(self.shiftlengthsinputChanged)
        self.layout.addWidget(self.shiftlengthsinput, row, 4, 1, 3)
        row += 1
        self.layout.addWidget(workinghourslbl,row,0,1,4)
        self.workinghoursinput = QtGui.QDoubleSpinBox()
        self.workinghoursinput.setValue(self.workinghours)
        self.workinghoursinput.setMinimum(8)
        self.workinghoursinput.valueChanged.connect(self.workinghoursinputChanged)
        self.layout.addWidget(self.workinghoursinput, row, 4, 1, 3)
        row += 1
        self.layout.addWidget(weeklyrestingtimelbl,row,0,1,4)
        self.weeklyrestinginput = QtGui.QSpinBox()
        self.weeklyrestinginput.setValue(self.weeklyresting)
        self.weeklyrestinginput.setMinimum(1)
        self.weeklyrestinginput.setToolTip("Swedish law: 36 hours minimum")
        self.weeklyrestinginput.valueChanged.connect(self.weeklyrestinginputChanged)
        self.layout.addWidget(self.weeklyrestinginput, row, 4, 1, 3)
        row += 1
        self.generateBtn = QtGui.QPushButton("Generate Combinations")
        self.generateBtn.clicked.connect(self.generateBtnClicked)
        self.layout.addWidget(self.generateBtn, row, 4, 1, 3)
        self.saveCombos = QtGui.QPushButton("Save all combos")
        self.saveCombos.clicked.connect(self.saveAllCombos)
        self.saveCombos.setVisible(False)
        self.layout.addWidget(self.saveCombos, row, 2, 1, 2)
        self.loadCombos = QtGui.QPushButton("Load combos")
        self.loadCombos.clicked.connect(self.loadAllcombos)
        self.layout.addWidget(self.loadCombos, row, 0, 1, 2)
        row += 1
        self.messageLabel01 = QtGui.QLabel(">> ")
        self.layout.addWidget(self.messageLabel01, row, 0, 1, 7)
        row += 1
        self.messageLabel02 = QtGui.QLabel("")
        self.layout.addWidget(self.messageLabel02, row, 0, 1, 7)
        row += 1
        self.messageLabel03 = QtGui.QLabel("")
        self.layout.addWidget(self.messageLabel03, row, 0, 1, 7)
        row += 1
        self.afterworklbl01 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.afterworklbl01.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.afterworklbl01, row, 0, 1, 7)
        row += 1
        self.afterworklbl02 = QtGui.QLabel("Post table generation schedule work")
        self.afterworklbl02.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.afterworklbl02, row, 0, 1, 7)
        row += 1
        self.afterworklbl03 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.afterworklbl03.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.afterworklbl03, row, 0, 1, 7)
        row += 1
        self.afterworklbl04 = QtGui.QLabel("Browse through the combinations' indices until you find one to work with:")
        self.layout.addWidget(self.afterworklbl04, row, 0, 1, 7)
        row += 1
        self.afterworkInt = QtGui.QSpinBox()
        self.afterworkInt.valueChanged.connect(self.afterworkIntChangedI)
        self.layout.addWidget(self.afterworkInt, row, 5, 1, 2)
        self.afterworkSlide = QtGui.QSlider()
        self.afterworkSlide.setOrientation(QtCore.Qt.Horizontal)
        self.afterworkSlide.valueChanged.connect(self.afterworkIntChangedS)
        self.layout.addWidget(self.afterworkSlide, row, 0, 1, 5)
        row += 1
        self.afterworklbl05 = QtGui.QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.afterworklbl05.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.afterworklbl05, row, 0, 1, 7)
        row += 1
        self.AWweek00 = QtGui.QLabel("1")
        self.AWweek00.setVisible(False)
        self.layout.addWidget(self.AWweek00, row, 0, 1, 1)
        self.AWweek01 = QtGui.QLabel("1")
        self.AWweek01.setVisible(False)
        self.layout.addWidget(self.AWweek01, row, 1, 1, 1)
        self.AWweek02 = QtGui.QLabel("1")
        self.AWweek02.setVisible(False)
        self.layout.addWidget(self.AWweek02, row, 2, 1, 1)
        self.AWweek03 = QtGui.QLabel("1")
        self.AWweek03.setVisible(False)
        self.layout.addWidget(self.AWweek03, row, 3, 1, 1)
        self.AWweek04 = QtGui.QLabel("1")
        self.AWweek04.setVisible(False)
        self.layout.addWidget(self.AWweek04, row, 4, 1, 1)
        self.AWweek05 = QtGui.QLabel("1")
        self.AWweek05.setVisible(False)
        self.layout.addWidget(self.AWweek05, row, 5, 1, 1)
        self.AWweek06 = QtGui.QLabel("1")
        self.AWweek06.setVisible(False)
        self.layout.addWidget(self.AWweek06, row, 6, 1, 1)
        row += 1
        self.AWweek10 = QtGui.QLabel("2")
        self.AWweek10.setVisible(False)
        self.layout.addWidget(self.AWweek10, row, 0, 1, 1)
        self.AWweek11 = QtGui.QLabel("2")
        self.AWweek11.setVisible(False)
        self.layout.addWidget(self.AWweek11, row, 1, 1, 1)
        self.AWweek12 = QtGui.QLabel("2")
        self.AWweek12.setVisible(False)
        self.layout.addWidget(self.AWweek12, row, 2, 1, 1)
        self.AWweek13 = QtGui.QLabel("2")
        self.AWweek13.setVisible(False)
        self.layout.addWidget(self.AWweek13, row, 3, 1, 1)
        self.AWweek14 = QtGui.QLabel("2")
        self.AWweek14.setVisible(False)
        self.layout.addWidget(self.AWweek14, row, 4, 1, 1)
        self.AWweek15 = QtGui.QLabel("2")
        self.AWweek15.setVisible(False)
        self.layout.addWidget(self.AWweek15, row, 5, 1, 1)
        self.AWweek16 = QtGui.QLabel("2")
        self.AWweek16.setVisible(False)
        self.layout.addWidget(self.AWweek16, row, 6, 1, 1)
        row += 1
        self.AWweek20 = QtGui.QLabel("3")
        self.AWweek20.setVisible(False)
        self.layout.addWidget(self.AWweek20, row, 0, 1, 1)
        self.AWweek21 = QtGui.QLabel("3")
        self.AWweek21.setVisible(False)
        self.layout.addWidget(self.AWweek21, row, 1, 1, 1)
        self.AWweek22 = QtGui.QLabel("3")
        self.AWweek22.setVisible(False)
        self.layout.addWidget(self.AWweek22, row, 2, 1, 1)
        self.AWweek23 = QtGui.QLabel("3")
        self.AWweek23.setVisible(False)
        self.layout.addWidget(self.AWweek23, row, 3, 1, 1)
        self.AWweek24 = QtGui.QLabel("3")
        self.AWweek24.setVisible(False)
        self.layout.addWidget(self.AWweek24, row, 4, 1, 1)
        self.AWweek25 = QtGui.QLabel("3")
        self.AWweek25.setVisible(False)
        self.layout.addWidget(self.AWweek25, row, 5, 1, 1)
        self.AWweek26 = QtGui.QLabel("3")
        self.AWweek26.setVisible(False)
        self.layout.addWidget(self.AWweek26, row, 6, 1, 1)
        row += 1
        self.AWweek30 = QtGui.QLabel("4")
        self.AWweek30.setVisible(False)
        self.layout.addWidget(self.AWweek30, row, 0, 1, 1)
        self.AWweek31 = QtGui.QLabel("4")
        self.AWweek31.setVisible(False)
        self.layout.addWidget(self.AWweek31, row, 1, 1, 1)
        self.AWweek32 = QtGui.QLabel("4")
        self.AWweek32.setVisible(False)
        self.layout.addWidget(self.AWweek32, row, 2, 1, 1)
        self.AWweek33 = QtGui.QLabel("4")
        self.AWweek33.setVisible(False)
        self.layout.addWidget(self.AWweek33, row, 3, 1, 1)
        self.AWweek34 = QtGui.QLabel("4")
        self.AWweek34.setVisible(False)
        self.layout.addWidget(self.AWweek34, row, 4, 1, 1)
        self.AWweek35 = QtGui.QLabel("4")
        self.AWweek35.setVisible(False)
        self.layout.addWidget(self.AWweek35, row, 5, 1, 1)
        self.AWweek36 = QtGui.QLabel("4")
        self.AWweek36.setVisible(False)
        self.layout.addWidget(self.AWweek36, row, 6, 1, 1)
        row += 1
        self.AWweek40 = QtGui.QLabel("5")
        self.AWweek40.setVisible(False)
        self.layout.addWidget(self.AWweek40, row, 0, 1, 1)
        self.AWweek41 = QtGui.QLabel("5")
        self.AWweek41.setVisible(False)
        self.layout.addWidget(self.AWweek41, row, 1, 1, 1)
        self.AWweek42 = QtGui.QLabel("5")
        self.AWweek42.setVisible(False)
        self.layout.addWidget(self.AWweek42, row, 2, 1, 1)
        self.AWweek43 = QtGui.QLabel("5")
        self.AWweek43.setVisible(False)
        self.layout.addWidget(self.AWweek43, row, 3, 1, 1)
        self.AWweek44 = QtGui.QLabel("5")
        self.AWweek44.setVisible(False)
        self.layout.addWidget(self.AWweek44, row, 4, 1, 1)
        self.AWweek45 = QtGui.QLabel("5")
        self.AWweek45.setVisible(False)
        self.layout.addWidget(self.AWweek45, row, 5, 1, 1)
        self.AWweek46 = QtGui.QLabel("5")
        self.AWweek46.setVisible(False)
        self.layout.addWidget(self.AWweek46, row, 6, 1, 1)
        row += 1
        self.AWweek50 = QtGui.QLabel("6")
        self.AWweek50.setVisible(False)
        self.layout.addWidget(self.AWweek50, row, 0, 1, 1)
        self.AWweek51 = QtGui.QLabel("6")
        self.AWweek51.setVisible(False)
        self.layout.addWidget(self.AWweek51, row, 1, 1, 1)
        self.AWweek52 = QtGui.QLabel("6")
        self.AWweek52.setVisible(False)
        self.layout.addWidget(self.AWweek52, row, 2, 1, 1)
        self.AWweek53 = QtGui.QLabel("6")
        self.AWweek53.setVisible(False)
        self.layout.addWidget(self.AWweek53, row, 3, 1, 1)
        self.AWweek54 = QtGui.QLabel("6")
        self.AWweek54.setVisible(False)
        self.layout.addWidget(self.AWweek54, row, 4, 1, 1)
        self.AWweek55 = QtGui.QLabel("6")
        self.AWweek55.setVisible(False)
        self.layout.addWidget(self.AWweek55, row, 5, 1, 1)
        self.AWweek56 = QtGui.QLabel("6")
        self.AWweek56.setVisible(False)
        self.layout.addWidget(self.AWweek56, row, 6, 1, 1)
        row += 1
        self.AWweek60 = QtGui.QLabel("7")
        self.AWweek60.setVisible(False)
        self.layout.addWidget(self.AWweek60, row, 0, 1, 1)
        self.AWweek61 = QtGui.QLabel("7")
        self.AWweek61.setVisible(False)
        self.layout.addWidget(self.AWweek61, row, 1, 1, 1)
        self.AWweek62 = QtGui.QLabel("7")
        self.AWweek62.setVisible(False)
        self.layout.addWidget(self.AWweek62, row, 2, 1, 1)
        self.AWweek63 = QtGui.QLabel("7")
        self.AWweek63.setVisible(False)
        self.layout.addWidget(self.AWweek63, row, 3, 1, 1)
        self.AWweek64 = QtGui.QLabel("7")
        self.AWweek64.setVisible(False)
        self.layout.addWidget(self.AWweek64, row, 4, 1, 1)
        self.AWweek65 = QtGui.QLabel("7")
        self.AWweek65.setVisible(False)
        self.layout.addWidget(self.AWweek65, row, 5, 1, 1)
        self.AWweek66 = QtGui.QLabel("7")
        self.AWweek66.setVisible(False)
        self.layout.addWidget(self.AWweek66, row, 6, 1, 1)
        row += 1
        self.AWweek70 = QtGui.QLabel("8")
        self.AWweek70.setVisible(False)
        self.layout.addWidget(self.AWweek70, row, 0, 1, 1)
        self.AWweek71 = QtGui.QLabel("8")
        self.AWweek71.setVisible(False)
        self.layout.addWidget(self.AWweek71, row, 1, 1, 1)
        self.AWweek72 = QtGui.QLabel("8")
        self.AWweek72.setVisible(False)
        self.layout.addWidget(self.AWweek72, row, 2, 1, 1)
        self.AWweek73 = QtGui.QLabel("8")
        self.AWweek73.setVisible(False)
        self.layout.addWidget(self.AWweek73, row, 3, 1, 1)
        self.AWweek74 = QtGui.QLabel("8")
        self.AWweek74.setVisible(False)
        self.layout.addWidget(self.AWweek74, row, 4, 1, 1)
        self.AWweek75 = QtGui.QLabel("8")
        self.AWweek75.setVisible(False)
        self.layout.addWidget(self.AWweek75, row, 5, 1, 1)
        self.AWweek76 = QtGui.QLabel("8")
        self.AWweek76.setVisible(False)
        self.layout.addWidget(self.AWweek76, row, 6, 1, 1)
        row += 1
        self.AWweek80 = QtGui.QLabel("9")
        self.AWweek80.setVisible(False)
        self.layout.addWidget(self.AWweek80, row, 0, 1, 1)
        self.AWweek81 = QtGui.QLabel("9")
        self.AWweek81.setVisible(False)
        self.layout.addWidget(self.AWweek81, row, 1, 1, 1)
        self.AWweek82 = QtGui.QLabel("9")
        self.AWweek82.setVisible(False)
        self.layout.addWidget(self.AWweek82, row, 2, 1, 1)
        self.AWweek83 = QtGui.QLabel("9")
        self.AWweek83.setVisible(False)
        self.layout.addWidget(self.AWweek83, row, 3, 1, 1)
        self.AWweek84 = QtGui.QLabel("9")
        self.AWweek84.setVisible(False)
        self.layout.addWidget(self.AWweek84, row, 4, 1, 1)
        self.AWweek85 = QtGui.QLabel("9")
        self.AWweek85.setVisible(False)
        self.layout.addWidget(self.AWweek85, row, 5, 1, 1)
        self.AWweek86 = QtGui.QLabel("9")
        self.AWweek86.setVisible(False)
        self.layout.addWidget(self.AWweek86, row, 6, 1, 1)
        row += 1
        self.AWweek90 = QtGui.QLabel("10")
        self.AWweek90.setVisible(False)
        self.layout.addWidget(self.AWweek90, row, 0, 1, 1)
        self.AWweek91 = QtGui.QLabel("10")
        self.AWweek91.setVisible(False)
        self.layout.addWidget(self.AWweek91, row, 1, 1, 1)
        self.AWweek92 = QtGui.QLabel("10")
        self.AWweek92.setVisible(False)
        self.layout.addWidget(self.AWweek92, row, 2, 1, 1)
        self.AWweek93 = QtGui.QLabel("10")
        self.AWweek93.setVisible(False)
        self.layout.addWidget(self.AWweek93, row, 3, 1, 1)
        self.AWweek94 = QtGui.QLabel("10")
        self.AWweek94.setVisible(False)
        self.layout.addWidget(self.AWweek94, row, 4, 1, 1)
        self.AWweek95 = QtGui.QLabel("10")
        self.AWweek95.setVisible(False)
        self.layout.addWidget(self.AWweek95, row, 5, 1, 1)
        self.AWweek96 = QtGui.QLabel("10")
        self.AWweek96.setVisible(False)
        self.layout.addWidget(self.AWweek96, row, 6, 1, 1)
        row += 1
        self.nextPhase = QtGui.QPushButton("Proceed with this combo to next phase")
        self.nextPhase.clicked.connect(self.runPhaseTwo)
        self.nextPhase.setVisible(False)
        self.layout.addWidget(self.nextPhase, row, 0, 1, 7)
        self.setLayout(self.layout)
    def shifttyperadiobuttonClicked(self):
        self.shifttyperadiobutton = self.sender()
        if self.shifttyperadiobutton.isChecked():
            self.shifttype = self.shifttyperadiobutton.shift
        if self.shifttype == 1:
            self.shiftLabel2Edit.setVisible(False)
            self.shiftLabel3Edit.setVisible(False)
        elif self.shifttype == 2:
            self.shiftLabel2Edit.setVisible(True)
            self.shiftLabel3Edit.setVisible(False)
        else:
            self.shiftLabel2Edit.setVisible(True)
            self.shiftLabel3Edit.setVisible(True)
    def workingdaysinputChanged(self):
        self.workingdays = self.workingdaysinput.value()
    def noofpeopleinputChanged(self):
        self.noofpeople = self.noofpeopleinput.value()
    def noofweeksinputChanged(self):
        self.noofweeks = self.noofweeksinput.value()
    def shiftlengthsinputChanged(self):
        self.shiftlengths = self.shiftlengthsinput.value()
    def workinghoursinputChanged(self):
        self.workinghours = self.workinghoursinput.value()
    def weeklyrestinginputChanged(self):
        self.weeklyresting = self.weeklyrestinginput.value()
    def afterworkIntChangedS(self):
        self.afterworkIntValue = self.afterworkSlide.value()
        self.afterworkInt.setValue(self.afterworkIntValue)
        self.updateafterworkInt()
    def afterworkIntChangedI(self):
        self.afterworkIntValue = self.afterworkInt.value()
        self.afterworkSlide.setValue(self.afterworkIntValue)
        self.updateafterworkInt()
    def afterweeksvisible(self,inp):
        weeksvis = []
        for m in range(0, 10):
            if m < self.noofweeks:
                weeksvis.append(inp)
            else:
                weeksvis.append(False)
        self.nextPhase.setVisible(weeksvis[0])
        self.saveCombos.setVisible(weeksvis[0])
        self.AWweek00.setVisible(weeksvis[0])
        self.AWweek01.setVisible(weeksvis[0])
        self.AWweek02.setVisible(weeksvis[0])
        self.AWweek03.setVisible(weeksvis[0])
        self.AWweek04.setVisible(weeksvis[0])
        self.AWweek05.setVisible(weeksvis[0])
        self.AWweek06.setVisible(weeksvis[0])
        self.AWweek10.setVisible(weeksvis[1])
        self.AWweek11.setVisible(weeksvis[1])
        self.AWweek12.setVisible(weeksvis[1])
        self.AWweek13.setVisible(weeksvis[1])
        self.AWweek14.setVisible(weeksvis[1])
        self.AWweek15.setVisible(weeksvis[1])
        self.AWweek16.setVisible(weeksvis[1])
        self.AWweek20.setVisible(weeksvis[2])
        self.AWweek21.setVisible(weeksvis[2])
        self.AWweek22.setVisible(weeksvis[2])
        self.AWweek23.setVisible(weeksvis[2])
        self.AWweek24.setVisible(weeksvis[2])
        self.AWweek25.setVisible(weeksvis[2])
        self.AWweek26.setVisible(weeksvis[2])
        self.AWweek30.setVisible(weeksvis[3])
        self.AWweek31.setVisible(weeksvis[3])
        self.AWweek32.setVisible(weeksvis[3])
        self.AWweek33.setVisible(weeksvis[3])
        self.AWweek34.setVisible(weeksvis[3])
        self.AWweek35.setVisible(weeksvis[3])
        self.AWweek36.setVisible(weeksvis[3])
        self.AWweek40.setVisible(weeksvis[4])
        self.AWweek41.setVisible(weeksvis[4])
        self.AWweek42.setVisible(weeksvis[4])
        self.AWweek43.setVisible(weeksvis[4])
        self.AWweek44.setVisible(weeksvis[4])
        self.AWweek45.setVisible(weeksvis[4])
        self.AWweek46.setVisible(weeksvis[4])
        self.AWweek50.setVisible(weeksvis[5])
        self.AWweek51.setVisible(weeksvis[5])
        self.AWweek52.setVisible(weeksvis[5])
        self.AWweek53.setVisible(weeksvis[5])
        self.AWweek54.setVisible(weeksvis[5])
        self.AWweek55.setVisible(weeksvis[5])
        self.AWweek56.setVisible(weeksvis[5])
        self.AWweek60.setVisible(weeksvis[6])
        self.AWweek61.setVisible(weeksvis[6])
        self.AWweek62.setVisible(weeksvis[6])
        self.AWweek63.setVisible(weeksvis[6])
        self.AWweek64.setVisible(weeksvis[6])
        self.AWweek65.setVisible(weeksvis[6])
        self.AWweek66.setVisible(weeksvis[6])
        self.AWweek70.setVisible(weeksvis[7])
        self.AWweek71.setVisible(weeksvis[7])
        self.AWweek72.setVisible(weeksvis[7])
        self.AWweek73.setVisible(weeksvis[7])
        self.AWweek74.setVisible(weeksvis[7])
        self.AWweek75.setVisible(weeksvis[7])
        self.AWweek76.setVisible(weeksvis[7])
        self.AWweek80.setVisible(weeksvis[8])
        self.AWweek81.setVisible(weeksvis[8])
        self.AWweek82.setVisible(weeksvis[8])
        self.AWweek83.setVisible(weeksvis[8])
        self.AWweek84.setVisible(weeksvis[8])
        self.AWweek85.setVisible(weeksvis[8])
        self.AWweek86.setVisible(weeksvis[8])
        self.AWweek90.setVisible(weeksvis[9])
        self.AWweek91.setVisible(weeksvis[9])
        self.AWweek92.setVisible(weeksvis[9])
        self.AWweek93.setVisible(weeksvis[9])
        self.AWweek94.setVisible(weeksvis[9])
        self.AWweek95.setVisible(weeksvis[9])
        self.AWweek96.setVisible(weeksvis[9])
    def afterweekslabels(self):
        values = []
        for m in range(0, 70):
            if m < len(self.activeSeries):
                values.append(self.activeSeries[m])
            else:
                values.append(0)
        self.AWweek00.setText(str(values[0]))
        self.AWweek01.setText(str(values[1]))
        self.AWweek02.setText(str(values[2]))
        self.AWweek03.setText(str(values[3]))
        self.AWweek04.setText(str(values[4]))
        self.AWweek05.setText(str(values[5]))
        self.AWweek06.setText(str(values[6]))
        self.AWweek10.setText(str(values[7]))
        self.AWweek11.setText(str(values[8]))
        self.AWweek12.setText(str(values[9]))
        self.AWweek13.setText(str(values[10]))
        self.AWweek14.setText(str(values[11]))
        self.AWweek15.setText(str(values[12]))
        self.AWweek16.setText(str(values[13]))
        self.AWweek20.setText(str(values[14]))
        self.AWweek21.setText(str(values[15]))
        self.AWweek22.setText(str(values[16]))
        self.AWweek23.setText(str(values[17]))
        self.AWweek24.setText(str(values[18]))
        self.AWweek25.setText(str(values[19]))
        self.AWweek26.setText(str(values[20]))
        self.AWweek30.setText(str(values[21]))
        self.AWweek31.setText(str(values[22]))
        self.AWweek32.setText(str(values[23]))
        self.AWweek33.setText(str(values[24]))
        self.AWweek34.setText(str(values[25]))
        self.AWweek35.setText(str(values[26]))
        self.AWweek36.setText(str(values[27]))
        self.AWweek40.setText(str(values[28]))
        self.AWweek41.setText(str(values[29]))
        self.AWweek42.setText(str(values[30]))
        self.AWweek43.setText(str(values[31]))
        self.AWweek44.setText(str(values[32]))
        self.AWweek45.setText(str(values[33]))
        self.AWweek46.setText(str(values[34]))
        self.AWweek50.setText(str(values[35]))
        self.AWweek51.setText(str(values[36]))
        self.AWweek52.setText(str(values[37]))
        self.AWweek53.setText(str(values[38]))
        self.AWweek54.setText(str(values[39]))
        self.AWweek55.setText(str(values[40]))
        self.AWweek56.setText(str(values[41]))
        self.AWweek60.setText(str(values[42]))
        self.AWweek61.setText(str(values[43]))
        self.AWweek62.setText(str(values[44]))
        self.AWweek63.setText(str(values[45]))
        self.AWweek64.setText(str(values[46]))
        self.AWweek65.setText(str(values[47]))
        self.AWweek66.setText(str(values[48]))
        self.AWweek70.setText(str(values[49]))
        self.AWweek71.setText(str(values[50]))
        self.AWweek72.setText(str(values[51]))
        self.AWweek73.setText(str(values[52]))
        self.AWweek74.setText(str(values[53]))
        self.AWweek75.setText(str(values[54]))
        self.AWweek76.setText(str(values[55]))
        self.AWweek80.setText(str(values[56]))
        self.AWweek81.setText(str(values[57]))
        self.AWweek82.setText(str(values[58]))
        self.AWweek83.setText(str(values[59]))
        self.AWweek84.setText(str(values[60]))
        self.AWweek85.setText(str(values[61]))
        self.AWweek86.setText(str(values[62]))
        self.AWweek90.setText(str(values[63]))
        self.AWweek91.setText(str(values[64]))
        self.AWweek92.setText(str(values[65]))
        self.AWweek93.setText(str(values[66]))
        self.AWweek94.setText(str(values[67]))
        self.AWweek95.setText(str(values[68]))
        self.AWweek96.setText(str(values[69]))
    def afterworkvisibleinvisible(self,input):
        self.afterworklbl01.setVisible(input)
        self.afterworklbl02.setVisible(input)
        self.afterworklbl03.setVisible(input)
        self.afterworklbl04.setVisible(input)
        self.afterworklbl05.setVisible(input)
        self.afterworkSlide.setVisible(input)
        self.afterworkInt.setVisible(input)
    def generateBtnClicked(self):
        if self.overwrite == 1:
            override = QtGui.QMessageBox.warning(self, 'Warning', "Warning: Unsaved data will be overwritten. Proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if override == QtGui.QMessageBox.Yes:
                self.overwrite = 0
        if self.overwrite == 0:
            self.overwrite = 1
            shiftsperpersonpercycle = int(self.workinghours*self.noofweeks/self.shiftlengths)+(self.workinghours*self.noofweeks/self.shiftlengths > 0) # rounding integer up
            freetimeperpersonpercycle = self.noofweeks*self.workingdays - shiftsperpersonpercycle
            self.freedaysover7days = int(self.weeklyresting/24)+(self.weeklyresting/24 > 0)
            weeksneeded = int(self.workingdays*self.shifttype*self.shiftlengths/self.workinghours) + (self.workingdays*self.shifttype*self.shiftlengths/self.workinghours > 0)
            if self.noofweeks > 4:
                errorflag = 1
                override = QtGui.QMessageBox.warning(self, 'Warning', str(self.noofweeks)+" weeks might require extensive amount of comping power and/or time. Continue anyways?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if override == QtGui.QMessageBox.Yes:
                    errorflag = 0
            if self.noofweeks < weeksneeded:
                errorflag = 1
                override = QtGui.QMessageBox.warning(self, 'Warning', "Warning: More weeks might be needed. Minimum recommendeded number of weeeks for these settings is "+str(weeksneeded)+". Continue anyways?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if override == QtGui.QMessageBox.Yes:
                    errorflag = 0
            else:
                errorflag = 0
            if errorflag == 0:
                t0 = time.time()
                self.shiftseries, noConstraints = self.createAllShiftPossibilities(range(self.noofweeks*self.workingdays), shiftsperpersonpercycle)
                t1 = time.time()
                if self.shiftseries is None or len(self.shiftseries) == 0:
                    self.messageLabel01.setText("No combinations found.")
                else:
                    self.messageLabel01.setText("Number of combinations with no constraints' =  "+str(noConstraints))
                    self.messageLabel02.setText("Number of combinations with constraints 'free days over 7 days' and 'all shifts filled' =  "+str(len(self.shiftseries)))
                    saveQ, ok = QtGui.QInputDialog.getItem(self, "Save / Print results", "Save all combinations (in .txt-format) or Print combinations found in the terminal output?", ["Save", "Print", "Neither"], 2, False)
                    print(saveQ)
                    if saveQ == "Save":
                        self.saveAllCombos()
                    elif saveQ == "Print":
                        print("Combinations found: ")
                        for combo in self.shiftseries:
                            print(combo)
                self.messageLabel03.setText("Time for completion: "+str(float("{:.6f}".format(t1-t0)))+" s")
                self.afterworkIntValue = 0
                self.afterworkvisibleinvisible(True)
                self.updateafterworkInt()
                self.afterworkSlide.setValue(self.afterworkIntValue)
                self.afterworkInt.setValue(self.afterworkIntValue)
                self.afterworkSlide.setRange(0,len(self.shiftseries)-1)
                self.afterworkInt.setRange(0,len(self.shiftseries)-1)
    def saveAllCombos(self):
        filename, type = QtGui.QFileDialog.getSaveFileName(self, 'Save output as...')
        #filename = input("Enter filename: >> ")
        if filename is not None and len(filename)>0:
            file = open(filename+".combo", 'w')
            for combo in self.shiftseries:
                file.write(combo+"\n")
            file.close()
            self.messageLabel01.setText("Combinations saved as file: "+filename+".combo")
            self.messageLabel02.setText(" ")
            self.messageLabel03.setText(" ")
    def loadAllcombos(self):
        filename, type = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '', 'Combo-files (*.combo)')
        if filename is not None and len(filename)>0:
            contents = open(filename, "r").read()
            combos = contents.split("\n")
            self.noofweeks = len(combos[0].split(" "))/7
            if self.noofweeks.is_integer():
                self.shiftseries = combos
                self.messageLabel01.setText("Combinations loaded from:")
                self.messageLabel02.setText(filename+".combo")
                self.messageLabel03.setText("Number of weeks: "+str(self.noofweeks))
                self.afterworkIntValue = 0
                self.afterworkvisibleinvisible(True)
                self.updateafterworkInt()
                self.afterworkSlide.setValue(self.afterworkIntValue)
                self.afterworkInt.setValue(self.afterworkIntValue)
                self.afterworkSlide.setRange(0,len(self.shiftseries)-1)
                self.afterworkInt.setRange(0,len(self.shiftseries)-1)
            else:
                self.messageLabel01.setText("Error: Could not load "+filename+".combo, data corrupt.")
                self.messageLabel02.setText("Number of days per week is not 7.")
                self.messageLabel03.setText(" ")
    def createAllShiftPossibilities(self,iterable, r): # <-- Where the actual magic happens
        noConstraints = 1
        shiftseries = []
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return 0, 0
        indices = list(range(r))
        item1 = ["0"] * (self.noofweeks*7)
        for ind in tuple(pool[i] for i in indices):
            item1[ind] = "1"
        appendflag = True # Reset for each combination
        appendflag = self.freedaysweeklycheck(appendflag,item1)
        appendflag = self.checkifallshiftsfilled(appendflag,item1)
        if appendflag == True:
            shiftseries.append(" ".join(item1))
        lp = True
        while lp == True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                lp = False
            if lp == True:
                indices[i] += 1
                for j in range(i+1, r):
                    indices[j] = indices[j-1] + 1
                item1 = ["0"] * (self.noofweeks*self.workingdays)
                for ind in tuple(pool[i] for i in indices):
                    item1[ind] = "1"
                appendflag = True # Reset for each combination
                appendflag = self.checkifallshiftsfilled(appendflag,item1) # check if all shifts are filled before adding the non-workdays for lists with less than 7 workdays per week
                if appendflag == True:
                    if self.workingdays < 7:
                        itemSerie2 = []
                        itemSerie1 = [item1[i * self.workingdays:(i + 1) * self.workingdays] for i in range((len(item1) + self.workingdays - 1) // self.workingdays )]
                        for items in itemSerie1:
                            for n1 in items:
                                itemSerie2.append(n1)
                            for n2 in range(7-self.workingdays):
                                itemSerie2.append("0")
                        item1 = itemSerie2
                appendflag = self.freedaysweeklycheck(appendflag,item1)
                noConstraints += 1
                if appendflag == True:
                    shiftseries.append(" ".join(item1))

        return shiftseries, noConstraints
    def checkifallshiftsfilled(self,appendflag,item1): # Just a constraint that must be fulfilled
        day = 0
        cycleseries = []
        weekseries = []
        for m in range(len(item1)):
            weekseries.append(item1[m])
            day += 1
            if day > self.workingdays-1:
                day = 0
                cycleseries.append(weekseries)
                weekseries = []
        cyclecheck = []
        for a in range(self.workingdays):
            cyclecheck.append(0)
        for a in cycleseries:
            for b in range(len(a)):
                cyclecheck[b] = cyclecheck[b] + int(a[b])
        for m in cyclecheck:
            if m < self.shifttype:
                appendflag = False
        return appendflag
    def freedaysweeklycheck(self,appendflag,item1): # Just another constraint that must be fulfilled
        noOnes = 0 # check so that number of free days over 7 day periods rule is followed.
        item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
        for m in range(len(item1)-7,len(item1)):
            item2.append(item1[m])
        for m in range(len(item1)):
            item2.append(item1[m])
        for item in item2:
            if item == "1":
                noOnes += 1
            elif item == "0":
                noOnes = 0
            if noOnes > 7-self.freedaysover7days:
                appendflag = False
        return appendflag
    def updateafterworkInt(self):
        try:
            activeSeries = self.shiftseries[self.afterworkIntValue].split(" ")
            self.afterweeksvisible(True)
        except:
            activeSeries = []
            self.afterweeksvisible(False)
        self.activeSeries = []
        for s in activeSeries:
            self.activeSeries.append(int(s))
        self.activeSeriesSerie = []
        n = 0
        activeSerie = []
        for m in self.activeSeries:
            n += 1
            activeSerie.append(m)
            if n == self.workingdays:
                self.activeSeriesSerie.append(activeSerie)
                activeSerie = []
                n = 0
        self.afterweekslabels()
    def shiftLabelsClicked(self):
        self.shiftLabel1 = self.shiftLabel1Edit.text()
        self.shiftLabel2 = self.shiftLabel2Edit.text()
        self.shiftLabel3 = self.shiftLabel3Edit.text()
    def runPhaseTwo(self):
        final = " / ".join(str([self.activeSeries[i * 7:(i + 1) * 7] for i in range((len(self.activeSeries) + 6) // 7 )]).split("[[")[1].split("]]")[0].split("], [")).replace(',', '')
        shifts0 = [self.shiftLabel1, self.shiftLabel2, self.shiftLabel3]
        shifts = ""
        for n in range(self.shifttype):
            shifts = shifts + " '" + str(shifts0[n]) + "'"
        os.system("python3 phase2.py '"+str(self.shifttype)+"' "+shifts+" "+str(final)+" &")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Dialog()
    window.show()
    sys.exit(app.exec_())
