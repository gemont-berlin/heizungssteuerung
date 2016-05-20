import datetime
from datetime import time
import sys
from time import sleep
import subprocess
import os

raum = "1214"	# setze Raumnummer!
d = datetime

# jeweils 5 min am ende vor
stunden = [
        [d.time(8,40),d.time(8,45)],
        [d.time(9,25),d.time(9,30)],
        [d.time(10,30),d.time(10,35)],
        [d.time(11,15),d.time(11,20)],
        [d.time(12,25),d.time(12,30)],
        [d.time(13,35),d.time(13,40)],
        [d.time(14,30),d.time(14,35)],
        [d.time(15,25),d.time(15,30)]
]

try:
        print "room to be tested: " + raum
        print "fetching data from http://belegung.gemont.de"
        arr = subprocess.check_output(["curl", "--silent", "http://belegung.gemont.de"]).split("<br>")
except:
        print "Couldn't fetch the data from http://belegung.gemont.de"
for room in arr:
        if room.split(";")[0] == raum:
                print "room found!"
                now = d.time(d.datetime.now().hour, d.datetime.now().minute)
                print d.datetime.now().strftime("%H:%M:%S")
                if room.split(";")[1] == "-1":
			break
		if d.time(int(room.split(";")[1]), int(room.split(";")[2])) <= now and now <= d.time(int(room.split(";")[1]), int(room.split(";")[2])):
                        if d.datetime.now().strftime("%a") == "Mon" or d.datetime.now().strftime("%a") == "Thu" :
                                os.system("mpg123 -q stuehle-fenster.mp3 &")
                        else:
                                os.system("mpg123 -q fenster.mp3 &")
