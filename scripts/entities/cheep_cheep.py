from .enemy import Enemy

class Cheep_Cheep(Enemy):
    def __init__(self, game, rect, index):
        super().__init__(game, list(rect.topleft), f'{["red", "grey"][index]}_cheep_cheep', 'swim')
        self.gravity = False
        self.stompable = False
        self.velocity = [-[1.1, 1][index],0]
        self.target_velocity = 0

    def load_velocity(self):
        if not self.target_velocity == 0:
            return

        if self.game.entities.mario.position[1] > self.position[1]:
            self.target_velocity = 1
        else:
            self.target_velocity = -1

    def update(self):
        if self.active:
            self.load_velocity()

            if self.game.game_timer % 10 == 0:
                self.rect[1] += self.target_velocity

        super().update(None, False, False)
