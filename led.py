import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(20,gpio.OUT)
gpio.setup(21,gpio.OUT)
gpio.output(20,False)
gpio.output(21,True)