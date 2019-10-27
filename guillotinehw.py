import RPi.GPIO as GPIO
import time
import pygame
from random import choice

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

filesound1 = "./guillotine1-normalized.wav"
filesound2 = "./guillotine2-normalized.wav"

RELAIS_SPRAY = 17
MAT_INPUT = 4

class GuillotineHW:
    def __init__(self):
        GPIO.setup(RELAIS_SPRAY, GPIO.OUT)
        GPIO.setup(MAT_INPUT, GPIO.IN)
        GPIO.output(RELAIS_SPRAY, GPIO.LOW) # off
        pygame.mixer.init()    
        sound1 = pygame.mixer.Sound(file=filesound1)
        sound2 = pygame.mixer.Sound(file=filesound2)
        sounds = [sound1, sound2]
        for s in sounds:
            s.set_volume(1)
        self.spraying = False

    def start_air(self):
        GPIO.output(RELAIS_SPRAY, GPIO.HIGH) # on
        print("ffffff")
        return 0.5

    def stop_air(self):
        GPIO.output(RELAIS_SPRAY, GPIO.LOW) # of
        print("stopair")

    def start_sound(self):
        sound = choice(sounds)
        print("playing sound")
        sound_length = sound.get_length()
        sound.play()        
        return sound_length - 1

    def __del__(self):
        print("cleaning GPIO")
        GPIO.cleanup()
