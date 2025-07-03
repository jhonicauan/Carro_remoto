import RPi.GPIO as gpio
class Motor:
    def __init__(self,in1,in2,en):
        self.in1 = in1
        self.in2 = in2
        self.en = en
    
        gpio.setup(self.in1,gpio.OUT)
        gpio.setup(self.in2,gpio.OUT)
        gpio.setup(self.en,gpio.OUT)
        
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.LOW)
        self.pwm = gpio.PWM(en,500)
        self.pwm.start(0)
        
    def forward(self,speed):
             gpio.output(self.in1,gpio.HIGH)
             gpio.output(self.in2,gpio.LOW)
             self.pwm.ChangeDutyCycle(speed)
             
    def backward(self,speed):
             gpio.output(self.in1,gpio.LOW)
             gpio.output(self.in2,gpio.HIGH)
             self.pwm.ChangeDutyCycle(speed)
             
    def stop(self):
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.LOW)
        self.pwm.ChangeDutyCycle(0)