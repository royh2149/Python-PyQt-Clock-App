from PyQt5.QtWidgets import *
from UI import UI
import sys
import mysql.connector

# import necessary modules

try:  # try to connect to the alarms database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="passwd",
        database="clocks"
    )

    print("connected.")

    cursor = db.cursor()  # create the cursor used to interact with the database

    # the table creation query
    cursor.execute("CREATE TABLE IF NOT EXISTS alarms (name varchar(50) NOT NULL, time datetime NOT NULL, a_repeat varchar(6) NOT NULL , sound varchar(50) NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

except:
    print("Error connecting to Database. Alarm won't work")

def quit_all():
    print("QUIT ALL")
    sys.exit(0)

app = QApplication(sys.argv)  # main app
app.setQuitOnLastWindowClosed(True)


# gtk2=qt5ct-style is default in my OS - mint
app.setStyle("Fusion")  # Available styles: 'cleanlooks', 'gtk2', 'cde', 'motif', 'plastique', 'qt5ct-style', 'Windows', 'Fusion'

win = UI()  # setup main window

win.show()

ret = app.exec_()  # app exit code
app.quit()
print("jnje")
print(ret)
sys.exit(0)
print("QHAT")
