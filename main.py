import sqlite3
import time

import pygame
import random

timing = time.time()
pygame.init()

pygame.mixer.music.load("data/themesong2.mp3")
pygame.mixer.music.set_volume(0.37)
pygame.mixer.music.play(-1)

con = sqlite3.connect('bd.sqlite')
cur = con.cursor()

HIGH_RECORD = cur.execute('select record from main').fetchone()[0]
print(HIGH_RECORD)
GIFT = cur.execute('select gift from main').fetchone()[0]
pause = False

# подсчет количества очков
POINT = 0

snowflakes = []

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 850

# высота границы
SCROLL_TRIGGER = 250

COUNT = 0

CREATE_ICICLE = pygame.USEREVENT  # событие для создания сосульки
pygame.time.set_timer(CREATE_ICICLE, 5000)

# сторона куда смотрит персоонаж
POLOZHENIYE = 'left'

JUMP_COUNT = 0

# fps
FPS = 60
clock = pygame.time.Clock()

# гравитация
GRAVITY = 1

# Создание окна
screen = pygame.display.set_mode((SCREEN_WINDTH, SCREEN_HEIGHT))

# название окна
pygame.display.set_caption('Game')

# Загрузка изображения
# image_platform = pygame.image.load('data/platform.png')  # платформа

theme = pygame.image.load('data/theme.png')
theme = pygame.transform.scale(theme, (SCREEN_WINDTH, SCREEN_HEIGHT))

# image_fake_platform = pygame.image.load('data/platform2.png')  # фэйк платформа

image_monster = pygame.image.load('data/grinch.png')  # монстр
image_monster = pygame.transform.scale(image_monster, (62, 102))

image_gift = ['data/gift_1.png', 'data/gift_2.png', 'data/gift_3.png']
image_gift_fon = pygame.transform.scale(pygame.image.load(image_gift[random.randrange(0, 3)]), (50, 50))

image_bullet = ['data/christmasball1.png', 'data/christmasball2.png', 'data/christmasball3.png',
                'data/christmasball4.png']

image_person = pygame.image.load('data\player.png')  # игрок
image_person_width = image_person.get_width()
image_person_height = image_person.get_height()

image_icicle = pygame.image.load('data/icicle.png')

image_start_fon = pygame.image.load('data/start_fon.png')
image_start_fon = pygame.transform.scale(image_start_fon, (SCREEN_WINDTH, SCREEN_HEIGHT))

image_platform_garland = ['data/platform_1.png', 'data/platform_2.png', 'data/platform_3.png', 'data/platform_4.png',
                          'data/platform_5.png']
image_platform_garland_fake = ['data/platform_1_fake.png', 'data/platform_2_fake.png', 'data/platform_3_fake.png',
                               'data/platform_4_fake.png', 'data/platform_5_fake.png']

sprite_player = pygame.sprite.Group()
sprite_bullet = pygame.sprite.Group()  # группа пуль
sprite_monster = pygame.sprite.Group()  # группа монстров
sprite_platforms = pygame.sprite.Group()  # группа платформ
sprite_gift = pygame.sprite.Group()
sprite_icicle = pygame.sprite.Group()
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
                        self.rect.bottom = platform.rect.top
                        jump_sound()
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
        if pygame.sprite.spritecollideany(self, sprite_icicle):
            fall_sound()
            return True
        if pygame.sprite.spritecollideany(self, sprite_monster):
            hit2_sound()
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
    def __init__(self, x, y, move, where_move, width_platform, *group):
        super().__init__(*group)
        self.image = image_monster
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.where_move = where_move
        self.is_move = move
        self.platform_width = width_platform

    def update(self, scroll):
        global POINT
        self.rect.y += scroll
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            POINT += 45
        if self.is_move and self.where_move == 'left':
            self.rect.x -= 3
        if self.is_move and self.where_move == 'right':
            self.rect.x += 3

        if self.rect.x < -self.platform_width:
            self.rect.x = SCREEN_WINDTH

        if self.rect.x > SCREEN_WINDTH:
            self.rect.x = -self.platform_width


# класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move, where_move, *group):
        super().__init__(*group)
        self.frame = 0
        self.image = pygame.image.load(image_platform_garland[self.frame])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_move = move
        self.where_move = where_move

    def update(self, scroll):
        global POINT
        self.rect.y += scroll
        self.frame += 0.05
        if self.is_move and self.where_move == 'left':
            self.rect.x -= 3
        if self.is_move and self.where_move == 'right':
            self.rect.x += 3

        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WINDTH

        if self.rect.x > SCREEN_WINDTH:
            self.rect.x = -self.rect.width
        if self.rect.y > SCREEN_HEIGHT:
            POINT += 90
            self.kill()

        if self.frame > 4:
            self.frame = 0
        self.image = pygame.image.load(image_platform_garland[int(self.frame)])


class FakePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.frame = 0
        self.image = pygame.image.load(image_platform_garland_fake[self.frame])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        global POINT
        self.frame += 0.05
        self.rect.y += scroll
        if self.rect.y > SCREEN_HEIGHT:
            global JUMP_COUNT
            JUMP_COUNT = 0
            self.kill()
            POINT += 90
        if self.frame > 4:
            self.frame = 0
        self.image = pygame.image.load(image_platform_garland_fake[int(self.frame)])


