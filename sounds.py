import os

import pygame


pygame.mixer.init()

music = pygame.mixer.music.load(os.path.join('sound', 'theme.ogg'))

jump = pygame.mixer.Sound(os.path.join('sound', 'jump.ogg'))
fireball = pygame.mixer.Sound(os.path.join('sound', 'fireball.ogg'))
health = pygame.mixer.Sound(os.path.join('sound', 'health.ogg'))
coin = pygame.mixer.Sound(os.path.join('sound', 'coin.ogg'))
enemy_hit = pygame.mixer.Sound(os.path.join('sound', 'enemy hit.ogg'))
