import os
import sys

import pygame
from pygame import freetype

import constants
import sounds


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
        self.damage = 0
        self.score = 0
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

        if self.rect.y > constants.WORLD_Y and self.move_y >= 0:
            self.move_y = 0
            self.rect.y = constants.WORLD_Y - ty - ty

    def jump(self):
        """Прыжок персонажа."""
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True
            pygame.mixer.Sound.play(sounds.jump)

    def update(self):
        """Обновление позиции спрайта."""
        self.rect.x = self.rect.x + self.move_x
        self.rect.y = self.rect.y + self.move_y

        # Движение влево.
        if self.move_x < 0:
            self.is_jumping = True  # Включает гравитацию.
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
            self.is_jumping = True  # Включает гравитацию.
            self.frame += 1
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = self.images[self.frame // constants.ANI]

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
            pygame.mixer.Sound.play(sounds.coin)

        # Детектор столкновения с хилом.
        healer_hit_list = pygame.sprite.spritecollide(self, healer_list, True)
        for healer in healer_hit_list:
            healer_list.remove(healer)
            self.health += 15
            pygame.mixer.Sound.play(sounds.health)

        # Детектор попадание за пределы карты.
        if self.rect.y > constants.WORLD_Y:
            self.health -= 1
            self.rect.x = tx
            self.rect.y = ty

        # Реализация прыжка.
        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.move_y -= 33  # Настройка скорости прыжка.


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

    def update(self, firepower, enemy_list):
        """Обновления спрайта."""

        # Детектор столкновений с fireball.
        fireball_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fireball_hit_list:
            pygame.mixer.Sound.play(sounds.enemy_hit, 0)
            enemy_list.remove(self)


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
            img.set_colorkey(constants.ALPHA)
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
            if self.frame > 3 * constants.ANI:
                self.frame = 0
            self.image = self.images[self.frame // constants.ANI]
        else:
            self.kill()  # Удаление объекта.
            self.firing = 0


class Level():
    """Создание уровней."""

    def bad(lvl, enemy_locaction):
        if lvl == 1:
            bat_enemy = BatEnemy(enemy_locaction[0][0], enemy_locaction[0][1])
            bat_enemy_2 = BatEnemy(enemy_locaction[1][0], enemy_locaction[1][1])
            enemy_list = pygame.sprite.Group()  # Саздание группы врагов.
            enemy_list.add(bat_enemy, bat_enemy_2)  # Добавление врага в массив.
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
                    gloc[i],
                    constants.WORLD_Y - ty,
                    tx, ty, 'tile.png'
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
            p_loc.append((100, constants.WORLD_Y - ty - 256, 3))
            p_loc.append((300, constants.WORLD_Y - ty - 512, 3))
            p_loc.append((600, constants.WORLD_Y - ty - 184, 2))
            p_loc.append((1200, constants.WORLD_Y - ty - 184, 4))
            p_loc.append((1500, constants.WORLD_Y - ty - 450, 4))
            p_loc.append((2000, constants.WORLD_Y - ty - 150, 1))
            p_loc.append((2300, constants.WORLD_Y - ty - 300, 1))
            p_loc.append((2600, constants.WORLD_Y - ty - 450, 1))
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
            loot_loc.append((2675, 150))
            loot_loc.append((2675, 150))
            loot_loc.append((2675, 150))
            while i < len(loot_loc):
                loot = Platform(loot_loc[i][0], loot_loc[i][1], tx, ty, 'coin.png')
                loot_list.add(loot)
                i += 1
        if lvl == 2:
            print(lvl)
        return loot_list
    
    def healer(lvl):
        """Создание хилок."""
        if lvl == 1:
            healer_list = pygame.sprite.Group()
            healer = Platform(1700, 75, tx, ty, 'health15.png')
            healer_list.add(healer)
        if lvl == 2:
            print(lvl)
        return healer_list


class Platform(pygame.sprite.Sprite):
    """Создание платформы."""

    def __init__(self, x_location, y_location, img_width, img_height, img_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join('images/stages', img_file)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(constants.ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = y_location
        self.rect.x = x_location


def stats(score, health):
    my_font.render_to(
        world, (775, 4), f'Score: {score}',
        constants.SCARLET, None, size=constants.HEALTH_SCORE_SIZE
    )
    my_font.render_to(
        world, (4, 4), f'Health: {health}',
        constants.SCARLET, None, size=constants.HEALTH_SCORE_SIZE
    )

"""
Настройка
"""

clock = pygame.time.Clock()
pygame.init()


font_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'fonts', 'spydi.ttf'
)
freetype.init()
my_font = freetype.Font(font_path, constants.FONT_SIZE)


world = pygame.display.set_mode([constants.WORLD_X, constants.WORLD_Y])
backdrop = pygame.image.load(os.path.join('images/stages', 'stage.png'))
backdrop_box = world.get_rect()

gloc = []
tx = constants.TILE_SIZE
ty = constants.TILE_SIZE

i = 0
while i <= (constants.WORLD_X / tx) + tx:
    gloc.append(i * tx)
    i += 1

ground_list = Level.ground(1, gloc, tx, ty)
plat_list = Level.platform(1, tx, ty)
loot_list = Level.loot(1)
healer_list = Level.healer(1)

"""
Главный цикл
"""
running = True

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

enemy_locaction = [[290, 75], [200, 575]]
enemy_list = Level.bad(1, enemy_locaction)

pygame.mixer.music.play(-1)

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
                player.jump()
            if event.key == pygame.K_SPACE:
                if not fireball.firing:
                    fireball = Throwball(
                        player.rect.x + constants.FB_DISTANCE, player.rect.y,
                        'images/sprites/fireball_sprites', 'fireball', 1
                    )
                    firepower.add(fireball)
                    pygame.mixer.Sound.play(sounds.fireball, loops=0)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(constants.STEPS_PLAYER, 0)
                # player.facing_right = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-constants.STEPS_PLAYER, 0)
                # player.facing_right = True

    # Прокрутка сцены вправо.
    if player.rect.x >= constants.FORWARD_X:
        scroll = player.rect.x - constants.FORWARD_X
        player.rect.x = constants.FORWARD_X
        for p in plat_list:
            p.rect.x -= scroll
        for enemy in enemy_list:
            enemy.rect.x -= scroll
        for loot in loot_list:
            loot.rect.x -= scroll
        for healer in healer_list:
            healer.rect.x -= scroll

    # Прокрутка сцены влево.
    if player.rect.x <= constants.BACKWARD_X:
        scroll = constants.BACKWARD_X - player.rect.x
        player.rect.x = constants.BACKWARD_X
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
    player.update()  # Обновляет положение персонажа.
    loot_list.draw(world)
    healer_list.draw(world)

    for enemy in enemy_list:
        enemy.move()

    if fireball.firing:
        fireball.update(constants.WORLD_X)
        firepower.draw(world)
        enemy_list.update(firepower, enemy_list)  # Обновление противника.

    player_list.draw(world)
    enemy_list.draw(world)
    ground_list.draw(world)
    plat_list.draw(world)

    stats(player.score, player.health)

    pygame.display.flip()
    clock.tick(constants.FPS)
