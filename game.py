import os
import sys

import pygame

import constants

"""
Переменные
"""
world_x = 960
world_y = 720

fps = 40  # Частота кадров.



"""
Объекты
"""


class Player(pygame.sprite.Sprite):
    """Создание главного персонажа."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move_x = 0  # Перемещение по оси Х.
        self.move_y = 0  # Перемещение по оси У.
        self.frame = 0  # Подсчет кадров.
        self.health = 10
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(
                os.path.join(
                    'images/sprites/hero_sprites',
                    f'hero{i}.png')).convert()
            img.convert_alpha()
            img.set_colorkey(constants.ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def control(self, x, y):
        """Управление перемещением персонажа."""
        self.move_x += x
        self.move_y += y

    def update(self):
        """Обновление позиции спрайта."""
        self.rect.x = self.rect.x + self.move_x
        self.rect.y = self.rect.y + self.move_y
        # Движение влево.
        if self.move_x < 0:
            self.frame += 1
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = pygame.transform.flip(
                self.images[self.frame // constants.ANI],
                True,
                False
            )
        # Движение вправо.
        if self.move_x > 0:
            self.frame += 1
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = self.images[self.frame // constants.ANI]

        # Детектор столкновений.
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
            print(self.health)


class BatEnemy(pygame.sprite.Sprite):
    """Создание врага - летучая мышь."""

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0  # Подсчет кадров.
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(
                os.path.join(
                    'images/sprites/bat_sprites',
                    f'bat{i}.png')).convert()
            img.convert_alpha()
            img.set_colorkey(constants.ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.counter = 0
            
    def move(self):
        """Перемещение врага."""
        distance = 80
        speed = 3
        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
            self.frame += 1
            if self.frame > 4 * constants.ANI:
                self.frame = 0
            self.image = pygame.transform.flip(
                self.images[self.frame // constants.ANI],
                True,
                False
            )
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= speed
            self.frame += 1
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = self.images[self.frame // constants.ANI]
        else:
            self.counter = 0
        self.counter += 1


class Level():
    """Создание уровней."""

    def bad(lvl, e_loc):
        if lvl == 1:
            bat_enemy = BatEnemy(e_loc[0], e_loc[1])
            enemy_list = pygame.sprite.Group()  # Саздание группы врагов.
            enemy_list.add(bat_enemy)  # Добавление врага в массив.
        if lvl == 2:
            print(f'Level {lvl}')
        return enemy_list



"""
Настройка
"""

clock = pygame.time.Clock()
pygame.init()

world = pygame.display.set_mode([world_x, world_y])
backdrop = pygame.image.load(os.path.join('images/stages', 'stage.png'))
backdrop_box = world.get_rect()


"""
Главный цикл
"""
running = True

player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)

e_loc = []
e_loc = [300, 0]
enemy_list = Level.bad(1, e_loc)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    running = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-constants.STEPS_PLAYER, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(constants.STEPS_PLAYER, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(constants.STEPS_PLAYER, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-constants.STEPS_PLAYER, 0)

    world.blit(backdrop, backdrop_box)
    player.update()  # Обновляет положение персонажа.
    player_list.draw(world)
    enemy_list.draw(world)
    for enemy in enemy_list:
        enemy.move()
    pygame.display.flip()
    clock.tick(fps)
