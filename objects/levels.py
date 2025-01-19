import os

import pygame

import settings.constants as const
from objects import BatEnemy


class Level:
    """Создание уровней."""

    enemy_location = [[290, 75], [200, 575]]

    def bad(lvl, enemy_loc=enemy_location):
        if lvl == 1:
            bat_enemy = BatEnemy(enemy_loc[0][0], enemy_loc[0][1])
            bat_enemy_2 = BatEnemy(enemy_loc[1][0], enemy_loc[1][1])
            enemy_list = pygame.sprite.Group()  # Саздание группы врагов.
            enemy_list.add(bat_enemy, bat_enemy_2)
        if lvl == 2:
            print(f'Level {lvl}')
        return enemy_list

    def ground(lvl, g_loc, width, height):
        """Создание земли."""
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(g_loc):
                ground = Platform(
                    g_loc[i],
                    const.WORLD_Y - const.ty,
                    const.tx, const.ty, 'tile.png'
                )
                ground_list.add(ground)
                i += 1
        if lvl == 2:
            print(f'Level {lvl}')
        return ground_list

    def platform(lvl, tx, ty):
        """Создание платформ."""
        plat_list = pygame.sprite.Group()
        p_loc = []
        i = 0
        if lvl == 1:
            p_loc.append((100, const.WORLD_Y - ty - 256, 3))
            p_loc.append((300, const.WORLD_Y - ty - 512, 3))
            p_loc.append((600, const.WORLD_Y - ty - 184, 2))
            p_loc.append((1200, const.WORLD_Y - ty - 184, 4))
            p_loc.append((1500, const.WORLD_Y - ty - 450, 4))
            p_loc.append((2000, const.WORLD_Y - ty - 150, 1))
            p_loc.append((2300, const.WORLD_Y - ty - 300, 1))
            p_loc.append((2600, const.WORLD_Y - ty - 450, 1))
            while i < len(p_loc):
                j = 0
                while j <= p_loc[i][2]:
                    plat = Platform(
                        (p_loc[i][0] + (j * tx)),
                        p_loc[i][1], tx, ty, 'tile.png'
                    )
                    plat_list.add(plat)
                    j += 1
                print(f'run {i} {p_loc[i]}')
                i += 1
        if lvl == 2:
            print(f'Level {lvl}')
        return plat_list

    def loot(lvl):
        """Создание лута."""
        loot_loc = []
        i = 0
        if lvl == 1:
            loot_list = pygame.sprite.Group()
            loot_loc.append((420, 75))
            loot_loc.append((690, 400))
            loot_loc.append((2055, 450))
            loot_loc.append((2355, 300))
            loot_loc.append((2655, 150))
            while i < len(loot_loc):
                loot = Platform(
                    loot_loc[i][0], loot_loc[i][1],
                    const.tx, const.ty, 'coin.png'
                )
                loot_list.add(loot)
                i += 1
        if lvl == 2:
            print(lvl)
        return loot_list

    def healer(lvl):
        """Создание хилок."""
        if lvl == 1:
            healer_list = pygame.sprite.Group()
            healer = Platform(1700, 75, const.tx, const.ty, 'health15.png')
            healer_list.add(healer)
        if lvl == 2:
            print(lvl)
        return healer_list


class Platform(pygame.sprite.Sprite):
    """Создание платформы."""

    def __init__(
            self, x_location, y_location, img_width, img_height, img_file
            ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join('images/stages', img_file)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(const.ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = y_location
        self.rect.x = x_location
