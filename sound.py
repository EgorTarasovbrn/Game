import pygame


def hit_sound():
    hit = pygame.mixer.Sound('data/hit.mp3')
    hit.play()


def jump_sound():
    jump = pygame.mixer.Sound('data/jump.mp3')
    jump.play()


def throw_sound():
    throw = pygame.mixer.Sound('data/throw.mp3')
    throw.play()