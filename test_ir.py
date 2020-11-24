import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
BUZZER=21
G_LED=16
IR=12
R_LED=20
GPIO.setup(IR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
import time
while 1:
    print(GPIO.input(IR))
    if(GPIO.input(IR)==0):
        print('obstacle detect')
    else:
        print('No obstacle')
    time.sleep(.3)
