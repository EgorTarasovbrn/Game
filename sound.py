import pygame


def hit_sound():
    hit = pygame.mixer.Sound('data/hit.mp3')
    hit.play()


def jump_sound():
    jump = pygame.mixer.Sound('data/jump.mp3')
    jump.set_volume(0.3)
    jump.play()


def throw_sound():
    throw = pygame.mixer.Sound('data/throw.mp3')
    throw.play()


def fall_sound():
    fall = pygame.mixer.Sound('data/fall.mp3')
    fall.play()


def hit2_sound():
    hit2 = pygame.mixer.Sound('data/hit2.mp3')
    hit2.play()