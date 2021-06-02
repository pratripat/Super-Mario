from ..entity import Entity
from ..funcs import *

class Enemy(Entity):
    def __init__(self, game, position, type, animation_id):
        super().__init__(game.animations, type, position, animation_id)
        self.velocity[0] = -1
        self.game = game
        self.dead = False
        self.remove = False
        self.active = False
        self.falling = False
        self.max_distance = 816
        self.stomp_sfx = pygame.mixer.Sound('data/sfx/stomp.wav')

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll, vertical_flip=self.falling)

    def update(self, function=None, enemies=True):
        if not self.active:
            if self.on_screen:
                self.active = True
            return

        if self.falling:
            self.rect[1] += self.velocity[1]
            self.velocity[1] += 0.25

            if self.rect[1] > self.game.tilemap.bottom:
                self.remove = True

            return

        super().update(self.game.dt)

        for enemy in self.game.entities.enemies:
            if enemy != self and (enemy.id == 'koopa' or enemy.id == 'red_koopa') and (enemy.current_animation_id == 'koopa_rolling' or enemy.current_animation_id == 'red_koopa_rolling'):
                if rect_rect_collision(enemy.rect, self.rect):
                    self.falling = True
                    self.velocity[1] = -5
                    self.stomp_sfx.play()
                    return

        if self.dead:
            if int(self.current_animation.frame) == self.current_animation.animation_data.duration():
                self.remove = True
            return

        if self.game.paused:
            return

        self.movement()
        self.move(self.game.entities.get_colliding_entities(entity=self, enemies=enemies), self.game.dt)

        if self.game.entities.mario.directions['down'] and not self.game.entities.mario.collisions['bottom']:
            rect = self.game.entities.mario.rect.copy()
            rect[1] += self.game.entities.mario.velocity[1]

            if rect_rect_collision(rect, self.rect):
                if function:
                    function()

                self.game.entities.mario.rect[1] -= self.game.entities.mario.velocity[1]
                self.game.entities.mario.velocity[1] *= -1

    def movement(self):
        if self.collisions['bottom']:
            self.velocity[1] = 1

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] *= -1

        if self.velocity[0] < 0:
            self.flip(True)
        else:
            self.flip(False)

        self.velocity[1] += 1

    @property
    def on_screen(self):
        return (
            0 < self.position[0]-self.game.camera.scroll[0] < self.game.screen.get_width() and
            0 < self.position[1]-self.game.camera.scroll[1] < self.game.screen.get_height()
        )

    @property
    def far_from_mario(self):
        return self.game.entities.mario.position[0]-self.position[0] > self.max_distance
