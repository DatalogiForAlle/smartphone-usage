import imu
import time
import hat
import fusion


speaker = hat.get(hat.SPEAKER)
motion_sensor = imu.IMU()

filter = fusion.Fusion()


count = 0
while True:
    filter.update_nomag(motion_sensor.acceleration, motion_sensor.gyro)
    pitch = filter.pitch
    roll = filter.roll

    if count == 10:
        lcd.clear(0x000000)
        lcd.print(pitch, lcd.CENTER, 10, color=0xff0000, transparent=True)
        lcd.print(roll, lcd.CENTER, 30, color=0xff0000, transparent=True)
        count = 0
    count += 1

    #print((pitch, roll)) # pitch 25-80, roll: 50-140
    if 25 < pitch < 80 and 50 < roll < 140:
        speaker.tone(1800, 10)
        lcd.print("there", lcd.CENTER, 50, color=0xff0000, transparent=True)
    else:
        time.sleep_ms(10)
