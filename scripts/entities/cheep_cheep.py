from .enemy import Enemy

class Cheep_Cheep(Enemy):
    def __init__(self, game, rect, index):
        super().__init__(game, list(rect.topleft), f'{["red", "grey", "red", "grey"][index]}_cheep_cheep', 'swim')
        self.gravity = False
        self.stompable = False
        self.velocity = [[1.1, 1, -1.1, -1][index],0]
        self.target_velocity = 0
        self.airtimer = 0

        if self.game.world_type != 'underwater':
            self.target_position = self.rect[1]
            self.rect[1] = self.game.tilemap.bottom
            self.velocity[1] = -10
            self.velocity[0] *= 2
            self.stompable = True

    def load_velocity(self):
        if not self.target_velocity == 0:
            return

        if self.game.entities.mario.position[1] > self.position[1]:
            self.target_velocity = 1
        else:
            self.target_velocity = -1

    def movement(self):
        if self.collisions['bottom'] and self.gravity:
            self.velocity[1] = 1

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] *= -1

        if self.velocity[0] < 0:
            self.flip(True)
        else:
            self.flip(False)

        if self.gravity:
            self.velocity[1] += 1

        self.velocity[1] = min(self.velocity[1], 20)

    def update(self):
        if self.active:
            if self.game.world_type == 'underwater':
                self.load_velocity()

                if self.game.game_timer % 10 == 0:
                    self.rect[1] += self.target_velocity
            else:
                if not self.rect[1]-self.target_position>40:
                    self.velocity[1] += 0.25

        super().update(self.die, False, False)

    def die(self):
        if self.stompable:
            self.dead = True
            self.falling = True
            self.stomp_sfx.play()

    @property
    def on_screen(self):
        return (
            -self.rect.w < self.position[0]-self.game.camera.scroll[0] < self.game.screen.get_width()
        )
