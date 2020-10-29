from abc import ABC, abstractmethod # make counter class an abstract one


class Counter(ABC):

    SEPARATOR = ":"

    def __init__(self, secs):
        self.seconds = secs

    def toString(self):
        copy = self.seconds

        hour = copy // 3600  # determine hours
        copy -= hour * 3600  # remove hours

        minute = copy // 60  # determine minutes
        copy -= minute * 60  # remove minutes

        s = ""

        # add the hour
        if hour < 10:
            s += "0" + str(hour)
        else:
            s += str(hour)

        s += Counter.SEPARATOR    # hour/minute separator

        # add the minute
        if minute < 10:
            s += "0" + str(minute)
        else:
            s += str(minute)

        s += Counter.SEPARATOR   # minute/second separator

        # add the second
        if copy < 10:
            s += "0" + str(copy)
        else:
            s += str(copy)

        return s

    @abstractmethod
    def f1(self):
        print("This function makes the class an abstract one!")