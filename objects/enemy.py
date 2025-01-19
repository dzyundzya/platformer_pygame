import os

import pygame
from pygame import mixer

import settings.constants as const
from objects import sound


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
            img.set_colorkey(const.ALPHA)
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
            if self.frame > 4 * const.ANI:
                self.frame = 0
            self.image = pygame.transform.flip(
                self.images[self.frame // const.ANI],
                True,
                False
            )
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= speed
            self.frame += 1
            if self.frame > 3 * const.ANI:
                self.frame = 0
            self.image = self.images[self.frame // const.ANI]
        else:
            self.counter = 0
        self.counter += 1

    def update(self, firepower, enemy_list):
        """Обновления спрайта."""

        # Детектор столкновений с fireball.
        fireball_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fireball_hit_list:
            mixer.Sound.play(sound.enemy_hit, 0)
            enemy_list.remove(self)
