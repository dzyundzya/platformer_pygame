import os

import pygame

import settings.constants as const


class Throwball(pygame.sprite.Sprite):
    """Создание объекта дял метания."""
    def __init__(self, x, y, dir, fire, throw):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(
                os.path.join(
                    dir,
                    f'{fire}{i}.png')).convert()
            img.convert_alpha()
            img.set_colorkey(const.ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.firing = throw
        self.frame = 0

    def update(self, world_x):
        """Физика метания."""
        if self.rect.x < world_x:
            self.rect.x += 5  # C какой скоростью перемещается объект.
            self.frame += 1
            if self.frame > 3 * const.ANI:
                self.frame = 0
            self.image = self.images[self.frame // const.ANI]
        else:
            self.kill()  # Удаление объекта.
            self.firing = 0
