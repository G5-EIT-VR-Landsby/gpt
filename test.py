import pygame
from time import sleep

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("speech.mp3", 'mp3')
pygame.mixer.music.play()
sleep(5)
