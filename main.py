import pygame
import random
import time
timing = time.time()

pygame.init()

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 850

snowflakes = []

# подсчет количества очков
POINT = 0

# сторона куда смотрит персоонаж
POLOZHENIYE = 'left'

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

theme = pygame.image.load('theme.png')
theme = pygame.transform.scale(theme, (SCREEN_WINDTH, SCREEN_HEIGHT))

# Загрузка изображения
image_platform = pygame.image.load('data/platform.png')  # платформа

image_monster = pygame.image.load('grinch.png')  # монстр
image_monster = pygame.transform.scale(image_monster, (62, 102))

image_person = pygame.image.load('data\player.png')  # игрок
image_person_width = image_person.get_width()
image_person_height = image_person.get_height()

sprite_player = pygame.sprite.Group()
sprite_monster = pygame.sprite.Group()
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
        global POLOZHENIYE
        dx = 0  # изменение координаты х
        dy = 0  # изменение координаты y
        scroll = 0
        key = pygame.key.get_pressed()  # список нажатых кнопок
        if key[pygame.K_a]:  # движение влево
            dx -= 10
            if POLOZHENIYE == 'left':
                POLOZHENIYE = 'right'
                self.image = pygame.transform.flip(self.image, True, False)
        if key[pygame.K_d]:  # движение вправо
            dx += 10
            if POLOZHENIYE == 'right':
                POLOZHENIYE = 'left'
                self.image = pygame.transform.flip(self.image, True, False)

        self.vel_y += GRAVITY  # прыжок
        dy += self.vel_y

        # проверка пересечения игроком границ карты слева и справа
        if self.rect.x < 0 - self.rect.width:
            self.rect.x = SCREEN_WINDTH
        elif self.rect.x > SCREEN_WINDTH:
            self.rect.x = -self.rect.width

        # проверка запрыгнул ли игрок на платформу
        for platform in sprite_platforms:
            # если при прыжке будет пересечение, то...
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # если игрок находится выше платформы
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # проверка коснулся ли игрок скролла или нет
        if self.rect.y <= SCROLL_TRIGGER and self.vel_y < 0:
            scroll = -dy

        self.rect.x += dx  # изменение координаты х у игрока(движение)
        self.rect.y += dy + scroll  # изменение координаты y у игрока(движение)
        return scroll

    def check_end_game(self):  # упал ли игрок
        if self.rect.bottom > SCREEN_HEIGHT:
            return True


# класс игрока
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = image_monster
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0


def end_screen():
    screen = pygame.display.set_mode((SCREEN_WINDTH, SCREEN_HEIGHT))
    running = True
    font = pygame.font.Font(None, 50)
    text = font.render('Game over', True, 'red')
    text_x = SCREEN_WINDTH // 2 - text.get_width() // 2
    text_y = SCREEN_HEIGHT // 2 - text.get_height() // 2
    screen.fill((0, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()


# класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = image_platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        global POINT
        self.rect.y += scroll
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            POINT += 90


player = Player(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 200)
sprite_player.add(player)
monster = Monster(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 600)
sprite_monster.add(monster)
platform = Platform(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 100)
sprite_platforms.add(platform)

# Основной игровой цикл
running = True
while running:
    if time.time() - timing > 2.0:
        timing = time.time()
        print("2 seconds")
    # создание платформ
    if len(sprite_platforms) < 10:
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)
        platform = Platform(platform_x, platform_y)
        sprite_platforms.add(platform)

    screen.blit(theme, (0, 0))

    sprite_platforms.update(player.move())
    sprite_player.draw(screen)
    sprite_monster.draw(screen)
    sprite_platforms.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.sprite.spritecollideany(player, sprite_monster):
        print("Игра окончена! Персонаж из первой группы коснулся персонажа из второй группы.")
        end_screen()

    if player.check_end_game():  # если игрок упал, то появляется экран с game over
        end_screen()
        running = False
        pygame.quit()

    if random.randint(1, 10) == 1:
        size = random.randint(1, 5)
        x = random.randint(0, SCREEN_WINDTH)
        y = 0
        speed = random.randint(1, 5)
        snowflakes.append([x, y, size, speed])

    # Обновление координат снежинок и удаление тех, что вышли за пределы экрана
    for flake in snowflakes:
        flake[1] += flake[3]
        if flake[1] > SCREEN_HEIGHT:
            snowflakes.remove(flake)

    # Отрисовка снежинок
    for flake in snowflakes:
        pygame.draw.circle(screen, (255, 255, 255), (flake[0], int(flake[1])), flake[2])

    font = pygame.font.Font(None, 80)
    text = font.render(f"{POINT}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(300, 100))
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()