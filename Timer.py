from Counter import Counter
import os

# import necessary modules


class Timer(Counter):
    def __init__(self, secs, title):
        self.seconds = secs  # current seconds passed
        self.title = title  # timer's title

    def fire(self):
        print(self.title + " is FIRING!")
        os.system("python3 TimerDialog.py {}".format(self.title))  # run the ringer with the timer's title

    def f1(self):  # needed because Counter is an abstract class
        pass