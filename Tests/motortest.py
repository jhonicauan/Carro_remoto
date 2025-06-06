from Components.Motor import Motor
import time

motor = Motor(5,6,13)

motor.forward(50)
time.sleep(5)
motor.stop()
time.sleep(5)
motor.backward(50)
time.sleep(5)
