import os

from pygame import freetype

from settings.constants import FONT_SIZE, HEALTH_SCORE_SIZE, SCARLET
from settings.settings_game import world


font_path = os.path.join('fonts', 'spydi.ttf')


freetype.init()
my_font = freetype.Font(font_path, FONT_SIZE)


def stats(score, health):
    my_font.render_to(
        world, (775, 4), f'Score: {score}',
        SCARLET, None, size=HEALTH_SCORE_SIZE
    )
    my_font.render_to(
        world, (4, 4), f'Health: {health}',
        SCARLET, None, size=HEALTH_SCORE_SIZE
    )
