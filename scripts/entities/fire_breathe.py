class Firebreathe:
    def __init__(self, game, rect, velocity=[-3,0]):
        self.game = game
        self.rect = rect
        self.velocity = velocity
        self.animation = self.game.animations.get_animation('fire_breathe')

    def render(self):
        self.animation.render(self.game.screen, [self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.game.camera.scroll[1]])

    def update(self):
        if not self.on_screen:
            return

        self.rect[0] += self.velocity[0]
        self.rect[1] += self.velocity[1]

    @property
    def on_screen(self):
        return (
            -self.rect.w < self.rect[0]-self.game.camera.scroll[0] < self.game.screen.get_width() and
            -self.rect.h < self.rect[1]-self.game.camera.scroll[1] < self.game.screen.get_height()
        )
