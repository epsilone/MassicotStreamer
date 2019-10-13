import RPi.GPIO as GPIO
import time
import pygame
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

sound_template = "/home/pi/Desktop/ScaryDahlia/MassicotStreamer/guillotine%s-loud.wav"
sounds = [sound_template % i for i in ["1", "2"]]
sound = sounds[0]

RELAIS_SPRAY = 17
MAT_INPUT = 4
try:
    GPIO.setup(RELAIS_SPRAY, GPIO.OUT)
    GPIO.setup(MAT_INPUT, GPIO.IN)
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    GPIO.output(RELAIS_SPRAY, GPIO.LOW) # on
    while True:
        while not GPIO.input(MAT_INPUT):
            time.sleep(0.2)
        pygame.mixer.music.play()
        time.sleep(4.5)
        GPIO.output(RELAIS_SPRAY, GPIO.HIGH) # on
        time.sleep(0.5)
        GPIO.output(RELAIS_SPRAY, GPIO.LOW) # on
except:  
    GPIO.cleanup()  