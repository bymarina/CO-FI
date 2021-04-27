#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pigpio
import time
import smbus
from webapp.machine.logger import log_and_print
from gpiozero import DistanceSensor, LightSensor, Buzzer
import RPi.GPIO as GPIO


class piGPIO(object):
    pi = None
    # Servo motores
    
    #GPIO 16
    ULTRASONIC_ECHO = 23

    #GPIO 18
    ULTRASONIC_TRIGGER = 24 
    
    # GPIO 32
    SERVO0 = 12

    # GPIO 33
    SERVO1 = 13
    
    # GPIO 35
    SERVO2 = 19
    
    # GPIO 22
    HEATER = 25
    
    # GPIO 11
    H_PUMP0 = 17

    # GPIO 13
    H_PUMP1 = 27
    
    # GPIO 7
    MIXER = 4
    
    # GPIO 12 test pin
    LED = 18

    #GPIO 15
    IR0 = 22

    #GPIO 19
    LDR_pin = 10

    def gpio_config(self):
        log_and_print("Configuring GPIO...")
        pi = pigpio.pi()
        if not pi.connected:
            raise Exception("Error while configuring RaspberryPI GPIO.")
        self.pi = pi

        # Stating outputs
        pi.set_mode(self.ULTRASONIC_TRIGGER, pigpio.OUTPUT)
        pi.set_mode(self.ULTRASONIC_ECHO, pigpio.INPUT)
        pi.set_mode(self.HEATER, pigpio.OUTPUT)
        pi.set_mode(self.H_PUMP0, pigpio.OUTPUT)
        pi.set_mode(self.H_PUMP1, pigpio.OUTPUT)
        pi.set_mode(self.MIXER, pigpio.OUTPUT)
        pi.set_mode(self.LED, pigpio.OUTPUT)
        pi.set_mode(self.SERVO0, pigpio.OUTPUT)
        pi.set_mode(self.SERVO1, pigpio.OUTPUT)
        pi.set_mode(self.SERVO2, pigpio.OUTPUT)
        pi.set_mode(self.IR0, pigpio.OUTPUT)
        

        pi.write(self.HEATER, 0)
        pi.write(self.H_PUMP0, 0)
        pi.write(self.H_PUMP1, 0)
        pi.write(self.MIXER, 0)
        pi.write(self.LED, 1)
        pi.write(self.ULTRASONIC_TRIGGER, 0)
        pi.write(self.IR0, 1)
        
        pi.read(self.ULTRASONIC_ECHO)

        log_and_print("GPIO Configured.")
        return pi

    def heater_control(self):
        log_and_print("Turning the heater on ")
        pi = self.pi
        pi.write(self.HEATER, 1)
        time.sleep(20)
        log_and_print("Turning the heater off ")
        pi.write(self.HEATER, 0)
        time.sleep(0.5)
        log_and_print("Heater function finished.")

    def mixer_control(self):
        log_and_print("Turning the mixer on ")
        pi = self.pi
        pi.write(self.MIXER, 1)
        time.sleep(5)
        log_and_print("Turning the mixer off ")
        pi.write(self.MIXER, 0)
        time.sleep(0.5)
        log_and_print("Mixer function finished.")

    def water_pump0_control(self):
        pi = self.pi
        log_and_print("Turning the water pump 0 on ")
        pi.write(self.H_PUMP0, 1)
        time.sleep(8)
        log_and_print("Turning the water pump 0 off ")
        pi.write(self.H_PUMP0, 0)
        time.sleep(0.5)
        log_and_print("Water pump 0 function finished.")

    def water_pump1_control(self):
        pi = self.pi
        log_and_print("Turning the water pump 1 on ")
        pi.write(self.H_PUMP1, 1)
        time.sleep(8)
        log_and_print("Turning the water pump 1 off ")
        pi.write(self.H_PUMP1, 0)
        time.sleep(0.5)
        log_and_print("Water pump 1 function finished.")

    def angle_to_percent (angle) :
        if angle > 180 or angle < 0 :
            return False

        start = 4
        end = 12.5
        ratio = (end - start)/180 #Calcul ratio from angle to percent

        angle_as_percent = angle * ratio

        return start + angle_as_percent

    def servo0_control(self, spoons):
        servoPIN = 12
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        s0 = GPIO.PWM(servoPIN, 50) # GPIO 12 for PWM with 50Hz
        s0.start(6) # Initialization of Servo0

        s0.ChangeDutyCycle(5.3)
        time.sleep(0.1)
        s0.ChangeDutyCycle(3.8)
        time.sleep(1*spoons)
        s0.ChangeDutyCycle(5.3)
        time.sleep(0.1)

        s0.stop()
        GPIO.cleanup()
        log_and_print("Servo0 test complete")

    def servo1_control(self, spoons):
        servoPIN = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        s1 = GPIO.PWM(servoPIN, 50) # GPIO 13 for PWM with 50Hz
        s1.start(6) # Initialization of Servo0

        s1.ChangeDutyCycle(4.5)
        time.sleep(0.1)
        s1.ChangeDutyCycle(3.0)
        time.sleep(1*spoons)
        s1.ChangeDutyCycle(4.5)
        time.sleep(0.1)

        s1.stop()
        GPIO.cleanup()
        log_and_print("Servo1 test complete")

    def servo2_control(self, spoons):
        servoPIN = 19
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        s2 = GPIO.PWM(servoPIN, 50) # GPIO 19 for PWM with 50Hz
        s2.start(4.5) # Initialization of Servo0

        s2.ChangeDutyCycle(4.5)
        time.sleep(0.1)
        s2.ChangeDutyCycle(3.0)
        time.sleep(1*spoons)
        s2.ChangeDutyCycle(4.5)
        time.sleep(0.1)

        s2.stop()
        GPIO.cleanup()
        log_and_print("Servo2 test complete")

    def i2c_communication_test(self):

        address = 0x48
        A0 = 0x40
        value=0

        bus = smbus.SMBus(1)

        while True:
            bus.write_byte_data(address,A0,0)
            value = bus.read_byte(address)
            print("IR Measure: ",value)
            time.sleep(1)

    def ultrasonic_sensor_distance_control(self):
        ultrasonic = DistanceSensor (echo=23, trigger=24)
        result = 0
        critical = 0.16000

        # while True:
        #     print("Distance: ",ultrasonic.distance)

        if ultrasonic.distance < critical:
            result = 1
        elif ultrasonic.distance >= critical:
            result = 0

        return result

    # def ultrasonic_sensor_range(self):
    #     ultrasonic = DistanceSensor (echo=23, trigger=24)
        
    
    #     ultrasonic.wait_for_in_range()
    #     print("In range")
    #     ultrasonic.wait_for_out_of_range()
    #     print("out of range")

    def light_sensor_control(self):
        result = 0
        critical_value = 0.1
        LDR = LightSensor(self.LDR_pin)

        #while True:
         #  print(LDR.value)
         #  time.sleep(1)

        if LDR.value <= critical_value:
            result = 1
        elif LDR.value > critical_value:
            result = 0
        
        return result

