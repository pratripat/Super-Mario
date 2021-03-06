import pygame, math

class Brick_Piece:
    def __init__(self, game, position, angle, n):
        self.game = game
        self.image = pygame.image.load(f'data/graphics/images/{self.game.world_type}_brick_pieces/{n}.png').convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.image.set_colorkey((0,0,0))
        self.position = [position[0]-self.image.get_width()/2, position[1]]
        self.velocity = [math.cos(angle)*2, math.sin(angle)*2-2]

    def render(self):
        self.game.screen.blit(self.image, [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]])

    def update(self):
        self.position[0] += (self.velocity[0]*self.game.dt*self.game.framerate)
        self.position[1] += (self.velocity[1]*self.game.dt*self.game.framerate)

        self.velocity[1] += 0.2

    @property
    def offscreen(self):
        return (
            self.position[0]+self.image.get_width() < self.game.camera.scroll[0] or
            self.position[1] > self.game.tilemap.right or
            self.position[1] > self.game.tilemap.bottom
        )
