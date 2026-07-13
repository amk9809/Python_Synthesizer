import librosa
from scipy.signal import butter, lfilter
import pygame
import sys
from pygame.locals import *
import sounddevice as sd
import time
import numpy as np


W_KEYS = []
B_KEYS = []

MEMORY = [[1, [0,0]]]

DISPLAY=pygame.display.set_mode((1600,800),0,32)

GREY=(200,200,200)
WHITE=(255,255,255)
WHITE_CLICKED=(205,205,205)
BLACK=(0,0,0)
BLACK_CLICKED=(50,50,50)
BROWN=(96,59,42)

B = [37, 72, 142, 177, 212, 282, 317, 387, 422, 457, 527, 562, 632, 667, 702, 772, 807, 877, 912, 947, 1017, 1052, 1122, 1157, 1192, 1262, 1297,
    1367, 1402, 1437, 1507, 1542]

W_FREQUENCIES = [16.35, 18.35, 20.60, 21.83, 24.5, 27.5, 30.87]
B_FREQUENCIES = [17.32, 19.45, 23.12, 25.96, 29.14]


def play_note(fr):
    frequency = fr  
    duration = 3     
    sampling_rate = 44100  

    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)

    sd.play(wave, samplerate=sampling_rate)


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
    if len(W_KEYS)<=n:
        return 0
    else: 
        play_note(librosa.effects.pitch_shift(y, sr=sr, n_steps=req_shift))

def mouse_input(pos):
    #black keys
    n = 0
    k = 0
    
    if pos[1]>=500 and pos[1]<=560:
        for i in range(32):
            if pos[0]>B[i] and pos[0]<B[i]+20:
                n = i
                k = 1

    if k == 0:
        n = (pos[0]-15)//35 

    if k == 1:
        m = n//5
        l = n%5
        req_shift = B_FREQUENCIES[l]*(2**(m+1))
    else:
        m = n//7
        l = n%7
        req_shift = W_FREQUENCIES[l]*(2**(m+1))


    if len(W_KEYS)<=n:
        return 0
    else: 
        play_note(req_shift)

def paint_keys(pos):
    k=0
    if pos[1]>=500 and pos[1]<=560:
        for i in range(len(B)):
            if pos[0]>B[i] and pos[0]<B[i]+20:
                m = i
                k = 1
    if k == 0:
        n = (pos[0]-15)//35
        if len(W_KEYS)<=n:
            return 0
    if k == 1:
        pygame.draw.rect(DISPLAY,BLACK_CLICKED,(B[m],500,20,60))
    elif k == 0:
        pygame.draw.rect(DISPLAY,WHITE_CLICKED,(W_KEYS[n],500,30,100))
        for i in range(40):
            for k in range(len(B)):
                if pos[0]+i == B[k]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k],500,20,60))
                if pos[0]-i == B[k]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k],500,20,60))

    return time.time()

def paint_back(pos):
    k=0
    if pos[1]>=500 and pos[1]<=560:
        for i in range(len(B)):
            if pos[0]>B[i] and pos[0]<B[i]+20:
                m = i
                k = 1
    if k == 0:
        n = (pos[0]-15)//35
        if len(W_KEYS)<=n:
            return 0
    if k == 1:
        pygame.draw.rect(DISPLAY,BLACK,(B[m],500,20,60))
    elif k == 0:
        pygame.draw.rect(DISPLAY,WHITE,(W_KEYS[n],500,30,100))
        for i in range(40):
            for k in range(len(B)):
                if pos[0]+i == B[k]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k],500,20,60))
                    K=k
                if pos[0]-i == B[k]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k],500,20,60))
                    K=k


def __main__():
    pygame.init()

    DISPLAY.fill(GREY)
    pygame.draw.rect(DISPLAY,BROWN,(5,490,1590,120))
    k=7
    for i in range(15, 1600, 35):
        if 1600-i>30:
            pygame.draw.rect(DISPLAY,WHITE,(i,500,30,100))
            W_KEYS.append(i)
    i=37
    while k>0:
        if 1600-i>20:
            for n in range(2):
                pygame.draw.rect(DISPLAY,BLACK,(i,500,20,60))
                B_KEYS.append(i)
                i=i+35
            i=i+35
            for n in range(3):
                pygame.draw.rect(DISPLAY,BLACK,(i,500,20,60))
                i=i+35
            i=i+35
        k-=1


    t1 = 0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        t0 = time.time()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (pos[1]>=500 and pos[1]<=600) and t0-t1>0.1:
                a = paint_keys(pos)
                temp = []
                temp.append(a)
                temp.append(pos)
                MEMORY.append(temp)
                mouse_input(pos)
            t1 = time.time()
        if len(MEMORY)>0:
            if t0-MEMORY[0][0]>2:
                paint_back(MEMORY[0][1])
                MEMORY.pop(0)

__main__()