#!/usr/bin/python2.7
from __future__ import print_function
import os
import glob
import sys
import MySQLdb
import spidev
import RPi.GPIO as GPIO
import datetime
from datetime import time
from time import sleep
import time
import subprocess

board_type = sys.argv[-1]

global temp
global soll
soll = 17
global now

channels = [22, 18, 16, 15, 13, 11]
#           G25 G24 G23 G22 G27 G17

d = datetime

raum = "1214"

start = "6:30".split(":")
end = "17:00"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

i = 0
for pin in channels:
    if int(board_type) == 1 and i % 2 == 0:
        GPIO.setup(pin, GPIO.OUT)
    elif int(board_type) == 2 and i % 2 == 1:
         GPIO.setup(pin, GPIO.OUT)
    i = i + 1

GPIO.setup(7, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,1)

def get_adc(channel):
	GPIO.output(7, GPIO.HIGH)
        GPIO.output(7, GPIO.LOW)
        if channel == 0:
                res = spi.xfer([1,128,0])
        elif channel == 1:
                res = spi.xfer([1,144,0])
        if 0 <= res[1] <= 3:
                return ((((res[1] * 256) + res[2]) * 0.00322) * 3)

def display(adc_temp, adc_co2):        # function handles the display of #####
    global datetime
    global co2
    global temp
    temp = adc_temp * 5
    datetime = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:00"))
    co2 = adc_co2 * 200
    print (time.strftime("%H:%M:%S",time.localtime()),';',"{0:04f}".format(adc_temp),';', temp,';', "{0:04f}".format(adc_co2),';',co2)

def show_air_quality(co2):
    if co2 < 650:
        print("Gute Luft")


    elif co2 in range(800):
        print("Schlechtere Luftqualitaet")

    elif co2 > 1000:
        print("Fenster auf")

def write_data_to_db(temp,co2,datetime):
   print("writing data to DB...")
   try:
	conn = MySQLdb.connect(host="10.16.103.202",user="r1214",passwd="BGyPLrtGyVZG8Vyj",db="messung")
        cur = conn.cursor()
        sql = ("""INSERT INTO temp (room,temp,co2,soll) VALUES (%s,%s,%s,%s)""", (raum,round(temp, 1),round(co2, 1),round(soll, 1)))
	cur.execute(*sql)
   	conn.commit()
	conn.close()
   	print("write successful!")
   except:
	print("could not write data to DB")

def heizungAn():
    i = 0
    for pin in channels:
        if int(board_type) == 1 and i % 2 == 0:
            GPIO.output(pin, GPIO.HIGH)
        elif int(board_type) == 2 and i % 2 == 1:
            GPIO.output(pin, GPIO.HIGH)
        i = i + 1

def heizungAus():
    i = 0
    for pin in channels:
        if int(board_type) == 1 and i % 2 == 0:
            GPIO.output(pin, GPIO.LOW)
        elif int(board_type) == 2 and i % 2 == 1:
            GPIO.output(pin, GPIO.LOW)
        i = i + 1

def get_minutes(soll,temperatur):
    global minutes_aus
    minutes_aus = 5 * (temperatur - soll) + 6
    print("soll:",soll)
    if minutes_aus > 10:
        minutes_aus = 10
    elif minutes_aus < 0:
        minutes_aus = 0
    heizungAus()
    print(minutes_aus, "Minuten aus!")
    sleep(60 * round(minutes_aus))
    if 60 * (10 - round(minutes_aus)) > 30:
        heizungAn()
        sleep(60 * (10 - round(minutes_aus)))

def setSollTemperatur():
    global soll
    global end
    now = d.datetime.now().time()
    if d.datetime.now().strftime("%a") != "Sat" and d.datetime.now().strftime("%a") != "Sun":
        if raum != "1202":
            arr = subprocess.check_output(["curl", "--silent", "http://belegung.gemont.de"]).split("<br>")
            for room in arr:
                if room.split(";")[0] == raum:
                    if room.split(";")[1] == "-1" or room.split(";")[2] == "-1":
                        end = "17:00"
                    else:
                        end = room.split(";")[1] + ":" + room.split(";")[2]
        if d.time(int(start[0]),int(start[1])) <= now and now <= d.time(int(end.split(":")[0]),int(end.split(":")[1])):
            soll = 21
        else:
            soll = 17
    else:
        soll = 17

sleep(60 * 5 * (int(board_type)-1) + 30)

while True:
    setSollTemperatur()
    adc_temp = (get_adc(0))
    adc_co2 = (get_adc(1))
    display(adc_temp,adc_co2)
    write_data_to_db(temp,co2,datetime)
    show_air_quality(co2)
    get_minutes(soll,temp)
