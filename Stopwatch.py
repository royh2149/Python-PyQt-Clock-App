from Counter import Counter


class Stopwatch(Counter):

    def __init__(self, start):
        super().__init__(start)
        self.laps = []  # laps storage
        self.status = 1  # on/off status

    def pause(self):
        self.status = 0  # indicate stopwatch is paused

    def f1(self):  # necessary because we inherit from an abstract class
        print("Stopwatch f1")

