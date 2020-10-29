import os
import datetime
import mysql.connector
import threading

# import necessary modules


class Alarm:

    reps = ['once', 'weekly', 'daily', 'allfs', 'never']  # available repetitions
    sounds = ["girls_like_you", "default", "sugar", "what_lovers_do"]  # available tracks

    # for "there is no attribute connect" error, install the python connector.
    # connect to the database
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="passwd",
            database="clocks"
        )

        cursor = db.cursor()
    except:
        print("Error Occured")

    def __init__(self, name, time, repeat, sound, num):  # constructor
        self.name = name
        self.time = time
        self.repeat = repeat
        self.sound = sound

        self.info_win = None

        if num == 0:  # allow the user to decide whether to add alarm to database or not
            self.addToDB()

    def set_repeat(self, rep):
        if rep in Alarm.reps:  # make sure repetition is a valid one
            self.repeat = rep
            return "Repetiton changed successfully to " + rep + "."
        return "Error in repetition type."

    def set_sound(self, new_sound):
        if new_sound in Alarm.sounds:  # make sure sound is a valid one
            self.sound = new_sound + ".wav"

    # def play_sounf(self):
    #     os.system("play " + self.sound)

    def addToDB(self):  # add the alarm to the database
        Alarm.cursor.execute("INSERT INTO alarms (name, time, a_repeat, sound) VALUES (%s, %s, %s, %s)", (self.name, self.time, self.repeat, self.sound))
        Alarm.db.commit()  # commit the changes caused by the query

    def is_before(self, other):  # returns true if time1 is before time2
        time1 = self.time.minute + self.time.hour * 60  # self minutes sum
        time2 = other.time.minute + other.time.hour * 60  # other minutes sum

        return time1 < time2  # true if self is before other

    def is_sooner(self, other):
        # get current time
        now = datetime.datetime.now()
        now = now.minute + now.hour * 60

        time1 = self.time.minute + self.time.hour * 60  # self time in minutes
        time2 = other.time.minute + other.time.hour * 60  # other time in minutes

        # determine how many minutes left to self alarm to ring
        if now > time1:  # in case time1 has already passed today
            diff1 = 60*60 - (now - time1)
        else:
            diff1 = time1 - now

        # determine how many minutes left to other alarm to ring
        if now > time2:  # in case time2 has already passed today
            diff2 = 60*60 - (now - time2)
        else:
            diff2 = time2 - now

        # return false if self will ring after the other
        # return true if self will ring sooner than other
        return not (diff1 > diff2)

    def is_now(self):  # return true if alarm is right now
        now = datetime.datetime.now()  # get current time

        return now.hour == self.time.hour and now.minute == self.time.minute  # check equivalence

    def go(self):
        # options: 'once', 'weekly', 'daily', 'allfs', 'never'
        if self.repeat == "never":
            return  # exit the function

        if self.repeat == "once":
            self.repeat = "never"  # preventing more rings
            self.ring()
            return

        # making sure it is the "right" day
        if self.repeat == "weekly" and self.time.weekday() == datetime.datetime.now().weekday():
            self.ring()
            return

        # making sure it is not friday or saturday
        if self.repeat == "allfs" and self.time.weekday() != 5 and self.time.weekday != 4:  # everyday except friday and saturday
            self.ring()
            return

        self.ring()  # in case repeat is daily

    def ring(self):  # run the alarmRinger
        print(self.name, self.sound)
        os.system("python3 AlarmRinger.py {} {}".format(self.name, self.sound))