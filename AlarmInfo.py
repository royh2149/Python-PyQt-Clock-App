from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime
from Alarm import Alarm
import os


class AlarmInfo(QDialog):

    def __init__(self):
        super().__init__()  # run superclass' constructor
        self.setWindowTitle("Enter Properties")  # set title
        self.setGeometry(300, 200, 400, 400)  # set dimensions
        self.setWindowIcon(QIcon("images/favicon.ico"))  # add an icon

        v1 = QVBoxLayout()  # main layout
        timing = QHBoxLayout()  # minutes, hours spinners layout

        h1 = QHBoxLayout()  # name layout
        h2 = QHBoxLayout()  # time layout
        h3 = QHBoxLayout()  # repetition layout
        h4 = QHBoxLayout()  # sound layout

        # labels
        l1 = QLabel("Name")
        l2 = QLabel("Time")
        l3 = QLabel("Repeat")
        l4 = QLabel("Sound")

        self.in1 = QLineEdit()  # name input
        self.c1 = QComboBox()  # repeat settings
        #self.c2 = QComboBox()  # sound settings
        # self.c2 = QFileDialog()
        # self.c2.setFileMode(QFileDialog.AnyFile)
        # self.c2.setFilter("Audio files (*.mp3, *.wav)")
        self.select_file = QPushButton("Select sound")
        self.select_file.clicked.connect(self.openFileNameDialog)
        self.in1.setMaxLength(50)  # name limitation matching varchar(50)

        self.c1.addItems(Alarm.reps)  # add repetitions options
        #self.c2.addItems(Alarm.sounds)  # add sound options

        # hours, minutes spinners
        self.hours_spinner = QSpinBox()
        self.minutes_spinner = QSpinBox()

        # set matching minimum and maximum values
        self.minutes_spinner.setMinimum(0)
        self.minutes_spinner.setMaximum(59)
        self.hours_spinner.setMaximum(23)
        self.hours_spinner.setMinimum(0)

        # add hours, minutes spinners to timing layout
        timing.addWidget(self.hours_spinner)
        timing.addWidget(self.minutes_spinner)

        submit = QPushButton("Submit")  # create submit button
        cancel = QPushButton("Cancel")  # create exit button

        submit.clicked.connect(self.add_alarm)  # connect submit to add_alarm method
        cancel.clicked.connect(self.exit_dialog)  # connect cancel to regular exit method

        # setup name label
        h1.addWidget(l1)
        h1.addWidget(self.in1)

        # setup time label
        h2.addWidget(l2)
        h2.addLayout(timing)

        # setup repetition label
        h3.addWidget(l3)
        h3.addWidget(self.c1)

        # setup sound label
        h4.addWidget(l4)
        h4.addWidget(self.select_file)

        # add sub-layouts to main layout
        v1.addLayout(h1)
        v1.addLayout(h2)
        v1.addLayout(h3)
        v1.addLayout(h4)
        v1.addWidget(submit)

        self.setLayout(v1)  # set window layout

    def exit_dialog(self):
        self.close()  # close the dialog

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)

    def add_alarm(self):
        name = self.in1.text()  # get name

        # get minutes and hours
        mins = int(self.minutes_spinner.value())
        hours = int(self.hours_spinner.value())
        cur = datetime.now()
        time = cur.replace(hour=hours, minute=mins)

        # get repetition and sound
        rep = Alarm.reps[self.c1.currentIndex()]
        #sound = Alarm.sounds[self.c2.currentIndex()]

        #print(self.c2.getOpenFileName(self, "Open File", '/', "Audio files (*.mp3 *.wav)"))
        self.fileName = self.fileName.split("/")[-1]
        if self.fileName and self.fileName.split(".")[-1] == "wav":
            filename = self.fileName
        else:
            filename = "default"

        new = Alarm(name, time, rep, filename, 0)  # in order to add the alarm to database

        self.close()  # close the dialog
