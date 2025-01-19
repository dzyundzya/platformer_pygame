import sys

import pygame
from pygame import mixer

from objects import Level, Player, sound, Throwball
import settings.constants as const
from settings.fonts import stats
from settings.settings_game import backdrop, backdrop_box, gloc, world


def main():
    clock = pygame.time.Clock()
    pygame.init()

    pygame.mixer.music.play(-1)  # Активирует фоновый симпл.

    ground_list = Level.ground(1, gloc, const.tx, const.ty)
    plat_list = Level.platform(1, const.tx, const.ty)
    loot_list = Level.loot(1)
    healer_list = Level.healer(1)
    enemy_list = Level.bad(1)

    player = Player()
    player.rect.x = 0
    player.rect.y = 0
    player_list = pygame.sprite.Group()
    player_list.add(player)

    fireball = Throwball(
        player.rect.x, player.rect.y,
        'images/sprites/fireball_sprites', 'fireball', 0
    )
    firepower = pygame.sprite.Group()

    running = True

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
                    player.control(-const.STEPS_PLAYER, 0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.control(const.STEPS_PLAYER, 0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    player.jump()
                if event.key == pygame.K_SPACE:
                    if not fireball.firing:
                        fireball = Throwball(
                            player.rect.x + const.FB_DISTANCE, player.rect.y,
                            'images/sprites/fireball_sprites', 'fireball', 1
                        )
                        firepower.add(fireball)
                        mixer.Sound.play(sound.fireball, loops=0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.control(const.STEPS_PLAYER, 0)
                    # player.facing_right = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.control(-const.STEPS_PLAYER, 0)
                    # player.facing_right = True

        # Прокрутка сцены вправо.
        if player.rect.x >= const.FORWARD_X:
            scroll = player.rect.x - const.FORWARD_X
            player.rect.x = const.FORWARD_X
            for p in plat_list:
                p.rect.x -= scroll
            for enemy in enemy_list:
                enemy.rect.x -= scroll
            for loot in loot_list:
                loot.rect.x -= scroll
            for healer in healer_list:
                healer.rect.x -= scroll

        # Прокрутка сцены влево.
        if player.rect.x <= const.BACKWARD_X:
            scroll = const.BACKWARD_X - player.rect.x
            player.rect.x = const.BACKWARD_X
            for p in plat_list:
                p.rect.x += scroll
            for enemy in enemy_list:
                enemy.rect.x += scroll
            for loot in loot_list:
                loot.rect.x += scroll
            for healer in healer_list:
                healer.rect.x += scroll

        world.blit(backdrop, backdrop_box)
        player.gravity()  # Проверка гравитации.
        player.update(
            enemy_list, ground_list, plat_list, loot_list, healer_list
        )
        loot_list.draw(world)
        healer_list.draw(world)

        for enemy in enemy_list:
            enemy.move()

        if fireball.firing:
            fireball.update(const.WORLD_X)
            firepower.draw(world)
            enemy_list.update(firepower, enemy_list)  # Обновление противника.

        ground_list.draw(world)
        plat_list.draw(world)
        player_list.draw(world)
        enemy_list.draw(world)

        stats(player.score, player.health)

        pygame.display.flip()
        clock.tick(const.FPS)


if __name__ == '__main__':
    main()
