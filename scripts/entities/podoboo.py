from .enemy import Enemy

class Podoboo(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, list(rect.topleft), 'podoboo', '')
        self.gravity = False
        self.stompable = False
        self.target_position = self.rect[1]
        self.rect[1] = self.game.tilemap.bottom
        self.velocity[1] = -10
        self.velocity[0] = 0

    def update(self):
        if self.active:
            if not self.rect[1]-self.target_position>40:
                self.velocity[1] += 0.25
            if self.rect[1] >= self.game.tilemap.bottom+16.5*self.game.tilemap.RES:
                self.velocity[1] = -10

        super().update(None, False, False)

    @property
    def on_screen(self):
        return (
            -self.rect.w < self.position[0]-self.game.camera.scroll[0] < self.game.screen.get_width()
        )
