from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Deleter(QDialog):
    def __init__(self):
        super().__init__()  # run superclass' constructor
        self.setWindowTitle("Choose Alarm to delete")  # set title
        self.setGeometry(300, 200, 400, 400)  # set dimensions
        self.setWindowIcon(QIcon("images/favicon.ico"))  # add window icon

        v1 = QVBoxLayout()  # main layout

        self.ok = QPushButton("SUBMIT")  # submit button
        self.ok.clicked.connect(self.quit_win)  # connect submit button to quit method

        color = "blue"  # label color

        self.l = QLabel("<font color={}><b><u>Select matching alarm number:</u></b><font>".format(color))  # create label

        self.inp = QSpinBox()  # specify alarm id to remove it

        # add widgets to layout
        v1.addWidget(self.l)
        v1.addWidget(self.inp)
        v1.addWidget(self.ok)

        self.setLayout(v1)  # set the window layout to the one we have just created

    def quit_win(self):  # close the dialog and return the alarm id to delete
        ret = self.inp.value()
        self.close()
        return ret
