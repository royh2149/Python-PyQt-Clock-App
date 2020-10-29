from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from Alarm import Alarm


class Updater(QDialog):
    def __init__(self):
        super().__init__()  # run superclass' constructor
        self.setWindowTitle("Enter Credentials")  # set title
        self.setGeometry(300, 200, 400, 400)  # set dimensions
        self.setWindowIcon(QIcon("images/favicon.ico"))  # add an icon

        self.info = []  # info to change list
        color = "blue"  # label color

        buttons = QGroupBox()  # group of the buttons
        h1 = QHBoxLayout()  # buttons layout

        time = QPushButton("Time")  # change time button
        time.clicked.connect(self.setup_time)  # connect the button to the right method

        name = QPushButton("Name")  # change name button
        name.clicked.connect(self.setup_name)  # connect the button to the right method

        repeat = QPushButton("Repeat")  # change repetition button
        repeat.clicked.connect(self.setup_repeat)  # connect the button to the right method

        sound = QPushButton("Sound")  # change sound button
        sound.clicked.connect(self.setup_sound)  # connect the button to the right method

        # add buttons to layout
        h1.addWidget(time)
        h1.addWidget(name)
        h1.addWidget(repeat)
        h1.addWidget(sound)
        buttons.setLayout(h1)  # add layout to groupBox
        buttons.setTitle("Choose attribute to change".title())

        v1 = QVBoxLayout()  # main layout

        # main label
        self.l = QLabel("<font color={}><b><u>Choose a property to edit. When you are done, click 'Close'</u></b><font>".format(color))

        v1.addWidget(self.l)  # add main label to layour

        v1.addWidget(buttons)  # add the buttons to the layout

        temp = QLabel()  # default label

        # setup facilities to substitute widgets on runtime
        self.section = QWidget()
        layout1 = QVBoxLayout(self.section)
        self.section.layout().addWidget(temp)
        v1.addWidget(self.section)

        self.cur = temp  # current showing widget variable

        self.ok = QPushButton("CLOSE")  # close button
        self.ok.clicked.connect(self.quit_win)  # connect close button to the appropriate method

        v1.addWidget(self.ok)  # add close button to layout

        self.setLayout(v1)  # set dialog's layout

    def quit_win(self):
        self.close()  # close the dialog
        return self.info  # return list of changes reuested

    def setup_time(self):

        id = QSpinBox()  # the matching id
        hours = QSpinBox()  # the hours
        minutes = QSpinBox()  # the minutes

        # explain to the user where to enter data
        l1 = QLabel("hours:")
        l2 = QLabel("minutes:")
        l3 = QLabel("id:")

        # "commit changes" button
        when_done = QPushButton("DONE")
        when_done.clicked.connect(lambda: self.up1(hours.text(), minutes.text(), id.text()))

        # create the layout with the field updaters
        h = QHBoxLayout()
        h.addWidget(l1)
        h.addWidget(hours)
        h.addWidget(l2)
        h.addWidget(minutes)
        h.addWidget(l3)
        h.addWidget(id)
        h.addWidget(when_done)

        # setup widgets in the appropriate location
        new_box = QGroupBox()
        new_box.setLayout(h)
        self.cur.deleteLater()
        self.section.layout().addWidget(new_box)
        self.cur = new_box

    def setup_name(self):
        inp = QLineEdit()  # new name
        id = QSpinBox()  # the matching id

        # explain to the user where to enter data
        l1 = QLabel("name:")
        l2 = QLabel("id:")

        # "commit changes" button
        when_done = QPushButton("DONE")
        when_done.clicked.connect(lambda: self.up2(inp.text(), id.text()))

        # create the layout with the field updaters
        h = QHBoxLayout()
        h.addWidget(l1)
        h.addWidget(inp)
        h.addWidget(l2)
        h.addWidget(id)
        h.addWidget(when_done)

        # setup widgets in the appropriate location
        new_box = QGroupBox()
        new_box.setLayout(h)
        self.cur.deleteLater()
        self.section.layout().addWidget(new_box)
        self.cur = new_box



    def setup_repeat(self):
        inp = QComboBox()  # new repeat
        inp.addItems(Alarm.reps)

        id = QSpinBox()  # the matching id

        # explain to the user where to enter data
        l1 = QLabel("repeat:")
        l2 = QLabel("id:")

        # "commit changes" button
        when_done = QPushButton("DONE")
        when_done.clicked.connect(lambda: self.up3(Alarm.reps[inp.currentIndex()], id.text()))

        # create the layout with the field updaters
        h = QHBoxLayout()
        h.addWidget(l1)
        h.addWidget(inp)
        h.addWidget(l2)
        h.addWidget(id)
        h.addWidget(when_done)

        # setup widgets in the appropriate location
        new_box = QGroupBox()
        new_box.setLayout(h)
        self.cur.deleteLater()
        self.section.layout().addWidget(new_box)
        self.cur = new_box

    def setup_sound(self):
        self.select_file = QPushButton("Select sound")
        self.select_file.clicked.connect(self.openFileNameDialog)

        id = QSpinBox()  # the matching id

        # explain to the user where to enter data
        l1 = QLabel("sound:")
        l2 = QLabel("id:")

        # "commit changes" button
        when_done = QPushButton("DONE")
        when_done.clicked.connect(lambda: self.up4(id.text()))

        # create the layout with the field updaters
        h = QHBoxLayout()
        h.addWidget(l1)
        h.addWidget(self.select_file)
        h.addWidget(l2)
        h.addWidget(id)
        h.addWidget(when_done)

        # setup widgets in the appropriate location
        new_box = QGroupBox()
        new_box.setLayout(h)
        self.cur.deleteLater()
        self.section.layout().addWidget(new_box)
        self.cur = new_box

    def up1(self, hours, minutes, id):
        self.info.append(("time", hours, minutes, id))  # append to list of changes
        print(self.info)

    def up2(self, name, id):
        self.info.append(("name", name, id))  # append to list of changes
        print(self.info)

    def up3(self, rep, id):
        self.info.append(("a_repeat", rep, id))  # append to list of changes
        print(self.info)

    def up4(self, id):
        self.fileName = self.fileName.split("/")[-1]
        if self.fileName and self.fileName.split(".")[-1] == "wav":
            filename = self.fileName
        else:
            filename = "default"
        self.info.append(("sound", filename, id))  # append to list of changes
        print(self.info)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Updater()  # create the object
    win.show()  # run the dialog

    sys.exit(app.exec_())



