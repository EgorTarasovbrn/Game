import pygame
import sys

pygame.init()

pygame.mixer.init()


def hit_sound():
    hit = pygame.mixer.Sound('data/hit.mp3')
    hit.play()


def jump_sound():
    jump = pygame.mixer.Sound('data/jump.mp3')
    jump.play()


def throw_sound():
    throw = pygame.mixer.Sound('data/throw.mp3')
    throw.play()


def fall_soound():
    fall = pygame.mixer.Sound('data/fall.mp3')
    fall.play()


def hit2_sound():
    hit = pygame.mixer.Sound('data/hit2.mp3')
    hit.play()


def theme_song():
    pygame.mixer.music.load('data/themesong2.mp3')
    pygame.mixer.music.play(-1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()