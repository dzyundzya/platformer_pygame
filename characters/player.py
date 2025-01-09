import os

import pygame

import constants


class Player(pygame.sprite.Sprite):
    """Создание главного персонажа."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move_x = 0  # Перемещение по оси Х.
        self.move_y = 0  # Перемещение по оси У.
        self.frame = 0  # Подсчет кадров.
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
        # Движение влево.
        if self.move_x < 0:
            self.frame += 1
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = self.images[self.frame // constants.ANI]
        # Движение вправо.
        if self.move_x > 0:
            self.frame += 1
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = self.images[self.frame // constants.ANI]


