import RPi.GPIO as GPIO
import time
import subprocess
GPIO.setmode(GPIO.BCM)
button1=5
button2=6
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
while(1):
#     print(GPIO.input(button))
    if(GPIO.input(button1)==1):
        print("halt")
        subprocess.Popen("sudo halt",shell=True)
    if(GPIO.input(button2)==1):
        print("reboot")
        subprocess.Popen("sudo reboot",shell=True)
    time.sleep(.03)