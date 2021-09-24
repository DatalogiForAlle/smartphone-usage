from m5stack import lcd
from m5stack import axp
from m5stack import rtc
import machine
import imu
import fusion
import re

# Funktion til at placere en værdi på en skala fra aims_min til aims_max
def map_value(value, input_min, input_max, aims_min, aims_max):
    value = min(max(input_min, value), input_max)
    value_deal = (value - input_min) * (aims_max - aims_min) / (input_max - input_min) + aims_min
    return round(value_deal, 2)

# Tegner en tidslinje udfra de data der ligger gemt i data.csv filen
def showTimeline():
        lcd.clear(0x660000)
        fil = open('data.csv', 'r')
        lines = fil.readlines()
        fil.close()
        last_lines = lines[-160:]
        step = round(160/len(last_lines))       #bruges til at tegne tykkere søjler, ved få data
        print(step)
        if (step >= 3):                         # Step skal være højere end eller lig med 3, da en firkant som minimum har 1 pixel fyld og en kontur med en tykkelse på 1 pixel
            for i in range(len(last_lines)):
                line = last_lines[i][:-1]
                regex = r"\d+"
                if re.match(regex,line):
                    place = step * i
                    lcd.rect(place, 80-int(line), step, int(line), color=0x000000, fillcolor=0xFFFF00)
            lcd.text(10,10,"total time: " + str(len(last_lines)/2) + " minutes")
            return
        if (step < 4):                          #Når step er mindre end fire tegnes tidslinjen med almindelige linjer
            for i in range(len(last_lines)):
                line = last_lines[i][:-1]
                regex = r"\d+"
                if re.match(regex,line):
                    for n in range(step):
                        lcd.line(i+n, 80, i+n, 80-int(line), color=0xFFFF00)
            for i in range(len(last_lines)):            # En hvid streg der vises hver 20. minut
                if (i%40 ==0):
                    lcd.line(i, 80, i, 0, color=0xFFFFFF)
                    lcd.text(i,20,"20 min")
            lcd.text(10,10,"total time: " + str(len(last_lines)/2) + " minutes")

def appendData(data):
    fil = open('data.csv', 'a')
    fil.write(str(data)+"\n")
    fil.close()

def whipeData():
    fil = open('data.csv', 'w')
    fil.write("new\n")
    fil.close()

# Batteriindikator
def drawBattery(startx,starty):
    vol = axp.getBatVoltage()
    rel = map_value(vol, 3.6, 4.12, 0, 30)
    if (rel < 7):
        lcd.rect(startx,starty,int(rel),10,fillcolor=0xFF0000)
    if (rel >= 7):
        lcd.rect(startx,starty,int(rel),10,fillcolor=0x00FF00)
    lcd.rect(startx, starty, 30, 10, color=0xFFFFFF)
    lcd.rect(startx+30,starty+2,2,6,fillcolor=0xFFFFFF)

# en tegning af et øje
def drawEye(startx,starty):
    lcd.line(startx,starty,startx,starty + 40) #midten
    lcd.line(startx-7,starty+2,startx-7,starty + 38) # 1. venstre
    lcd.line(startx+7,starty+2,startx+7,starty + 38) # 1. højre
    lcd.line(startx-14,starty+4,startx-14,starty + 36)
    lcd.line(startx+14,starty+4,startx+14,starty + 36)
    lcd.line(startx-18,starty+10,startx-18,starty + 30)
    lcd.line(startx+18,starty+10,startx+18,starty + 30)
    lcd.ellipse(startx,starty+20,20,10, color=0x000000, fillcolor=0xFFFFFF);
    lcd.circle(startx,starty+20,8, color=0x0022FF, fillcolor=0x0022FF);
    lcd.circle(startx,starty+20,4, color=0x000000, fillcolor=0x000000);
