import RPi.GPIO as GPIO
import time

# Configura��o do GPIO
servo_pin = 19  # GPIO 18 (pino f�sico 12)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Frequ�ncia de PWM para servo (50 Hz � comum para servos)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)  # Inicia com duty cycle 0

def set_angle(angle):
    # Convers�o simples: 0 graus -> 2.5% duty cycle, 180 graus -> 12.5% duty cycle
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Espera para o servo se mover

try:
    while True:
        print("Girando para 0 graus")
        set_angle(0)
        time.sleep(1)

        print("Girando para 90 graus")
        set_angle(90)
        time.sleep(1)

        print("Girando para 180 graus")
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("Encerrando programa")

finally:
    pwm.stop()
    GPIO.cleanup()