class Gift(pygame.sprite.Sprite):

    def __init__(self, image, x, y, width_platform, move, where_move):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x + width_platform // 2 - self.rect.width // 2
        self.rect.y = y - self.image.get_width()
        self.is_move = move
        self.where_move = where_move
        self.platform_width = width_platform

    def update(self, scroll):
        self.rect.y += scroll

        if self.is_move and self.where_move == 'left':
            self.rect.x -= 3
        if self.is_move and self.where_move == 'right':
            self.rect.x += 3

        if self.rect.x < -self.platform_width:
            self.rect.x = SCREEN_WINDTH

        if self.rect.x > SCREEN_WINDTH:
            self.rect.x = -self.platform_width

        if pygame.sprite.spritecollideany(self, sprite_player):
            global GIFT
            GIFT += 1
            cur.execute('update main set gift = gift + 1')
            con.commit()
            take_sound()
            self.kill()

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Icicle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image_icicle
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 8

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


def hit_sound():
    hit = pygame.mixer.Sound('data/hit.mp3')
    hit.play()


def take_sound():
    take = pygame.mixer.Sound('data/take.mp3')
    take.set_volume(0.7)
    take.play()


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


def start_screen(gift):
    screen = pygame.display.set_mode((SCREEN_WINDTH, SCREEN_HEIGHT))
    running = True
    font = pygame.font.Font(None, 50)
    text_gift = font.render(str(GIFT), True, 'white')
    text_score = font.render(f'Лучший рекорд: {HIGH_RECORD}', True, 'white')
    text = font.render('Для начала игры нажмите Space', True, 'White')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
        screen.blit(image_start_fon, (0, 0))
        screen.blit(gift, (10, 10))

        screen.blit(text_gift, (gift.get_width() + 20, gift.get_height() // 2))
        screen.blit(text_score, (10, 90))
        screen.blit(text, (SCREEN_WINDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 200))

        pygame.display.flip()
        screen.fill((0, 0, 0))


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


def switch_pause():
    global pause
    pause = not pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = False

        font = pygame.font.Font(None, 200)
        text = font.render('Пауза', True, 'green')
        screen.blit(text, (SCREEN_WINDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()


start_screen(image_gift_fon)

player = Player(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 200)
sprite_player.add(player)

platform = Platform(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 100, False, False)
sprite_platforms.add(platform)

last_shot_time = time.time()
cooldown_time = 1.0  # Задержка между выстрелами в секундах

gift_image = pygame.transform.scale(pygame.image.load(image_gift[random.randrange(0, len(image_gift))]), (50, 50))

# Основной игровой цикл
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == CREATE_ICICLE:
            sprite_icicle.add(
                Icicle(random.randint(0, SCREEN_WINDTH - image_icicle.get_width()), -image_icicle.get_height() * 2))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                switch_pause()

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

    # создание платформ
    if len(sprite_platforms) < 10 and COUNT != 15:
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)

        COUNT += 1

        move = True if random.randrange(1, 4) == 3 else False
        where_move = 'left' if random.randrange(1, 3) == 1 else 'right'
        give_gift = True if random.randrange(1, 6) == 1 else False

        if time.time() - timing > 10.0 and len(sprite_monster) == 0:
            timing = time.time()
            monster = Monster(platform_x + 31, platform_y - 102, move, where_move, platform_width)
            sprite_monster.add(monster)

        if give_gift:
            gift = Gift(random.choice(image_gift), platform_x, platform_y, platform_width, move, where_move)
            sprite_gift.add(gift)

        platform = Platform(platform_x, platform_y, move, where_move)
        sprite_platforms.add(platform)

    elif len(sprite_platforms) < 10 and COUNT == 15:
        COUNT = 0
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)
        platform = FakePlatform(platform_x, platform_y)
        sprite_fake_platforms.add(platform)

    screen.blit(theme, (0, 0))

    scroll = player.move()

    sprite_monster.update(scroll)

    sprite_platforms.update(scroll)

    sprite_fake_platforms.update(scroll)

    sprite_gift.update(scroll)

    sprite_icicle.update()

    sprite_bullet.update()

    sprite_platforms.draw(screen)

    sprite_bullet.draw(screen)

    sprite_player.draw(screen)

    sprite_gift.draw(screen)

    sprite_fake_platforms.draw(screen)

    sprite_monster.draw(screen)

    sprite_icicle.draw(screen)

    for bullet in sprite_bullet:
        if pygame.sprite.spritecollideany(bullet, sprite_monster):
            POINT += 180
            hit_sound()
            sprite_monster.remove(monster)
            sprite_bullet.remove(bullet)

    if JUMP_COUNT == 2:
        JUMP_COUNT = 0
        sprite_fake_platforms.empty()

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

    if player.check_end_game():  # если игрок упал, то появляется экран с game over
        end_screen()
        if int(POINT) > HIGH_RECORD:
            cur.execute('update main set record = ?', (POINT,))
            print(f'da {POINT}')
            con.commit()
        running = False
        pygame.quit()

    font = pygame.font.Font(None, 60)
    text = font.render(f"{POINT}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WINDTH // 2 - text.get_width() // 2, 10))

    screen.blit(gift_image, (10, 10))

    font_gift = pygame.font.Font(None, 50)
    text_gift = font_gift.render(f"{GIFT}", True, 'white')
    screen.blit(text_gift, (gift_image.get_width() + 20, gift_image.get_height() // 2))

    font_high_record = pygame.font.Font(None, 50)
    text_high_record = font_high_record.render(f'Рекорд: {HIGH_RECORD}', True, 'white')
    screen.blit(text_high_record, (10, text_gift.get_height() * 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
