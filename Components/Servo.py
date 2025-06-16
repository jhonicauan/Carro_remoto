import RPi.GPIO as gpio
import time

class Servo:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        self.pwm = gpio.PWM(self.pin, 50)  # 50Hz = 20ms por ciclo
        self.pwm.start(0)
        self.current_angle = 90  # come�a centralizado

    def angle_to_duty(self, angle):
        # Mapeia o �ngulo (0-180) para um duty entre ~2.5% e ~12.5%
        return 2.5 + (angle / 180.0) * 10.0

    def set_angle(self, target_angle, step=1, delay=0.02):
        if target_angle < 0:
            target_angle = 0
        elif target_angle > 180:
            target_angle = 180

        if target_angle > self.current_angle:
            angles = range(self.current_angle, target_angle + 1, step)
        else:
            angles = range(self.current_angle, target_angle - 1, -step)

        for angle in angles:
            duty = self.angle_to_duty(angle)
            self.pwm.ChangeDutyCycle(duty)
            time.sleep(delay)

        self.pwm.ChangeDutyCycle(0)  # desliga o PWM para evitar jitter
        self.current_angle = target_angle
