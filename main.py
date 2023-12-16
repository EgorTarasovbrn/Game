import pygame
import random

pygame.init()

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 700

# высота границы
SCROLL_TRIGGER = 250

# fps
FPS = 60
clock = pygame.time.Clock()
# гравитация
GRAVITY = 1

# Создание окна
screen = pygame.display.set_mode((SCREEN_WINDTH, SCREEN_HEIGHT))
# название окна
pygame.display.set_caption('Game')

# Загрузка изображения(просто для примера)
image_background = pygame.image.load('game_fon.jpg')  # задний фон
image_platform = pygame.image.load('data/platform.png')  # платформа

image_person = pygame.image.load('data\player.png')  # игрок
image_person_width = image_person.get_width()
image_person_height = image_person.get_height()

sprite_player = pygame.sprite.Group()
sprite_platforms = pygame.sprite.Group()  # группа платформ


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(image_person, (image_person_width * 2, image_person_height * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0

    def move(self):  # движение игрока
        dx = 0  # изменение координаты х
        dy = 0  # изменение координаты y
        scroll = 0

        key = pygame.key.get_pressed()  # список нажатых кнопок
        if key[pygame.K_a]:  # движение влево
            dx -= 10
        if key[pygame.K_d]:  # движение вправо
            dx += 10

        self.vel_y += GRAVITY  # прыжок
        dy += self.vel_y

        # проверка пересечения игроком границ карты слева и справа
        if self.rect.x < 0 - self.rect.width:
            self.rect.x = SCREEN_WINDTH
        elif self.rect.x > SCREEN_WINDTH:
            self.rect.x = -self.rect.width
        # проверка запрыгнул ли игрок на платформу
        for platform in sprite_platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
        # проверка коснулся ли игрок скролла или нет
        if self.rect.y <= SCROLL_TRIGGER and self.vel_y < 0:
            scroll = -dy

        self.rect.x += dx # изменение координаты х у игрока(движение)
        self.rect.y += dy + scroll # изменение координаты y у игрока(движение)
        return scroll

#класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = image_platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


player = Player(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 200)
sprite_player.add(player)
platform = Platform(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 100)
sprite_platforms.add(platform)

# Основной игровой цикл
running = True
while running:
    if len(sprite_platforms) < 10:
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)
        platform = Platform(platform_x, platform_y)
        sprite_platforms.add(platform)
    # Рисование заднего фона
    # screen.blit(image_background, (0, 0))
    screen.fill((210, 210, 210))
    pygame.draw.line(screen, 'black', (0, SCROLL_TRIGGER), (SCREEN_WINDTH, SCROLL_TRIGGER))

    sprite_platforms.update(player.move())
    sprite_player.draw(screen)
    sprite_platforms.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
