# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # #                                                                                             # # # #
# # # #                    1/2/3-shift scheduling algorithm - Launcher:                             # # # #
# # # #                                                                                             # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                                 # # # #
# # # #                                                                                             # # # #
# # # #                             Automatic shift generator                                       # # # #
# # # #                                                                                             # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                                 # # # #
# # # #                                                                                             # # # #
# # # #   Author: Benjamin Bolling                                                                  # # # #
# # # #   Affiliation: European Spallation Source ERIC                                              # # # #
# # # #   Lund, Sweden                                                                              # # # #
# # # #   Initialization date: 2020-06-08                                                           # # # #
# # # #   Milestone 1 (phase 1, 0:s and 1:s generated):                               2020-06-29    # # # #
# # # #   Milestone 2 (phase 1 all working, proceeding to phase 2):                   2020-07-01    # # # #
# # # #   Milestone 3 (phase 2 all working, initial version ready):                   2020-07-03    # # # #
# # # #   Milestone 4 (phase 2 finished, solution finder implemented):                2020-07-03    # # # #
# # # #   Milestone 5 (abstracting functions, added check for solutions in phase1):   2021-01-09    # # # #
# # # #   Milestone 6 (Finalising full software, including a launcher):               2021-05-03    # # # #
# # # #                                                                                             # # # #
# # # #                                                                                             # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PyQt5.QtWidgets import QApplication,QCheckBox,QDialog,QDoubleSpinBox,QFileDialog,QGridLayout,QInputDialog,QMessageBox,QLabel,QLineEdit,QPushButton,QRadioButton,QSlider,QSpinBox,QWidget
from PyQt5.QtCore import Qt
from time import time
import sys, os

class DialogLauncher(QWidget):
    def __init__(self, parent=None):
        super(DialogLauncher, self).__init__(parent)
        self.setWindowTitle("Automatic Schedule Generator for Rotational Shift Work")
        self.createLayout()

    def createLayout(self):
        self.layout = QGridLayout(self)
        toplabel1 = QLabel("1-, 2- or 3-Shift Combinations Generator Algorithm.")
        toplabelx1 = QLabel("A Computational Approach to Generate Multi-Shift Rotational Workforce Schedules")
        toplabelx2 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        toplabel2 = QLabel("- - - -  Select what to launch  - - - -")
        toplabel3 = QLabel("")
        toplabel1.setAlignment(Qt.AlignCenter)
        toplabel2.setAlignment(Qt.AlignCenter)
        toplabel3.setAlignment(Qt.AlignCenter)
        toplabelx1.setAlignment(Qt.AlignCenter)
        toplabelx2.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(toplabel1, 0,0,1,7)
        self.layout.addWidget(toplabelx1, 1,0,1,7)
        self.layout.addWidget(toplabelx2, 2,0,1,7)
        self.layout.addWidget(toplabel2, 3,0,1,7)
        self.layout.addWidget(toplabel3, 4,0,1,7)

        self.newPhase1Btn = QPushButton("New")
        self.newPhase1Btn.clicked.connect(self.newPhase1)
        newPhase1BtnLbl = QLabel("New Combos from Template (phase 1)")

        self.loadPhase1Btn = QPushButton("Load Combos")
        self.loadPhase1Btn.clicked.connect(self.loadPhase1)
        loadPhase1BtnLbl = QLabel("Load Combos from file (phase 1)")

        self.loadPhase2Btn = QPushButton("Solve Combo")
        self.loadPhase2Btn.clicked.connect(self.loadPhase2)
        loadPhase2BtnLbl = QLabel("Load Combo into Solution Finder (phase 2)")

        self.layout.addWidget(self.newPhase1Btn, 5,0,1,1)
        self.layout.addWidget(newPhase1BtnLbl, 5,1,1,1)

        self.layout.addWidget(self.loadPhase1Btn, 6,0,1,1)
        self.layout.addWidget(loadPhase1BtnLbl, 6,1,1,1)

        self.layout.addWidget(self.loadPhase2Btn, 7,0,1,1)
        self.layout.addWidget(loadPhase2BtnLbl, 7,1,1,1)

        bottomlabel1 = QLabel("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        bottomlabel2 = QLabel("Coder: Benjamin Bolling (benjaminbolling@icloud.com)")

        self.setLayout(self.layout)

    def newPhase1(self):
        self.close()
        os.system("python src/phase1.py &")

    def loadPhase1(self):
        fn, type = QFileDialog.getOpenFileName(self, 'Open File', '', 'Combo-files (*.combo)')
        if fn:
            self.close()
            os.system("python src/phase1.py '{}' &".format(fn))

    def loadPhase2(self):
        fn, type = QFileDialog.getOpenFileName(self, 'Load File', "", "Text Files (*.sol)")
        if fn:
            self.close()
            os.system("python src/phase2.py '{}' &".format(fn))

    def getDirPath(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DialogLauncher()
    window.show()
    sys.exit(app.exec_())
