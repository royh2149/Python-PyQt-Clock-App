from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
import sys

# import necessary modules


class AlarmRinger(QDialog):
    def __init__(self, name, song):
        super().__init__()
        self.setWindowTitle("Alarm On Fire!!!")  # setup title
        self.setGeometry(300, 200, 400, 400)  # setup dimensions
        self.setWindowIcon(QIcon("images/favicon.ico"))  # add window icon

        # instance properties
        self.name = name
        self.song = song

        v1 = QVBoxLayout()  # main layout

        self.ok = QPushButton("CLOSE")
        self.ok.clicked.connect(self.quit)  # connect the button to its action

        color = "blue"  # label color

        self.l = QLabel("<font color={}><b><u>{}</u></b><font>".format(color, name))  # main label - alarm name
        self.l.setFont(QFont("Arial", 64, QFont.Bold))  # enlarge text with Italic style
        self.l.setAlignment(Qt.AlignCenter)  # put it in the center

        # add widgets to layout
        v1.addWidget(self.l)
        v1.addWidget(self.ok)

        self.setLayout(v1)  # setup main layout

        # setup music facility
        filename = 'sounds/' + self.song
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(filename))

    def quit(self):
        self.close()  # close the window
        self.sound.stop()  # stop the music
        sys.exit(0)  # exit with "OK" status

    # override exec_ to always play music on startup
    def exec_(self):
        self.sound.play()
        super().exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # setup application

    song = sys.argv[-1]  # specify the song to be played
    name = ""

    # specify the "right" name - name with spaces gets counted as separated arguments
    for i in range(1, len(sys.argv)-1):
        name += sys.argv[i] + " "

    name = name[:-1]  # remove the last space

    win = AlarmRinger(name, song)  # initialize the object
    win.exec_()  # open the dialog and play the music

    sys.exit(app.exec_())



