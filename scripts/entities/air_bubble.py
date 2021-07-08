import pygame

class Air_Bubble:
    def __init__(self, game, position):
        self.game = game
        self.position = position
        self.image = pygame.image.load('data/graphics/images/air_bubble.png').convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))
        self.image.set_colorkey((0,0,0))

    def render(self):
        self.game.screen.blit(self.image, [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]])

    def update(self):
        self.position[1] -= 1
