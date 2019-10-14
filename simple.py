import RPi.GPIO as GPIO
import time
import pygame
from random import choice

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

filesound1 = "/home/pi/Desktop/ScaryDahlia/MassicotStreamer/guillotine1-loud.wav"
filesound2 = "/home/pi/Desktop/ScaryDahlia/MassicotStreamer/guillotine2-loud.wav"

RELAIS_SPRAY = 17
MAT_INPUT = 4
try:
    GPIO.setup(RELAIS_SPRAY, GPIO.OUT)
    GPIO.setup(MAT_INPUT, GPIO.IN)
    GPIO.output(RELAIS_SPRAY, GPIO.LOW) # off
    pygame.mixer.init()    
    sound1 = pygame.mixer.Sound(file=filesound1)
    sound2 = pygame.mixer.Sound(file=filesound2)
    sounds = [sound1, sound2]
    for s in sounds:
        s.set_volume(1)
    while True:
        print("waiting")
        while not GPIO.input(MAT_INPUT):
            time.sleep(0.2)
        print("a client")
        time.sleep(10)
        # if the trigger left after 10s
        if not GPIO.input(MAT_INPUT):
            # Back to waiting
            print("client left")
            continue
        # The subject must be in place by now.
        sound = choice(sounds)
        sound_length = sound.get_length()
        sound.play()
        time.sleep(sound_length - 0.5)  # delay of the sound
        # .5s of full blast of air in the nect
        print("bam")
        GPIO.output(RELAIS_SPRAY, GPIO.HIGH) # on
        time.sleep(0.5)
        GPIO.output(RELAIS_SPRAY, GPIO.LOW) # off
except:  
    GPIO.cleanup()  