import os
import sys

import pygame

from characters.player import Player
from constants import STEPS_PLAYER



"""
Переменные
"""
world_x = 960
world_y = 720

fps = 40  # Частота кадров.



main = True

"""
Объекты
"""


"""
Настройка
"""

clock = pygame.time.Clock()
pygame.init()

world = pygame.display.set_mode([world_x, world_y])
backdrop = pygame.image.load(os.path.join('images/stages', 'stage.png'))
backdrop_box = world.get_rect()

player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)


"""
Главный цикл
"""

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-STEPS_PLAYER, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(STEPS_PLAYER, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(STEPS_PLAYER, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-STEPS_PLAYER, 0)

    world.blit(backdrop, backdrop_box)
    player_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
