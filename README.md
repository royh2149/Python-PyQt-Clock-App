# Python-PyQt-Clock-App
This is a clock application created with PyQt5 uing MYSQL database. It features:
 - Clock
 - Alarm
 - Stopwatch
 - Timer
 
# Requirements
  - MYSQL server or docker
  - python3
  - PyQt5
  
# Instructions
  - Clone the Repo
  - Create a MYSQL docker: docker run --name server -p 3306:3306 -e MYSQL_ROOT_PASSWORD=passwd -d mysql:5.6
  - Move to the created directory
  - python3 App.py
  
  tested on Linux.
  to run from anywhere, edit /home/your-user/.bashrc and insert the line: alias myclock='S=$(pwd); cd /path/to/my_alarm; python3 App.py; cd $S'
  
*if you have copyrights on one of the images/sounds, please contact me*


