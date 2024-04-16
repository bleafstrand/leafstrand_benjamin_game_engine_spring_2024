#this file was created by Benjamin Leafstrand

# loop through a list

from setting import *
import pygame as pg

clock = pg.time.Clock()


frames = ["frame1", "frame2", "frame3", "frame4"]

#print(len(frames))

current_frame = 0

frames_length = len(frames)

then = 0

while True:
    #print("forever....")
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 500:
        print(now)
        then = now
        print(current_frame%frames_length)
        current_frame += 1
        








#write a loop that prints in terminal each frame