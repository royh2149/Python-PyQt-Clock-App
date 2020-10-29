from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime
import threading
import Stopwatch
from Alarm import Alarm
from AlarmInfo import AlarmInfo
from Deleter import Deleter
import mysql.connector
from Timer import Timer
import sys
from Updater import Updater


# import necessary modules


def setup_image(obj):
    img = QLabel()

    img.setGeometry(QRect(300, 100, 128, 128))  # set image dimensions
    img.setAlignment(Qt.AlignCenter)  # align to center
    img.setText("")
    img.setScaledContents(True)
    img.setObjectName(obj)
    img.setPixmap(QPixmap('images/clock.jpeg'))  # add the image file

    return img  # return the created image label


def trunc(string) -> (int, int):  # a function that returns (begin,end) indexes of first digits in string
    beg = None
    end = None
    for i, char in enumerate(string):
        if char in '0123456789':
            if beg is None:
                beg = int(i)
        elif beg is not None:
            end = int(i)
            break

    return (beg, end)


def findnum(string) -> int:
    ret = 0
    for ind, c in enumerate(string):
        if c in "0123456789":
            while c in "0123456789":
                ret = 10 * ret + int(c)
                ind += 1
                c = string[ind]
            break

    return ret



class UI(QWidget):
    stw = 0  # stopwatch status variable
    timer = 0  # timer status
    is_alarm_available = 0  # indicates whether database is available

    colors = ["red", "blue", "green", "purple", "pink", "yellow", "gray", "orange"]  # common text colors list
    stw_default = "00:00:00"  # stopwatch default text
    timer_default = "00:00:00"  # timer default text
    ids = []  # listed alarms ids
    listed = []  # alarms labels

    closest = None  # closest alarm variable
    cur_timer = None  # current timer variable

    def __init__(self):  # init method

        super().__init__()  # execute QWidget.__init__() method

        try:  # try to connect to the alarms database
            mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="passwd",
                database="clocks"
            )

            print("HEY")

            UI.is_alarm_available = 1
        except:
            print("Database not available")  # leave alarms listing empty if database not available

        self.measure = Stopwatch.Stopwatch(0)  # stopwatch variable

        self.setWindowTitle("Clock")  # set window title
        self.setGeometry(300, 200, 400, 400)  # setup window dimensions
        self.setWindowIcon(QIcon("images/favicon.ico"))  # add an icon

        self.tabs = QTabWidget()  # tab hosting widget

        self.tab1 = QWidget()  # clock tab
        self.tab2 = QWidget()  # alarms tab
        self.tab3 = QWidget()  # stopwatch tab
        self.tab4 = QWidget()  # timer tab

        self.setup_tabs_layouts()  # setup tabs

        # add tabs to window
        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        self.setLayout(vbox)



        self.update_all()  # run the updating thread

    def setup_tabs_layouts(self):
        # create basic layouts for each tab
        self.tab1.layout = QGridLayout()
        self.tab2.layout = QGridLayout()
        self.tab3.layout = QGridLayout()
        self.tab4.layout = QGridLayout()

        self.tab1.layout.setColumnStretch(1, 4)
        self.tab1.layout.setColumnStretch(2, 4)
        self.tab2.layout.setColumnStretch(1, 4)
        self.tab2.layout.setColumnStretch(2, 4)
        self.tab3.layout.setColumnStretch(1, 4)
        self.tab3.layout.setColumnStretch(2, 4)
        self.tab4.layout.setColumnStretch(1, 4)
        self.tab4.layout.setColumnStretch(2, 4)

        #######
        # clock tab
        self.setup_clock_tab()

        ########
        # alarm tab
        if UI.is_alarm_available == 1:
            self.setup_alarm_tab()
            # if database is available, list the alarms and determine the closest one
            self.list_alarms()
            self.determine_closest_alarm(0)

        #########
        # stopwatch tab
        self.setup_stopwatch_tab()

        #########
        # timer tab
        self.setup_timer_tab()

        # set the layouts
        self.tab1.setLayout(self.tab1.layout)
        self.tab3.setLayout(self.tab3.layout)
        self.tab4.setLayout(self.tab4.layout)

        # add tabs to main window
        self.tabs.addTab(self.tab1, "Clock")

        if UI.is_alarm_available == 1:  # add the tabs only if database is available
            self.tab2.setLayout(self.tab2.layout)
            self.tabs.addTab(self.tab2, "Alarm")

        self.tabs.addTab(self.tab3, "Stopwatch")
        self.tabs.addTab(self.tab4, "Timer Countdown")



    def show_time(self):  # update time on clock
        # get current time
        time = datetime.now()
        s = ""

        # add the hour
        if time.hour < 10:
            s += "0" + str(time.hour)
        else:
            s += str(time.hour)

        s += ":"  # hour/minute separator

        # add the minute
        if time.minute < 10:
            s += "0" + str(time.minute)
        else:
            s += str(time.minute)

        s += ":"  # minute/second separator

        # add the second
        if time.second < 10:
            s += "0" + str(time.second)
        else:
            s += str(time.second)

        color = UI.colors[self.choose_color.currentIndex()]  # pick the chosen color
        text = "<font color={}><u>{}</u></font>".format(color, s)  # create the text string
        self.l1.setText(text)  # set right text
        self.l1.setFont(QFont("Arial", 128, QFont.Bold))  # make the text big and bold

    def update_all(self):  # update function
        threading.Timer(1.0, self.update_all).start()  # run the method every second
        self.show_time()  # update current time

        if UI.stw == 1:  # if stopwatch is active, update the content
            self.measure.seconds += self.measure.status
            self.l2.setText(self.measure.toString())

        # if the timer is active, update the content
        if UI.timer == 1:
            self.timer_label.setText("<font color=blue>{}</font>".format(UI.cur_timer.toString()))
            if UI.cur_timer.seconds == 0:  # if timer is finished, change the status and notify the user
                UI.timer = 0
                UI.cur_timer.fire()
            else:
                UI.cur_timer.seconds -= 1  # update timer if there is time left

        if UI.closest is not None and UI.closest.is_now():  # if the closest alarm is now
            temp = UI.closest
            self.determine_closest_alarm(5)  # determine **next** closest alarm
            print("FIRING ALARM " + temp.name)
            temp.go()  # fire the alarm

    def setup_clock_tab(self):
        # setup image
        img1 = setup_image("img1")
        img1.setPixmap(QPixmap("images/clock.jpeg"))
        img1.setFixedSize(128, 128)

        self.l1 = QLabel()  # main time label

        # setup color picking combobox
        self.choose_color = QComboBox()
        self.choose_color.addItems(UI.colors)
        self.choose_color.setToolTip("Choose font color")
        self.choose_color.setFixedWidth(70)

        # add widgets to layout
        self.tab1.layout.addWidget(img1, 0, 1)
        self.tab1.layout.addWidget(self.choose_color, 0, 2)
        self.tab1.layout.addWidget(self.l1, 3, 2)

    def setup_alarm_tab(self):
        # setup alarm image
        img2 = setup_image("img2")
        img2.setPixmap(QPixmap("images/alarm.png"))
        img2.setFixedSize(128, 128)

        # new alarm button
        self.add_alarm = QPushButton("+")
        self.add_alarm.clicked.connect(self.create_alarm)

        # delete alarm button
        self.remove_alarm = QPushButton("-")
        self.remove_alarm.clicked.connect(self.delete_alarm)

        # modify alarm button
        self.edit_alarm = QPushButton("*")
        self.edit_alarm.clicked.connect(self.update_alarm)

        # scroller for alarm labels
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # show vertical scrollbar only if necessary
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # show horizontal scrollbar only if necessary
        scroll.setWidgetResizable(True)

        # setup alarms labels environment
        self.alarms = QVBoxLayout()
        group = QGroupBox()
        group.setLayout(self.alarms)
        group.setTitle("Your Alarms")
        scroll.setWidget(group)

        # group the buttons
        buttons = QGroupBox()
        h1 = QHBoxLayout()
        h1.addWidget(self.edit_alarm)
        h1.addWidget(self.remove_alarm)
        h1.addWidget(self.add_alarm)
        buttons.setLayout(h1)
        buttons.setTitle("Edit | Remove | Add")

        # add widgets to layout
        self.tab2.layout.addWidget(img2, 0, 0)
        self.tab2.layout.addWidget(buttons, 0, 2)
        self.tab2.layout.addWidget(scroll, 1, 1)

    def setup_stopwatch_tab(self):
        # setup alarm image
        img3 = setup_image("img3")
        img3.setPixmap(QPixmap("images/stopwatch.png"))
        img3.setFixedSize(128, 128)

        # stopwatch start button
        self.start_stopwatch = QPushButton("START")
        self.start_stopwatch.clicked.connect(self.run_stopwatch)

        # stopwatch lap button
        self.lap = QPushButton("LAP")
        self.lap.clicked.connect(self.lap_tapped)

        # stopwatch reset button
        self.reset = QPushButton("RESET")
        self.reset.clicked.connect(self.stw_reset)

        # stopwatch resume button
        self.resume = QPushButton("RESUME")
        self.resume.clicked.connect(self.stw_resume)

        # stopwatch pause button
        self.pause = QPushButton("PAUSE")
        self.pause.clicked.connect(self.stw_pause)

        # stopwatch time label
        self.l2 = QLabel("{}".format(UI.stw_default))
        self.l2.setFont(QFont("Arial", 128, QFont.Bold))
        self.l2.setStyleSheet("color: green")

        # laps display area
        self.laps = QTextEdit()
        self.laps.setReadOnly(True)
        # self.laps.setLineWrapMode(QTextEdit.)

        # make a groupbox for all the buttons
        buttons = QGroupBox()
        hbox = QHBoxLayout()

        # add the buttons
        hbox.addWidget(self.start_stopwatch)
        hbox.addWidget(self.reset)
        hbox.addWidget(self.pause)
        hbox.addWidget(self.resume)
        hbox.addWidget(self.lap)

        # set hbox to buttons' layout
        buttons.setLayout(hbox)

        # add widgets to layout
        self.tab3.layout.addWidget(img3, 0, 0)
        self.tab3.layout.addWidget(self.l2, 0, 1)
        self.tab3.layout.addWidget(buttons, 2, 1)
        self.tab3.layout.addWidget(self.laps, 3, 1)

    def setup_timer_tab(self):
        # setup timer image
        img4 = setup_image("img4")
        img4.setPixmap(QPixmap("images/timer.png"))
        img4.setFixedSize(128, 128)

        # timer main label
        self.timer_label = QLabel("<font color=blue>{}</font>".format(UI.timer_default))
        self.timer_label.setFont(QFont("Arial", 128, QFont.Bold))

        # setup hours spinner with appropriate minimum and maximum values
        self.hour_spinner = QSpinBox()
        self.hour_spinner.setMinimum(0)
        self.hour_spinner.setMaximum(99)

        # setup minutes spinner with appropriate minimum and maximum values
        self.minute_spinner = QSpinBox()
        self.minute_spinner.setMinimum(0)
        self.minute_spinner.setMaximum(59)

        # setup seconds spinner with appropriate minimum and maximum values
        self.second_spinner = QSpinBox()
        self.second_spinner.setMinimum(0)
        self.second_spinner.setMaximum(59)

        # create spin-boxes group
        group = QGroupBox()
        hbox = QHBoxLayout()
        hbox.addWidget(self.hour_spinner)
        hbox.addWidget(self.minute_spinner)
        hbox.addWidget(self.second_spinner)
        hbox.setStretch(2, 2)
        group.setLayout(hbox)

        # make all spinners in the same size
        width = abs(self.timer_label.width()) / 3
        self.minute_spinner.setFixedWidth(width)
        self.hour_spinner.setFixedWidth(width)
        self.second_spinner.setFixedWidth(width)

        # start button
        start = QPushButton("Start!")
        start.clicked.connect(self.start_timer)

        # stop button
        stop = QPushButton("Stop!")
        start.clicked.connect(self.stop_timer)

        # buttons groupbox
        vbox = QVBoxLayout()
        vbox.addWidget(start)
        vbox.addWidget(stop)
        group1 = QGroupBox()
        group1.setLayout(vbox)

        # timer title input box
        title = QGroupBox()
        hbox1 = QHBoxLayout()
        label = QLabel("Set Timer Title:")
        self.timer_title = QLineEdit()  # input field for timer name
        hbox1.addWidget(label)
        hbox1.addWidget(self.timer_title)
        title.setLayout(hbox1)

        # add widgets to layout
        self.tab4.layout.addWidget(img4, 0, 0)
        self.tab4.layout.addWidget(title, 0, 2)
        self.tab4.layout.addWidget(self.timer_label, 1, 2)
        self.tab4.layout.addWidget(group, 2, 2)
        self.tab4.layout.addWidget(group1, 1, 3)

    def run_stopwatch(self):
        self.measure = Stopwatch.Stopwatch(0)
        self.start_stopwatch.setEnabled(False)  # disable "start" clicking option
        self.laps.setText("")  # reset laps
        self.l2.setText(self.measure.toString())
        UI.stw = 1  # change stopwatch status

    def stw_reset(self):
        self.start_stopwatch.setEnabled(True)  # enable "start" clicking option
        UI.stw = 0  # change stopwatch status
        self.measure.seconds = 0  # reset stopwatch
        self.l2.setText(UI.stw_default)  # retrieve default stopwatch label
        self.laps.setText("")  # clear laps

    def stw_resume(self):
        UI.stw = 1  # change stopwatch status
        self.measure.status = 1  # continue the counting

    def stw_pause(self):
        UI.stw = 0
        self.measure.pause()

    def create_alarm(self):
        info_win = AlarmInfo()
        info_win.exec_()  # launch alarm details input window
        self.determine_closest_alarm(0)  # maybe the new alarm is the closest one
        self.list_alarms()  # list the new alarm

    def lap_tapped(self):
        time = self.measure.toString()  # convert the lap to string
        self.measure.laps += time  # add the lap to stopwatch's list
        self.laps.setText(self.laps.toPlainText() + "\n" + time)  # add current lap to the lap QTextArea

    def list_alarms(self):
        db = mysql.connector.connect(  # connect to the MySQL database
            host="localhost",
            user="root",
            passwd="passwd",
            database="clocks"
        )

        data = []  # store the current alarms

        cursor = db.cursor()  # used to execute MySQL queries

        cursor.execute("SELECT * FROM alarms")  # get all current alarms
        for x in cursor:
            data.append(x)

        for elem in data:  # list all alarms
            if elem[4] not in UI.ids:  # convert alarm to label only if it does not already appear
                label = QLabel(UI.tuple_to_string(elem))  # convert to string
                label.setFont(QFont("Arial", 16, QFont.Bold))  # setup font
                self.alarms.addWidget(label)  # add the label
                UI.listed.append(label)  # store the label
                UI.ids.append(elem[4])  # in next times, add only alarms that are not listed yet

    def delete_alarm(self):
        win = Deleter()
        win.exec_()  # launch alarm deleting dialog
        rem = win.quit_win()  # receive the alarm ID that needs to be removed

        db = mysql.connector.connect(  # connect to the MySQL database
            host="localhost",
            user="root",
            passwd="passwd",
            database="clocks"
        )

        cursor = db.cursor()  # to run the query

        cursor.execute("DELETE FROM alarms WHERE id={}".format(rem))  # delete the corresponding alarm
        db.commit()  # commit the changes made

        for i in range(len(UI.listed)):  # remove the corresponding label
            if findnum(UI.listed[i].text().split("    ")[-1]) != rem:  # find the right ID
                continue
            UI.listed[i].setParent(None)

    def update_alarm(self):  # change certain properties of alarms
        win = Updater()  # create the needed dialog
        win.exec_()  # run the dialog
        info = win.quit_win()  # after dialog is closed, receive the list of requested changes

        db = mysql.connector.connect(  # connect to database
            host="localhost",
            user="root",
            passwd="passwd",
            database="clocks"
        )

        cursor = db.cursor()  # create the cursor in order to interact with the database

        for item in info:  # iterate through the changes requested
            if item[0] == "time":  # check if the attribute requested is time
                _id = item[3]
                cursor.execute("SELECT time FROM alarms WHERE id = {}".format(item[3]))  # get the right alarm

                for i in cursor:
                    cur_time = i[0]  # take current time
                    new_time = cur_time.replace(hour=int(item[1]),
                                                minute=int(item[2]))  # change the time based on the user's input

                    query = "UPDATE alarms SET time = '{}' WHERE id={}".format(new_time, _id)  # update query
                    cursor.execute(query)  # execute the query that updates the time
                    db.commit()  # commit the changes to the database

            else:  # what to do to any other attribute
                _id = item[2]

                # update the corresponding property bases on the user's inout
                query = "UPDATE alarms SET {} = '{}' WHERE id={}".format(item[0], item[1], item[2])
                cursor.execute(query)  # execute the query that updates the attribute
                db.commit()  # commit the changes to the database

        # re-list alarms
        for label in UI.listed:  # remove all labels
            label.setParent(None)

        UI.ids = []  # reset listed ids list
        UI.listed = []  # reset labels list
        self.list_alarms()  # re-list the alarms
        self.determine_closest_alarm(0)  # redetermine closest alarm, because it might have been changed now

    @staticmethod
    def tuple_to_string(elem):
        # get the info
        name = elem[0]
        mins = elem[1].minute
        hours = elem[1].hour
        rep = elem[2]
        sound = elem[3].replace("_", " ")

        time = ""
        if (hours < 10):
            time += "0" + str(hours) + ":"
        else:
            time += str(hours) + ":"

        if (mins < 10):
            time += "0" + str(mins)
        else:
            time += str(mins)

        # create the string in order to create the sufficing label
        s = "<b><font color=red>" + time + "</font>    <font color=blue>" + name + "</font>    <font color=black>" + rep + "</font>    <font color=purple>" + sound + "</font>    <font color=grey>" + str(
            elem[4]) + "</font></b>"
        return s

    def determine_closest_alarm(self, state):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="passwd",
            database="clocks"
        )

        listed = []

        cursor = db.cursor()

        cursor.execute("SELECT * FROM alarms")
        for x in cursor:  # each x is a tuple
            if UI.closest is None:
                UI.closest = Alarm(x[0], x[1], x[2], x[3], 4)

            cur = Alarm(x[0], x[1], x[2], x[3], 4)

            if state == 5:
                if cur.is_now():
                    continue

            if cur.is_sooner(UI.closest) or UI.closest.is_now():
                UI.closest = cur

        print(UI.closest.name)

    def stop_timer(self):
        pass

    def start_timer(self):
        hours = self.hour_spinner.value()
        mins = self.minute_spinner.value()
        secs = self.second_spinner.value()

        # fire error messageBox due to invalid timer values
        if secs == 0 and mins == 0 and hours == 0:
            msg = QMessageBox()
            msg.setWindowTitle("INVALID INPUT")
            msg.setText("Timer cannot be for 0 seconds long!")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Close)

            msg.setDefaultButton(QMessageBox.Close)

            msg.exec_()
            return

        UI.cur_timer = Timer(secs + mins * 60 + hours * 3600, self.timer_title.text())
        UI.timer = 1  # indicate that a timer is running
