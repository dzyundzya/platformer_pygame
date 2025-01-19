import os

import pygame

import settings.constants as const


world = pygame.display.set_mode([const.WORLD_X, const.WORLD_Y])
backdrop = pygame.image.load(os.path.join('images/stages', 'stage.png'))
backdrop_box = world.get_rect()


gloc = []

i = 0
while i <= (const.WORLD_X / const.tx) + const.tx:
    gloc.append(i * const.tx)
    i += 1
