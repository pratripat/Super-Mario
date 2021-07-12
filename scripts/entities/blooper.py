from .enemy import Enemy

class Blooper(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, list(rect.topleft), 'blooper', 'swim_up')
        self.gravity = False
        self.stompable = False
        self.velocity = [0,0]
        self.timer = 1

    def update(self):
        if not self.velocity[1] > 0:
            if self.game.entities.mario.center[0]+self.game.tilemap.RES < self.center[0]:
                self.velocity[0] = -1
            elif self.game.entities.mario.center[0]-self.game.tilemap.RES > self.center[0]:
                self.velocity[0] =  1

        self.timer -= self.game.dt

        if self.timer <= 0:
            if self.game.entities.mario.center[1] < self.center[1] or self.rect[1] >= self.game.tilemap.bottom-self.game.tilemap.RES*6:
                self.velocity[1] = -1
                self.timer = 1
            elif self.game.entities.mario.center[1] > self.center[1]:
                self.velocity[1] = 1
                self.timer = 1

        if self.velocity[1] < 0:
            self.set_animation('swim_up')
        elif self.velocity[1] > 0:
            self.set_animation('swim_down')

        super().update(None, False, False)
