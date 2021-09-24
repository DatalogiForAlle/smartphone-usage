from m5stack import lcd         #bibliotek til lcdskærm
from m5stack import axp
from m5stack import rtc
import machine
import imu
import fusion
from m5stack import btnA
from m5stack import btnB
import re
import f        #bibliotek med de selvskrevne funktioner

axp.setLcdBrightness(50)
rtc.setTime(0000, 00, 00, 00, 00, 00)
sensor = imu.IMU()
myfilter = fusion.MahonyFilter()
lcd.orient(lcd.LANDSCAPE)
state = "start"        #kan også startes i state = "monitor", så få man ikke mulighed for at slette data.
hit = 0
horisontalhit = 0   #en variable til at gemme de scalerede hits, så de kan vises på 160 pixels
verticalhit = 0     #en variable til at gemme de scalerede hits, så de kan vises på 80 pixels
lcd.clear(0x000000)
f.appendData(0)       #vigtigt at sikre datafilen ikke er helt tom
lcd.font(lcd.FONT_DefaultSmall)

while True:
    if (axp.getBatVoltage()<3.6):     #sikre at M5stickC ikke crasher kritisk, ved at slukke, ved lav batterispænding
        lcd.clear(0xFF0000)
        lcd.text(10,30,"Power low")
        lcd.text(10,30,"closing down")
        machine.lightsleep(10000)
        axp.powerOff()
    if state == "start":                # Startmenu
        lcd.text(10,10,"reset tryk B")
        lcd.text(10,40,"continue tryk A")
        if btnA.wasPressed():
            lcd.clear(0x000000)
            state = "monitor" #1
        if btnB.wasPressed():
            f.whipeData()
            lcd.clear(0x000000)
            lcd.text(10,10,"data er blevet slettet")
            lcd.text(10,40,"continue tryk A")
            state = "pause"
    if state == "monitor":              #overvågningens egentlige mototr
        f.drawBattery(10,60)            #batteriindikator, med x,y koordinat som input
        machine.lightsleep(100)         #selvom det ikke virker som meget, er det denne lightsleep der giver eksra batteritid
        year, month, day, hour, minute, second = rtc.now()
        lcd.text(10,2,"current running time: ")
        lcd.text(10,15, str(hour) + ":" + str(minute) + ":" + str(second))
        if (hour == 1 and minute > 20): #Stopper uret når det har kørt i 80 minutter.
            cd.clear(0xFF0000)
            lcd.text(10,30,"got enough info")
            lcd.text(10,30,"closing down")
            machine.lightsleep(10000)
            axp.powerOff()
        myfilter.update(sensor.acceleration, sensor.gyro)
        pitch = int(myfilter.pitch)
        roll = int(myfilter.roll)
        if 25 < pitch < 80 and 50 < roll < 140:        # Her afsløres mobilbrug! Insæt de fundne grænser for pitch og roll her
            hit += 1
            horisontalhit = int(f.map_value(hit,0,180,0,140))             # 180 er max antal hits, det skal skaleres så det kan tegns på 160 pixel, med en margin på 10 pixel
            lcd.rect(10,30,horisontalhit, 20, fillcolor=0x00FFFF)            # en idikator der vises på skærmen, så man kan se om den faktisk registrerer hits
            print(hit)
        if -71 < pitch < -40 and -10 < roll < 5:        # Creepy indslag - et øje der kigger på dig, hvis du kigger på M5stick!
            f.drawEye(120,25)
            machine.lightsleep(1000)
            lcd.clear(0x000000)
        if (second%30 == 0):         # gemme data hvert 30 sekund. Maximum antal hits på 30  sekunder: 180
            verticalhit = int(f.map_value(hit,0,180,0,80))             # 180 er max antal hits, det skal skaleres så det kan tegnes på 80 pixel
            f.appendData(verticalhit)
            hit = 0
            machine.lightsleep(1000)            #nødvendig at sikre der går et sekund så den ikke når at skrive dobbelt data
            lcd.clear(0x000000)
        if btnA.wasPressed():
            f.showTimeline()                # Knaptryk skifter til tidslinjevisning
            state = "pause"
    if state == "pause":
        if btnA.wasPressed():
            lcd.clear(0x000000)
            state = "monitor"
