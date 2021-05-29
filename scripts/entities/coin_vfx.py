import math

class Coin:
    def __init__(self, game, position):
        self.game = game
        self.position = position
        self.offset = 0
        self.timer = 0
        self.max_height = 144
        self.updating = False
        self.animation = game.animations.get_animation('coin_from_block')

    def render(self):
        self.animation.render(self.game.screen, [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]-self.offset])

    def update(self):
        self.animation.run(self.game.dt)

        self.timer += self.game.dt*4
        self.offset = math.sin(self.timer)*self.max_height

    @property
    def finished(self):
        return int(self.offset) <= 0
