import librosa
from scipy.signal import butter, lfilter
import pygame
import sys
from pygame.locals import *
import sounddevice as sd
import time


y, sr = librosa.load('Projekat/C_Major_Piano.mp3', sr=44100)
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

B = [[37, 1], [72, 3], [142, 6], [177, 8], [212, 10], [282, 13], [317, 15], [387, 18], [422, 20], [457, 22], [527, 25], [562, 27], [632, 30], [667, 32], 
    [702, 34], [772, 37], [807, 39], [877, 42], [912, 44], [947, 46], [1017, 49], [1052, 51], [1122, 54], [1157, 56], [1192, 58], [1262, 61], [1297, 61], 
    [1367, 66], [1402, 68], [1437, 70], [1507, 73], [1542, 75]]

def play_note(sound):
    sd.play(sound, sr)

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
            if pos[0]>B[i][0] and pos[0]<B[i][0]+20:
                m = B[i][1]
                k = 1
    if k == 0:
        W = [[0, 0], [1, 2], [2, 4], [3, 5], [4, 7], [5, 9], [6, 11]]
        n = (pos[0]-15)//35

        for i in range(7):
            if n%7 == W[i][0]:
                m = W[i][1]

    req_shift = (n//7)*12 + m - 36
    if len(W_KEYS)<=n:
        return 0
    else: 
        play_note(lowpass_filter(librosa.effects.pitch_shift(y, sr=sr, n_steps=req_shift)))

def paint_keys(pos):
    k=0
    if pos[1]>=500 and pos[1]<=560:
        for i in range(len(B)):
            if pos[0]>B[i][0] and pos[0]<B[i][0]+20:
                m = i
                k = 1
    if k == 0:
        n = (pos[0]-15)//35
        if len(W_KEYS)<=n:
            return 0
    if k == 1:
        pygame.draw.rect(DISPLAY,BLACK_CLICKED,(B[m][0],500,20,60))
    elif k == 0:
        pygame.draw.rect(DISPLAY,WHITE_CLICKED,(W_KEYS[n],500,30,100))
        for i in range(40):
            for k in range(len(B)):
                if pos[0]+i == B[k][0]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k][0],500,20,60))
                if pos[0]-i == B[k][0]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k][0],500,20,60))

    return time.time()

def paint_back(pos):
    k=0
    if pos[1]>=500 and pos[1]<=560:
        for i in range(len(B)):
            if pos[0]>B[i][0] and pos[0]<B[i][0]+20:
                m = i
                k = 1
    if k == 0:
        n = (pos[0]-15)//35
        if len(W_KEYS)<=n:
            return 0
    if k == 1:
        pygame.draw.rect(DISPLAY,BLACK,(B[m][0],500,20,60))
    elif k == 0:
        pygame.draw.rect(DISPLAY,WHITE,(W_KEYS[n],500,30,100))
        for i in range(40):
            for k in range(len(B)):
                if pos[0]+i == B[k][0]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k][0],500,20,60))
                    K=k
                if pos[0]-i == B[k][0]:
                    pygame.draw.rect(DISPLAY,BLACK,(B[k][0],500,20,60))
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