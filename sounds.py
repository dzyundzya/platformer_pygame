import os

import pygame


pygame.mixer.init()

jump = pygame.mixer.Sound(os.path.join('sound', 'jump.ogg'))
fireball = pygame.mixer.Sound(os.path.join('sound', 'fireball.ogg'))
health = pygame.mixer.Sound(os.path.join('sound', 'health.ogg'))
coin = pygame.mixer.Sound(os.path.join('sound', 'coin.ogg'))
music = pygame.mixer.music.load(os.path.join('sound', 'theme.ogg'))
