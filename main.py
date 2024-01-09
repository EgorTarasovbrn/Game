import pygame
import random
import time

timing = time.time()

pygame.init()

pygame.mixer.music.load("data/themesong2.mp3")
pygame.mixer.music.set_volume(0.37)
pygame.mixer.music.play(-1)

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 850

COUNT = 0

JUMP_COUNT = 0

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

theme = pygame.image.load('data/theme.png')
theme = pygame.transform.scale(theme, (SCREEN_WINDTH, SCREEN_HEIGHT))

# Загрузка изображения
image_platform = pygame.image.load('data/platform.png')  # платформа
image_fake_platform = pygame.image.load('data/platform2.png')  # фэйк платформа

image_monster = pygame.image.load('data/grinch.png')  # монстр
image_monster = pygame.transform.scale(image_monster, (62, 102))

image_bullet = ['data/christmasball1.png', 'data/christmasball2.png', 'data/christmasball3.png',
                'data/christmasball4.png']

image_person = pygame.image.load('data/player.png')  # игрок
image_person_width = image_person.get_width()
image_person_height = image_person.get_height()

sprite_player = pygame.sprite.Group()  # персонаж
sprite_bullet = pygame.sprite.Group()  # группа пуль
sprite_monster = pygame.sprite.Group()  # группа монстров
sprite_platforms = pygame.sprite.Group()  # группа платформ
sprite_fake_platforms = pygame.sprite.Group()  # группа фэйк платформ


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
                        jump_sound()
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        for platform in sprite_fake_platforms:
            # если при прыжке будет пересечение, то...
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # если игрок находится выше платформы
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        global JUMP_COUNT
                        JUMP_COUNT += 1
                        jump_sound()
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
            fall_sound()
            return True


# класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_bullet[random.randrange(0,
                                                                                            len(image_bullet))]),
                                            (23, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y < 0 or self.rect.x < 0 or self.rect.x > SCREEN_WINDTH or self.rect.y > SCREEN_HEIGHT:
            self.kill()


# класс игрока
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = image_monster
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0

    def update(self, scroll):
        global POINT
        self.rect.y += scroll
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            POINT += 45


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


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        font = pygame.font.Font(None, 50)
        text = font.render('Paused. Press enter to continue', True, 'red')
        text_x = SCREEN_WINDTH // 2 - text.get_width() // 2
        text_y = SCREEN_HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()


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


class FakePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = image_fake_platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        global POINT
        self.rect.y += scroll
        if self.rect.y > SCREEN_HEIGHT:
            global JUMP_COUNT
            JUMP_COUNT = 0
            self.kill()
            POINT += 90


player = Player(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 200)
sprite_player.add(player)
platform = Platform(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 100)
sprite_platforms.add(platform)

last_shot_time = time.time()
cooldown_time = 1.0  # Задержка между выстрелами в секундах

# Основной игровой цикл
running = True
while running:
    # создание платформ
    if len(sprite_platforms) < 10 and COUNT != 15:
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)
        platform = Platform(platform_x, platform_y)
        COUNT += 1
        if time.time() - timing > 15.0:
            timing = time.time()
            monster = Monster(platform_x + 31, platform_y - 102)
            sprite_monster.add(monster)
        sprite_platforms.add(platform)
    elif len(sprite_platforms) < 10 and COUNT == 15:
        COUNT = 0
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)
        platform = FakePlatform(platform_x, platform_y)
        sprite_fake_platforms.add(platform)

    scroll = player.move()
    screen.blit(theme, (0, 0))
    sprite_monster.update(scroll)
    sprite_platforms.update(scroll)
    sprite_fake_platforms.update(scroll)
    sprite_player.draw(screen)
    sprite_fake_platforms.draw(screen)
    sprite_monster.draw(screen)
    sprite_platforms.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pause()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_time = time.time()
            x, y = event.pos
            if current_time - last_shot_time > cooldown_time:
                throw_sound()
                if x < SCREEN_WINDTH // 3:
                    bullet = Bullet(player.rect.centerx, player.rect.centery, -5, -5)
                    sprite_bullet.add(bullet)
                elif x < 2 * SCREEN_WINDTH // 3:
                    bullet = Bullet(player.rect.centerx, player.rect.centery, 0, -5)
                    sprite_bullet.add(bullet)
                else:
                    bullet = Bullet(player.rect.centerx, player.rect.centery, 5, -5)
                    sprite_bullet.add(bullet)
                # Обновите время последнего выстрела
                last_shot_time = current_time

    sprite_bullet.update()
    sprite_bullet.draw(screen)

    for bullet in sprite_bullet:
        if pygame.sprite.spritecollideany(bullet, sprite_monster):
            POINT += 180
            hit_sound()
            sprite_monster.remove(monster)
            sprite_bullet.remove(bullet)

    if pygame.sprite.spritecollideany(player, sprite_monster):
        hit2_sound()
        end_screen()
        running = False
        pygame.quit()

    if JUMP_COUNT == 2:
        JUMP_COUNT = 0
        sprite_fake_platforms.empty()

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
