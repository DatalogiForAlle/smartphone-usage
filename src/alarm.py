import imu
import time
import hat
import fusion


speaker = hat.get(hat.SPEAKER)
motion_sensor = imu.IMU()

filter = fusion.Fusion()

alarmstate = 0
timer = 0
total = 0

count = 0
while True:
    filter.update_nomag(motion_sensor.acceleration, motion_sensor.gyro)
    pitch = filter.pitch
    roll = filter.roll

    if count == 100:
        lcd.clear(0x000000)
        lcd.print(int(total/1000), lcd.CENTER, 10, color=0xff0000, transparent=True)
        count = 0
    count += 1

    print((pitch, roll, alarmstate, timer)) # pitch 48-62, roll: 65-85
    if 40 < pitch < 70 and 80 < roll < 110:
        timer += 10
        total += 10
        print("there")
        speaker.tone(1800, 10)
    else:
        time.sleep_ms(10)

    if alarmstate == 0:

        if  timer >= 3000:
            alarmstate = 1

    elif 1 <= alarmstate < 5:
        #speaker.tone(1800, 100)
        alarmstate += 1
    else:
        alarmstate = 0
        timer = 0
