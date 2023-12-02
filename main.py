import pygame

pygame.init()

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 700

# fps
FPS = 60
clock = pygame.time.Clock()

# Создание окна
screen = pygame.display.set_mode((SCREEN_WINDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')

# Загрузка изображения(просто для примера)
image_background = pygame.image.load('game_fon.jpg')
image_person = pygame.image.load('person.png')


class Player:
    def __init__(self):
        self.image = pygame.transform.scale(image_person, (100, 100))
        self.coords = [SCREEN_WINDTH // 2 - 50, SCREEN_HEIGHT - 150]
        self.gravity = 10

    def draw(self):
        screen.blit(self.image, (self.coords))

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.coords[0] -= 10
        if key[pygame.K_d]:
            self.coords[0] += 10

        self.check_positions()

    def check_positions(self):
        x, y = self.coords
        if x < 0 - self.image.get_width():
            self.coords[0] = SCREEN_WINDTH
        elif x > SCREEN_WINDTH:
            self.coords[0] = -self.image.get_width()


player = Player()

# Основной игровой цикл
running = True
while running:

    # Рисование заднего фона
    screen.blit(image_background, (0, 0))

    # Рисование спрайтов
    player.draw()

    # Движение персонажа
    player.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
