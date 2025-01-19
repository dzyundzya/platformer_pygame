import os

import pygame
from pygame import mixer

import settings.constants as const
from objects.sounds import Sound


sound = Sound()


class Player(pygame.sprite.Sprite):
    """Создание главного персонажа."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move_x = 0  # Перемещение по оси Х.
        self.move_y = 0  # Перемещение по оси У.
        self.frame = 0  # Подсчет кадров.
        self.health = 10
        self.damage = 0
        self.score = 0
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(
                os.path.join(
                    'images/sprites/hero_sprites',
                    f'hero{i}.png')).convert()
            img.convert_alpha()
            img.set_colorkey(const.ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
        self.is_jumping = True
        self.is_falling = True
        # self.facing_right = True

    def control(self, x, y):
        """Управление перемещением персонажа."""
        self.move_x += x
        self.move_y += y

    def gravity(self):
        """Гравитация персонажа."""
        if self.is_jumping:
            self.move_y += 2  # Скорость падения.

        if self.rect.y > const.WORLD_Y and self.move_y >= 0:
            self.move_y = 0
            self.rect.y = const.WORLD_Y - const.ty - const.ty

    def jump(self):
        """Прыжок персонажа."""
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True
            mixer.Sound.play(sound.jump)

    def update(
            self, enemy_list, ground_list, plat_list, loot_list, healer_list
            ):
        """Обновление позиции спрайта."""
        self.rect.x = self.rect.x + self.move_x
        self.rect.y = self.rect.y + self.move_y

        # Движение влево.
        if self.move_x < 0:
            self.is_jumping = True  # Включает гравитацию.
            self.frame += 1
            if self.frame > 3 * const.ANI:
                self.frame = 0
            self.image = pygame.transform.flip(
                self.images[self.frame // const.ANI],
                True,
                False
            )
        # Движение вправо.
        if self.move_x > 0:
            self.is_jumping = True  # Включает гравитацию.
            self.frame += 1
            if self.frame > 3 * const.ANI:
                self.frame = 0
            self.image = self.images[self.frame // const.ANI]

        # Детектор столкновений c врагом.
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)

        if self.damage == 0:
            for enemy in enemy_hit_list:
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)

        if self.damage == 1:
            id_x = self.rect.collidelist(enemy_hit_list)
            if id_x == -1:
                self.damage = 0
                self.health -= 1

        # Детектор столкновения с землей.
        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for ground in ground_hit_list:
            self.move_y = 0
            self.rect.bottom = ground.rect.top
            self.is_jumping = False

        # Детектор столкновения с платформой.
        plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)
        for platform in plat_hit_list:
            self.move_y = 0
            self.is_jumping = False  # Останавливает прыжок.

            if self.rect.bottom <= platform.rect.bottom:
                self.rect.bottom = platform.rect.top
            else:
                self.move_y = 1.5

        # Детектор столкновения с лутом.
        loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1
            mixer.Sound.play(sound.coin)

        # Детектор столкновения с хилом.
        healer_hit_list = pygame.sprite.spritecollide(self, healer_list, True)
        for healer in healer_hit_list:
            healer_list.remove(healer)
            self.health += 15
            mixer.Sound.play(sound.health)

        # Детектор попадание за пределы карты.
        if self.rect.y > const.WORLD_Y:
            self.health -= 1
            self.rect.x = const.tx
            self.rect.y = const.ty

        # Реализация прыжка.
        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.move_y -= 33  # Настройка скорости прыжка.
