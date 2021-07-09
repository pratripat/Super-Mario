import pygame

image1 = pygame.image.load('data/graphics/spritesheet/background.png')
image2 = pygame.image.load('data/graphics/images/spritesheet.png')

surface = pygame.Surface((image1.get_width(), image1.get_height()))

surface.blit(image1, (0,0))
surface.blit(image2, (0,image1.get_height()-image2.get_height()))

# pygame.image.save(surface, 'data/graphics/images/spritesheet2.png')
