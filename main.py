import pygame
import random

pygame.init()

pause = False

# размеры окна
SCREEN_WINDTH = 600
SCREEN_HEIGHT = 700

# высота границы
SCROLL_TRIGGER = 250

CREATE_ICICLE = pygame.USEREVENT
pygame.time.set_timer(CREATE_ICICLE, 5000)

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
image_platform = pygame.image.load('data/platform.png')  # платформа

image_gift = ['data/gift_1.png', 'data/gift_2.png', 'data/gift_3.png']

image_person = pygame.image.load('data\player.png')  # игрок
image_person_width = image_person.get_width()
image_person_height = image_person.get_height()

image_icicle = pygame.image.load('data/icicle.png')

sprite_player = pygame.sprite.Group()
sprite_platforms = pygame.sprite.Group()  # группа платформ
sprite_gift = pygame.sprite.Group()
sprite_icicle = pygame.sprite.Group()


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
        if pygame.sprite.spritecollideany(self, sprite_icicle):
            return True


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


# класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move, where_move, *group):
        super().__init__(*group)
        self.image = image_platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_move = move
        self.where_move = where_move

    def update(self, scroll):
        self.rect.y += scroll
        if self.is_move and self.where_move == 'left':
            self.rect.x -= 3
        if self.is_move and self.where_move == 'right':
            self.rect.x += 3

        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WINDTH

        if self.rect.x > SCREEN_WINDTH:
            self.rect.x = -self.rect.width
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


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
            self.rect.x = -self.platform_width  # доработать появление

        if pygame.sprite.spritecollideany(self, sprite_player):
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


player = Player(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 200)
sprite_player.add(player)
platform = Platform(SCREEN_WINDTH // 2 - image_person_width // 2, SCREEN_HEIGHT - 100, False, False)
sprite_platforms.add(platform)

# Основной игровой цикл
running = True
while running:
    # создание платформ
    if len(sprite_platforms) < 10:
        platform_width = 110
        platform_x = random.randint(0, SCREEN_WINDTH - platform_width)
        platform_y = platform.rect.y - random.randint(100, 120)

        move = True if random.randrange(1, 4) == 3 else False
        where_move = 'left' if random.randrange(1, 3) == 1 else 'right'

        give_gift = True if random.randrange(1, 6) == 1 else False
        if give_gift:
            gift = Gift(random.choice(image_gift), platform_x, platform_y, platform_width, move, where_move)
            sprite_gift.add(gift)

        platform = Platform(platform_x, platform_y, move, where_move)
        sprite_platforms.add(platform)

    screen.fill((210, 210, 210))
    pygame.draw.line(screen, 'black', (0, SCROLL_TRIGGER), (SCREEN_WINDTH, SCROLL_TRIGGER))

    scroll = player.move()

    sprite_platforms.update(scroll)
    sprite_platforms.draw(screen)

    sprite_player.draw(screen)

    sprite_gift.draw(screen)
    sprite_gift.update(scroll)

    sprite_icicle.draw(screen)
    sprite_icicle.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == CREATE_ICICLE:
            sprite_icicle.add(
                Icicle(random.randint(0, SCREEN_WINDTH - image_icicle.get_width()), -image_icicle.get_height() * 2))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                switch_pause()
    if player.check_end_game():  # если игрок упал, то появляется экран с game over
        end_screen()
        running = False
        pygame.quit()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
