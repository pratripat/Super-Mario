from .entity import Entity

class Mario(Entity):
    def __init__(self, game):
        super().__init__(game.animations, 'mario', [300,100], False, 'idle')
        self.game = game
        self.airtimer = 0
        self.speed = 6
        self.directions = {k:False for k in ['left', 'right', 'up', 'down']}
        self.directions['down'] = True

    def run(self):
        self.move(self.game.tilemap.get_tiles('tiles'), self.game.dt)
        self.movement()
        self.update(self.game.dt)

    def movement(self):
        # print(self.collisions)
        # print(self.directions)

        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 10

        if self.directions['left'] and not self.directions['right']:
            animation_state = 'run'
            self.velocity[0] -= 2
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)

        if self.directions['right'] and not self.directions['left']:
            animation_state = 'run'
            self.velocity[0] += 2
            self.velocity[0] = min(self.speed, self.velocity[0])
            self.flip(False)

        if not (self.directions['right'] or self.directions['left']):
            self.velocity[0] = 0

        if self.directions['down']:
            self.velocity[1] += 1

        #Jump
        elif self.directions['up']:
            if self.airtimer < 10:
                self.velocity[1] -= 4.6*self.airtimer/10
                self.airtimer += 1

            #If player is at max height, setting the upward movement false and allowing player to fall
            else:
                self.directions['up'] = False
                self.directions['down'] = True

        self.velocity[1] = min(8, self.velocity[1])

        self.set_animation(animation_state)
