import RPi.GPIO as gpio
import time

in1 = 5
in2 = 6
ena = 13

gpio.setmode(gpio.BCM)

gpio.setup(in1,gpio.OUT)
gpio.setup(in2,gpio.OUT)
gpio.setup(ena,gpio.OUT)

pwm = gpio.PWM(ena,1000)

pwm.start(0)

while True:
    gpio.output(in1,gpio.HIGH)
    gpio.output(in2,gpio.LOW)
    pwm.ChangeDutyCycle(0)
