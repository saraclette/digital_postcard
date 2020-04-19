import constant
import config
import logging
from threading import Lock

if config.USE_EFFECT:
  import RPI.GPIO as GPIO
  GPIO.setmode(GPIO.BOARD)       # Number GPIOs by physical location


trigger_effect_lock = Lock()

trigger_led_effect   = constant.STOP_COMMAND
trigger_motor_effect = constant.STOP_COMMAND


def led_effect_thread():
    global trigger_led_effect
    GPIO.setup(config.LED_PIN, GPIO.OUT)   # Set led_pin mode is output
    GPIO.output(config.LED_PIN, GPIO.LOW)  # Set led_pin to low(0V)

    p = GPIO.PWM(config.LED_PIN, 1000)     # set frequency to 1kHz
    p.start(0)                             # Duty Cycle = 0
    while True:
        time.sleep(constant.LED_UPDATE_DELAY)
        while trigger_led_effect == constant.START_COMMAND:
            for dc in range(0, 101, 4):   # Increase duty cycle: 0~100
                p.ChangeDutyCycle(dc)     # Change duty cycle
                time.sleep(0.05)
            time.sleep(1)
            for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
                p.ChangeDutyCycle(dc)
                time.sleep(0.05)
            time.sleep(1)


def motor_effect_thread():
    global trigger_motor_effect
    GPIO.setmode(GPIO.BOARD)        # Number GPIOs by physical location
    GPIO.setup(config.MOTOR_PIN, GPIO.OUT)   # Set motor_pin mode is output
    GPIO.output(config.MOTOR_PIN, GPIO.LOW)  # Set motor_pin to low(0V)

    while True:
        time.sleep(constant.MOTOR_UPDATE_DELAY)
        if trigger_motor_effect == constant.START_COMMAND:
            GPIO.output(config.MOTOR_PIN, GPIO.HIGH)
            time.sleep(config.MOTOR_EFFECT_DELAY)
            GPIO.output(config.MOTOR_PIN, GPIO.LOW)
            trigger_effect(constant.MOTOR_EFFECT_TARGET, constant.STOP_COMMAND)


def trigger_effect(target, command):
     global trigger_led_effect
     global trigger_motor_effect

     trigger_effect_lock.acquire()
     if (command is not constant.STOP_COMMAND) and (command is not constant.START_COMMAND):
       logging.error("Wrong value for command")

     if target == constant.ALL_EFFECT_TARGET:
         trigger_motor_effect = command
         trigger_led_effect = command
     elif target == constant.LED_EFFECT_TARGET:
         trigger_led_effect = command
     elif target == constant.MOTOR_EFFECT_TARGET:
         trigger_motor_effect = command
     else:
       logging.error("Wrong value for target")
     trigger_effect_lock.release()

