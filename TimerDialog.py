from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
import sys
from UI import setup_image


# import sounddevice as sd
# import soundfile as sf


class TimerDialog(QDialog):
    def __init__(self, title):
        super().__init__()  # run superclass' constructor
        self.setWindowTitle("Timer On Fire!!!")  # set title
        self.setGeometry(400, 300, 200, 250)  # set dimensions
        self.setWindowIcon(QIcon("images/favicon.ico"))  # add an icon

        layout = QVBoxLayout()  # main layout

        image = setup_image("image")  # create the image

        image.setPixmap(QPixmap("images/timer.png"))  # put matching image
        image.setFixedSize(128, 128)  # set fixed size

        image.setAlignment(Qt.AlignCenter)  # align the image to the center

        self.title = title

        # main label
        sub = QLabel("<font color=green><b>Timer finished:\n" + self.title + "</b></font>")
        sub.setAlignment(Qt.AlignCenter)  # align label to center

        exit_all = QPushButton("Close")  # create closing button
        exit_all.clicked.connect(self.after)  # connect closing button to the close method

        # add widgets to layout
        layout.addWidget(image)
        layout.addWidget(sub)
        layout.addWidget(exit_all)

        self.setLayout(layout)  # set dialog's layout

        filename = 'sounds/default.wav'  # music filename
        self.sound = QSoundEffect()  # sound player object
        self.sound.setSource(QUrl.fromLocalFile(filename))  # make the file a source to the sound player

    def exec_(self):  # override exec_ method
        self.sound.play()  # play the sound
        super().exec_()  # execute superclass' exec_

    def after(self):  # close function
        self.close()  # close the window
        self.sound.stop()  # stop the music
        sys.exit(0)  # exit with success code

    # def t1(self):
    #     filename = 'sounds/default.wav'
    #     # Extract data and sampling rate from file
    #
    #     data, fs = sf.read(filename, dtype='float32')
    #     sd.play(data, fs)
    #     #status = sd.wait()  # wait until the file is done playing


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = TimerDialog(sys.argv[1])  # the timer's title is the first argument
    win.exec_()  # run the dialog

    sys.exit(app.exec_())