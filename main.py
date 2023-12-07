import pygame

pygame.init()

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 700

# fps
FPS = 60
clock = pygame.time.Clock()

GRAVITY = 1

# Создание окна
screen = pygame.display.set_mode((SCREEN_WINDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')

# Загрузка изображения(просто для примера)
image_background = pygame.image.load('game_fon.jpg')
image_person = pygame.image.load('person.png')


class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(image_person, (100, 100))
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.coords = [x, y]
        self.gravity = 10
        self.vel_y = 0

    def draw(self):
        screen.blit(self.image, (self.coords))

    def move(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()  # список нажатых кнопок
        if key[pygame.K_a]:
            dx -= 10
        if key[pygame.K_d]:
            dx += 10

        self.vel_y += GRAVITY
        dy += self.vel_y

        x, y = self.coords
        if x < 0 - self.image.get_width():
            self.coords[0] = SCREEN_WINDTH
        elif x > SCREEN_WINDTH:
            self.coords[0] = -self.image.get_width()

        if y > SCREEN_HEIGHT - self.image_height:
            self.dy = 0
            self.vel_y = -25

        self.coords[0] += dx
        self.coords[1] += dy


player = Player(SCREEN_WINDTH // 2 - 50, SCREEN_HEIGHT - 150)

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
