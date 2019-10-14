import RPi.GPIO as GPIO
import time
import pygame
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

sound = "/home/pi/Desktop/ScaryDahlia/MassicotStreamer/guillotine2-loud.wav"

RELAIS_SPRAY = 17
MAT_INPUT = 4
try:
    GPIO.setup(RELAIS_SPRAY, GPIO.OUT)
    GPIO.setup(MAT_INPUT, GPIO.IN)
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    GPIO.output(RELAIS_SPRAY, GPIO.LOW) # on
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
        pygame.mixer.music.play()
        time.sleep(2.1)  # delay of the sound
        # .5s of full blast of air in the nect
        print("bam")
        GPIO.output(RELAIS_SPRAY, GPIO.HIGH) # on
        time.sleep(0.5)
        GPIO.output(RELAIS_SPRAY, GPIO.LOW) # off
except:  
    GPIO.cleanup()  
