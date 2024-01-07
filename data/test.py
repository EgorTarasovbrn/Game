import pygame
import sys

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load('themesong2.mp3')

pygame.mixer.music.set_volume(0.5)

pygame.mixer.music.play(-1)

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
