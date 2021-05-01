import pygame, math

class Brick_Piece:
    def __init__(self, game, position, angle):
        self.game = game
        self.image = pygame.transform.scale2x(pygame.image.load('data/graphics/images/brick_piece.png').convert())
        self.position = [position[0]-self.image.get_width()/2, position[1]]
        self.velocity = [math.cos(angle), math.sin(angle)-2]

    def render(self):
        angle = math.atan2(self.velocity[1], self.velocity[0])
        rotated_image = pygame.transform.rotate(self.image, angle)

        self.game.screen.blit(rotated_image, [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]])

    def update(self):
        self.position[0] += (self.velocity[0]*self.game.dt*80)
        self.position[1] += (self.velocity[1]*self.game.dt*80)

        self.velocity[1] += 0.1
