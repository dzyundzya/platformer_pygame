from pygame import mixer


mixer.init()


class Sound:
    def __init__(self):
        self.music = mixer.music.load('./sfx/theme.ogg')

        self.jump = mixer.Sound('./sfx/jump.ogg')
        self.fireball = mixer.Sound('./sfx/fireball.ogg')
        self.health = mixer.Sound('./sfx/health.ogg')
        self.coin = mixer.Sound('./sfx/coin.ogg')
        self.enemy_hit = mixer.Sound('./sfx/enemy hit.ogg')
