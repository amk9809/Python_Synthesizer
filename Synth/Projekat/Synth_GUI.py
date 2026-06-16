import librosa
from scipy.signal import butter, lfilter
import pygame
import sys
from pygame.locals import *
import sounddevice as sd


y, sr = librosa.load('/home/amk9809/Desktop/MyFolder/python_projects/PFE_2026/Prolecni/Projekat/C_Major_Piano.mp3', sr=44100)

def terminal_input():
    a = input("Type a note: ")
    n=0
    A = a[0]
    B = int(a[1])

    M = [['C', 1], ['C#', 2], ['D', 3], ['D#', 4], ['E', 5], ['F', 6], ['F#', 7], ['G', 8], ['G#', 9], ['A', 10], ['A#', 11], ['H', 12]]

    for i in range(12):
        if A==M[i][0]:
            n = i

    req_shift = (B-4)*12 + M[n][1]-1

    return librosa.effects.pitch_shift(y, sr=sr, n_steps=req_shift)


def lowpass_filter(Sound):

    def butter_lowpass(cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='low', analog=False)

    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    order = 6
    fs = sr     
    cutoff = 4500 

    return butter_lowpass_filter(Sound, cutoff, fs, order)

def play_note(sound):
    sd.play(sound, sr)
    status = sd.wait()



def __main__():
    sound = lowpass_filter(terminal_input())
    play_note(sound)

    pygame.init()

    DISPLAY=pygame.display.set_mode((1600,800),0,32)

    WHITE=(255,255,255)
    BLACK=(0,0,0)

    DISPLAY.fill(WHITE)

    pygame.draw.rect(DISPLAY,BLACK,(700,350,100,50))

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


__main__()
