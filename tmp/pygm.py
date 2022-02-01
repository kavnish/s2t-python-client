import pyaudio
import wave

import pygame, sys
from pygame.locals import *
import time

pygame.init()
scr = pygame.display.set_mode((640, 480))
recording = True

'''
import pyautogui
import pygame
loop = True

a_key_down = False                                    # Added variable
while loop:

     for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    a_key_down = True                 # Replaced keydown code with this
            if event.type == pygame.KEYUP:            # Added keyup
                if event.key == pygame.K_a:
                    a_key_down = False                
    if a_key_down:                                    # Added to check if key is down
         pyautogui.moveRel(-50,0)
'''

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")


def read_frames():
    frames = []
    while True:
        if recording:
            data = stream.read(CHUNK, exception_on_overflow = False)
            frames.append(data)

        for event in pygame.event.get():
            if event.type == KEYDOWN and recording:
                print("* done recording")

                stream.stop_stream()
                stream.close()
                p.terminate()
                return frames

RECORD = True

read_frames()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
recording = False

if event.type == QUIT:
    pygame.quit(); sys.exit()